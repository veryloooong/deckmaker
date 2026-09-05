# Deckmaker

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

A pre-built `dist/deckmaker.exe` is included — just place your `vocab.csv` in the
same folder and double-click it, or run from a terminal:

```powershell
.\dist\deckmaker.exe
.\dist\deckmaker.exe --no-audio   # skip TTS if audio files already present
```

The CSV must have these columns: `Từ, Phát âm, Loại từ, Ý nghĩa, Ví dụ, Ghi chú`.

To rebuild the `.exe` yourself:

```bash
uv pip install pyinstaller
pyinstaller --onefile --console --name deckmaker --collect-all gtts deckmaker.py
```

## Usage

```bash
# Full run (generates audio + deck)
python deckmaker.py

# Skip audio generation (if audio files already exist)
python deckmaker.py --no-audio
```

This reads `vocab.csv` and produces `vocab.apkg` —
import it into Anki via **File → Import**.

## Updating an existing deck (adding words)

Cards are matched on a stable ID, so re-importing is safe: **existing cards keep
their progress; only genuinely new words are added.** Workflow:

1. Add the new word(s) to `vocab.csv`
2. Re-run deckmaker
3. Re-import `vocab.apkg` (File → Import) — Anki merges into the existing deck

> **One-time migration note:** decks built *before* the stable-ID fix carry
> random IDs and will duplicate once on the first re-import. To get a clean deck,
> delete the old "IELTS Vocabulary" deck in Anki and re-import once. After that,
> all re-imports are incremental.

Editing a word's text in `vocab.csv` changes its ID, so the old card is left
behind and a new one is added. Revert the edit (or delete the old card) to keep
things tidy.

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

| File                                  | Purpose                                                   |
| ------------------------------------- | --------------------------------------------------------- |
| `deckmaker.py`                        | Main script — parses CSV, generates audio, builds `.apkg` |
| `requirements.txt`                    | Python dependencies (`genanki`, `gtts`)                   |
| `Kế hoạch ôn thi IELTS - Từ vựng.csv` | Input vocabulary data                                     |
| `ielts_vocab.apkg`                    | Output Anki deck                                          |
| `audio/`                              | Generated TTS mp3 files                                   |
