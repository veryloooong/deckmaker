# AGENTS.md

> **Notice:** Sections _Run_, _Gotchas_, and _CI/CD_ have been updated by AI to reflect custom CSV input paths, test suites, and the automated Windows PyInstaller pipeline.

Single-file Python script (`deckmaker.py`) that turns a CSV of IELTS vocab into an
Anki `.apkg` (via `genanki`) with TTS audio (via `gTTS`). Unit tests in `tests/test_deckmaker.py`.
Deps in `requirements.txt`: `genanki>=0.13.0`, `gtts>=2.5.0`, `pyinstaller>=6.0.0`.

## Run

```bash
uv run python deckmaker.py                           # default run (looks for vocab.csv or prompts)
uv run python deckmaker.py path/to/my_words.csv      # run with specific CSV
uv run python deckmaker.py path/to/words.csv --no-audio  # skip TTS, use existing audio/ files
uv run python deckmaker.py path/to/words.csv --anki      # push into running Anki (AnkiConnect addon)
```

- No system `python3`; always use `uv run` (or `.venv/bin/python`).
- Input is any CSV file passed via CLI, drag-and-dropped onto `deckmaker.exe` / terminal,
  or default `vocab.csv`. Columns must include Vietnamese headers: `Từ, Phát âm, Loại từ, Ý nghĩa, Ví dụ, Ghi chú`.
  Read with `utf-8-sig` encoding. Missing headers trigger an informative exit.
- Output: `<csv_stem>.apkg` in the same directory as the CSV + shared `audio/` mp3s (both gitignored).
- `gTTS` needs network access.
- Note GUIDs are set in `build_word_note` (Word, `guid_for("word", word)`) and
  inline for MCQ (`guid_for("mcq", word, example)`). Word cards used to rely on
  genanki's content-derived default GUID, so editing any field duplicated the
  card and orphaned progress; that is fixed, but decks built before the change
  duplicate once per edited word. Never switch either GUID back to
  content-derived or every re-import resets progress.
- `--anki` pushes the built `.apkg` into a running Anki via **AnkiConnect**
  (addon `2055492159`, HTTP `127.0.0.1:8765`, override with `ANKI_CONNECT_URL`).
  `push_to_anki` is warn-only: it catches everything, prints the manual
  `File → Import` fallback, and the run still exits 0 with the `.apkg` written.
  `importPackage` path semantics are ambiguous upstream (docs say relative to
  Anki's `collection.media`), so `anki_import_package` tries the absolute path
  first and then stages a copy in `getMediaDirPath()`.
- Transport is stdlib `urllib`, deliberately not `requests` — keeps
  `requirements.txt` and the PyInstaller onefile command unchanged.
- New CLI flags must be added to **both** the `in sys.argv` check and the filter
  list in `resolve_cli_args` (`deckmaker.py:70-104`), otherwise the flag is
  consumed as the CSV path.

## Gotchas

- genanki model/deck IDs are hardcoded constants in `deckmaker.py` (lines ~28-30).
  When adding a card model or deck, use fresh IDs — genanki errors on collisions.
- Card generation: Word→Meaning card is always added; MCQ cloze card is skipped
  per word when `Ví dụ` (example) is empty or fewer than 3 distractor words exist
  (`deckmaker.py:531-539`).
- Audio files are skipped if already on disk (`generate_audio`). With `--no-audio`,
  missing mp3s produce silent `[sound:…]` links (warned at runtime, `deckmaker.py:568-573`).
- Note GUIDs drive Anki's import dedup — a changed GUID = duplicate card + orphaned
  progress. Word cards get genanki's default GUID (hash of all fields → stable while
  content is unchanged). MCQ cards get an explicit stable GUID `guid_for("mcq", word, example)`
  because their fields contain randomly-shuffled distractors that would otherwise change
  the GUID every build (this was the "import resets progress" bug). Re-importing an
  updated deck therefore only adds genuinely new cards.
- Migration: decks imported before this GUID fix contain old random MCQ GUIDs — the
  first re-import after the fix adds one duplicate MCQ set. Delete the old deck in Anki
  and re-import once to get a clean, stable deck; future re-imports are incremental.
- Rewrite of the shipped `dist/deckmaker.exe`: `uv pip install pyinstaller && pyinstaller --onefile --console --name deckmaker --collect-all gtts deckmaker.py`.
  This is automated in `.github/workflows/build-exe.yml`: runs unit tests, compiles `dist/deckmaker.exe`
  on Windows (`windows-latest`), runs a smoke test against `tests/sample.csv`, uploads artifact `deckmaker-windows`,
  and attaches the binary to a GitHub Release on `v*` tags with write permissions.
  The smoke test intentionally omits `--anki` — no Anki/AnkiConnect exists on the
  CI runner.
