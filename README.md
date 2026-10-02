# Deckmaker

[🇻🇳 Tiếng Việt](README_vi.md)

> **Notice:** This document has been updated by AI to include cross-language navigation, drag-and-drop / custom CSV support, and content parity with the Vietnamese guide.

Generate an IELTS vocabulary Anki deck programmatically from a CSV file.

## Anki Setup

Install the required Anki addon (needed for the MCQ card type):

1. Open Anki, go to **Tools → Add-ons**
2. Click **Get Add-ons…**
3. Enter the code: **`1566095810`**
4. Restart Anki

## Setup

```bash
uv pip install -r requirements.txt
```

## Standalone Executable (no Python needed)

A pre-built `dist/deckmaker.exe` is included. You can:
- **Drag and drop** any vocabulary `.csv` file directly onto `deckmaker.exe` in Windows Explorer.
- Run from terminal with an optional custom CSV path:

```powershell
.\dist\deckmaker.exe [path\to\vocab.csv]
.\dist\deckmaker.exe [path\to\vocab.csv] --no-audio   # skip TTS if audio files already present
```

The CSV must include these 6 columns (first row as headers):

| Từ | Phát âm | Loại từ | Ý nghĩa | Ví dụ | Ghi chú |
| --- | ------- | ------- | ------- | ----- | ------- |

Outputs `<filename>.apkg` in the same folder as the input CSV.

To rebuild the `.exe` yourself:

```bash
uv pip install pyinstaller
pyinstaller --onefile --console --name deckmaker --collect-all gtts deckmaker.py
```

## Usage

```bash
# Full run with default vocab.csv (or prompts if not found)
python deckmaker.py

# Full run with custom CSV file
python deckmaker.py path/to/my_words.csv

# Skip audio generation
python deckmaker.py path/to/my_words.csv --no-audio
```

If no arguments are provided and `vocab.csv` is not in the directory, the program interactively prompts you to drag and drop or enter the CSV path.

This reads the CSV and produces `<filename>.apkg` —
import it into Anki via **File → Import**.

## Updating an existing deck (adding words)

Cards are matched on a stable ID, so re-importing is safe: **existing cards keep
their progress; only genuinely new words are added.** Workflow:

1. Add new word(s) to your CSV or export a new CSV.
2. Re-run deckmaker (drag onto `deckmaker.exe` or run CLI).
3. Re-import `<filename>.apkg` (File → Import) — Anki merges into the existing deck.

> **One-time migration note:** decks built *before* the stable-ID fix carry
> random IDs and will duplicate once on the first re-import. To get a clean deck,
> delete the old "IELTS Vocabulary" deck in Anki and re-import once. After that,
> all re-imports are incremental.

Editing a word's text changes its ID, so the old card remains and a new one is added. Revert the edit (or delete the old card in Anki) to keep things tidy.

## Card Types

### 1. Word → Meaning (with audio)

Front shows the English word, IPA pronunciation, word type, and a **play button**
for TTS audio. Back reveals the Vietnamese meaning plus an example sentence.

### 2. MCQ Cloze

A sentence with the target word blanked out. You pick the correct word from
4 radio-button choices. Answer is colour-coded (green = correct, red = wrong)
with a score on the back. Uses the same JavaScript card template as the sample
addon (`1566095810`).

## Files

| File               | Purpose                                                   |
| ------------------ | --------------------------------------------------------- |
| `deckmaker.py`     | Main script — parses CSV, generates audio, builds `.apkg` |
| `requirements.txt` | Python dependencies (`genanki`, `gtts`, `pyinstaller`)     |
| `*.csv`            | Input vocabulary CSV                                      |
| `*.apkg`           | Output Anki deck                                          |
| `audio/`           | Generated TTS mp3 files                                   |

## Troubleshooting

| Issue | Resolution |
| ----- | ---------- |
| "CSV file is missing required headers" | Ensure row 1 has: `Từ, Phát âm, Loại từ, Ý nghĩa, Ví dụ, Ghi chú`. |
| "File not found" | Check the file path or drag and drop the CSV into the terminal / onto `deckmaker.exe`. |
| CSV text encoding looks garbled | Open CSV in an editor (like Notepad or VS Code) and save as **UTF-8** with BOM. |
| Missing audio | An internet connection is required for `gTTS` to generate new pronunciation files. |
| MCQ cards not rendering properly | Install Anki addon `1566095810` and restart Anki before importing. |
| Windows SmartScreen popup | Click **More info → Run anyway**. |

