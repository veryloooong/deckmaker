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
