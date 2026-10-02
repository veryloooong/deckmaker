import os
import sys
import tempfile
import unittest

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
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8-sig", suffix=".csv", delete=False) as f:
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
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8-sig", suffix=".csv", delete=False) as f:
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


if __name__ == "__main__":
    unittest.main()
