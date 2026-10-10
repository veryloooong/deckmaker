import json
import os
import sys
import tempfile
import unittest
import urllib.error
from unittest import mock

# (AI) Ensure stdout and stderr handle UTF-8 cleanly across Windows test runners
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# (AI) Add root repository path to module lookup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import deckmaker


class TestDeckmaker(unittest.TestCase):
    # (AI) Test stripping surrounding quotes, backticks, and shell escapes from paths
    def test_clean_path(self):
        self.assertEqual(
            deckmaker.clean_path('  "path/to/file.csv"  '),
            os.path.abspath("path/to/file.csv"),
        )
        self.assertEqual(
            deckmaker.clean_path("  'path/to/file.csv'  "),
            os.path.abspath("path/to/file.csv"),
        )
        self.assertEqual(
            deckmaker.clean_path("`path/to/file.csv`"),
            os.path.abspath("path/to/file.csv"),
        )
        if os.name != "nt":
            self.assertEqual(
                deckmaker.clean_path("path/to/my\\ file.csv"),
                os.path.abspath("path/to/my file.csv"),
            )

    # (AI) Test output file path derivation alongside input CSV
    def test_get_output_path(self):
        csv_path = os.path.abspath("sample_data.csv")
        expected = os.path.abspath("sample_data.apkg")
        self.assertEqual(deckmaker.get_output_path(csv_path), expected)

    # (AI) Test valid 6-column header CSV parsing
    def test_parse_csv_valid_headers(self):
        with tempfile.NamedTemporaryFile(
            "w+", encoding="utf-8-sig", suffix=".csv", delete=False
        ) as f:
            f.write("Từ,Phát âm,Loại từ,Ý nghĩa,Ví dụ,Ghi chú\n")
            f.write("test,/test/,noun,kiểm tra,This is a test sentence.,ghi chú\n")
            temp_path = f.name

        try:
            words = deckmaker.parse_csv(temp_path)
            self.assertEqual(len(words), 1)
            self.assertEqual(words[0]["word"], "test")
            self.assertEqual(words[0]["meaning"], "kiểm tra")
            self.assertEqual(words[0]["example"], "This is a test sentence.")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # (AI) Test missing required headers exit code
    def test_parse_csv_missing_headers(self):
        with tempfile.NamedTemporaryFile(
            "w+", encoding="utf-8-sig", suffix=".csv", delete=False
        ) as f:
            f.write("Từ,Ý nghĩa\n")
            f.write("test,kiểm tra\n")
            temp_path = f.name

        try:
            with self.assertRaises(SystemExit) as cm:
                deckmaker.parse_csv(temp_path)
            self.assertEqual(cm.exception.code, 1)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class _FakeHttpResponse:
    """Minimal stand-in for the object urlopen() returns."""

    def __init__(self, payload):
        self._body = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False


def _word(word="abandon", meaning="từ bỏ"):
    return {
        "word": word,
        "pronunciation": f"/{word}/",
        "word_type": "verb",
        "meaning": meaning,
        "example": f"They {word} it.",
        "notes": "",
    }


class TestAnkiPush(unittest.TestCase):
    # (AI) Test that --anki is recognised and never mistaken for the CSV path
    def test_resolve_cli_args_anki_flag(self):
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", suffix=".csv", delete=False
        ) as f:
            f.write("Từ,Phát âm,Loại từ,Ý nghĩa,Ví dụ,Ghi chú\n")
            temp_path = f.name

        original_argv = sys.argv
        try:
            sys.argv = ["deckmaker.py", temp_path, "--anki", "--no-audio", "--no-pause"]
            csv_file, no_audio, push_anki = deckmaker.resolve_cli_args()
            self.assertEqual(csv_file, os.path.abspath(temp_path))
            self.assertTrue(no_audio)
            self.assertTrue(push_anki)

            # Flag first: it must still be filtered out, not read as the CSV path.
            sys.argv = ["deckmaker.py", "--anki", temp_path]
            csv_file, no_audio, push_anki = deckmaker.resolve_cli_args()
            self.assertEqual(csv_file, os.path.abspath(temp_path))
            self.assertFalse(no_audio)
            self.assertTrue(push_anki)

            # Absent by default.
            sys.argv = ["deckmaker.py", temp_path]
            self.assertFalse(deckmaker.resolve_cli_args()[2])
        finally:
            sys.argv = original_argv
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # (AI) Test the AnkiConnect request envelope, error field, and connection failure
    def test_anki_invoke_request_and_error(self):
        captured = {}

        def fake_urlopen(request, timeout=None):
            captured["url"] = request.full_url
            captured["body"] = json.loads(request.data.decode("utf-8"))
            return _FakeHttpResponse({"result": 6, "error": None})

        with mock.patch.object(deckmaker.urllib.request, "urlopen", fake_urlopen):
            self.assertEqual(deckmaker.anki_invoke("version"), 6)

        self.assertEqual(captured["url"], deckmaker.ANKI_CONNECT_URL)
        self.assertEqual(
            captured["body"],
            {"action": "version", "version": deckmaker.ANKI_API_VERSION, "params": {}},
        )

        with mock.patch.object(
            deckmaker.urllib.request,
            "urlopen",
            lambda request, timeout=None: _FakeHttpResponse(
                {"result": None, "error": "unsupported action"}
            ),
        ):
            with self.assertRaises(RuntimeError):
                deckmaker.anki_invoke("nonsense")

        with mock.patch.object(
            deckmaker.urllib.request,
            "urlopen",
            side_effect=urllib.error.URLError("connection refused"),
        ):
            with self.assertRaises(urllib.error.URLError):
                deckmaker.anki_invoke("version")

    # (AI) Test that an unreachable Anki warns and falls back instead of raising
    def test_push_to_anki_returns_false_when_unreachable(self):
        with (
            mock.patch.object(
                deckmaker,
                "anki_import_package",
                side_effect=RuntimeError("Anki is closed"),
            ),
            mock.patch("builtins.print") as printed,
        ):
            self.assertFalse(deckmaker.push_to_anki("/tmp/words.apkg"))

        output = "\n".join(
            str(call.args[0]) for call in printed.call_args_list if call.args
        )
        self.assertIn("File → Import", output)

    # (AI) Test the success path
    def test_push_to_anki_returns_true_on_success(self):
        with (
            mock.patch.object(deckmaker, "anki_import_package"),
            mock.patch("builtins.print"),
        ):
            self.assertTrue(deckmaker.push_to_anki("/tmp/words.apkg"))

    # (AI) Test that editing a field no longer changes the word note GUID
    def test_build_word_note_guid_is_stable(self):
        first = deckmaker.build_word_note(_word(), "[sound:abandon.mp3]")
        edited = deckmaker.build_word_note(
            _word(meaning="bỏ rơi"), "[sound:abandon.mp3]"
        )
        other = deckmaker.build_word_note(_word(word="abduct"), "[sound:abduct.mp3]")

        self.assertEqual(first.guid, edited.guid)
        self.assertNotEqual(first.fields[3], edited.fields[3])
        self.assertNotEqual(first.guid, other.guid)


if __name__ == "__main__":
    unittest.main()
