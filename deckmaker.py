#!/usr/bin/env python3
"""Deckmaker — Generate an IELTS vocabulary Anki deck from CSV.

Produces two card types:
  1. Word → Meaning (with TTS audio pronunciation)
  2. MCQ Cloze — sentence with blank, pick the correct word from 4 choices
"""

import csv
import os
import random
import re
import sys
import time

import genanki
from genanki.util import guid_for
from gtts import gTTS

# (AI) Ensure stdout and stderr handle UTF-8 cleanly across Windows consoles and environments
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ═══════════════════════════════════════════════════════════════════
#  Configuration
# ═══════════════════════════════════════════════════════════════════

# (AI) Default filenames, schema expectations, and audio cache location
DEFAULT_CSV = "vocab.csv"
REQUIRED_HEADERS = ["Từ", "Phát âm", "Loại từ", "Ý nghĩa", "Ví dụ", "Ghi chú"]
APP_DIR = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)
AUDIO_DIR = os.path.join(APP_DIR, "audio")

# genanki requires unique IDs — pick anything, just don't reuse
MODEL_WORD_ID = 1607392319
MODEL_MCQ_ID = 2059400110
DECK_ID = 3141592653

# ═══════════════════════════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════════════════════════


# (AI) Clean raw paths from drag-and-drop actions, stripping shell quotes and escape characters
def clean_path(raw_path: str) -> str:
    path = raw_path.strip().strip("'\"`")
    if os.name != "nt" and "\\ " in path:
        path = path.replace("\\ ", " ")
    return os.path.abspath(os.path.expanduser(path))


# (AI) Prevent instant terminal closure on Windows Explorer drag-and-drop or execution errors
def pause_if_needed() -> None:
    if "--no-pause" in sys.argv:
        return
    if os.name == "nt" and getattr(sys, "frozen", False):
        try:
            input("\nPress Enter to exit...")
        except (KeyboardInterrupt, EOFError):
            pass


# (AI) Determine input CSV path and options from CLI arguments, defaults, or interactive prompts
def resolve_cli_args() -> tuple[str, bool]:
    no_audio = "--no-audio" in sys.argv
    args = [a for a in sys.argv[1:] if a not in ("--no-audio", "--no-pause")]

    target_csv = ""
    if args:
        target_csv = clean_path(args[0])
    elif os.path.exists(DEFAULT_CSV):
        target_csv = os.path.abspath(DEFAULT_CSV)
    else:
        if sys.stdin and sys.stdin.isatty():
            print("No CSV file specified and 'vocab.csv' not found.")
            try:
                prompted = input("Drag and drop your CSV file here (or enter path): ")
                if prompted.strip():
                    target_csv = clean_path(prompted)
            except (KeyboardInterrupt, EOFError):
                print("\nCancelled.")
                sys.exit(0)

    if not target_csv:
        print("Error: No CSV file provided.")
        print("Usage: python deckmaker.py <path_to_vocab.csv> [--no-audio]")
        sys.exit(1)

    if not os.path.exists(target_csv):
        print(f"Error: File not found: {target_csv}")
        sys.exit(1)

    if not target_csv.lower().endswith(".csv"):
        print(f"Warning: File does not have a .csv extension: {target_csv}")

    return target_csv, no_audio


# (AI) Derive output .apkg path alongside the input CSV file
def get_output_path(csv_path: str) -> str:
    base_dir = os.path.dirname(csv_path)
    stem = os.path.splitext(os.path.basename(csv_path))[0]
    output_name = f"{stem}.apkg"
    target = os.path.join(base_dir, output_name)
    try:
        if os.access(base_dir, os.W_OK):
            return target
    except Exception:
        pass
    return os.path.abspath(output_name)


def sanitize_filename(name: str) -> str:
    """Turn a word into a safe mp3 filename."""
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", name).strip("_").lower()
    return f"{safe}.mp3" if safe else "unknown.mp3"


# (AI) Validate CSV headers against expected schema and extract vocabulary entries
def parse_csv(filepath: str) -> list[dict]:
    words: list[dict] = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            print(f"Error: CSV file is empty or missing headers: {filepath}")
            sys.exit(1)

        normalized_headers = [h.strip() for h in reader.fieldnames if h]
        missing_headers = [h for h in REQUIRED_HEADERS if h not in normalized_headers]
        if missing_headers:
            print(f"Error: CSV file is missing required headers: {filepath}")
            print(f"  Missing : {', '.join(missing_headers)}")
            print(f"  Expected: {', '.join(REQUIRED_HEADERS)}")
            print(f"  Found   : {', '.join(normalized_headers)}")
            sys.exit(1)

        for row in reader:
            row_clean = {k.strip(): v for k, v in row.items() if k}
            word = row_clean.get("Từ", "").strip()
            if not word:
                continue
            words.append(
                {
                    "word": word,
                    "pronunciation": row_clean.get("Phát âm", "").strip(),
                    "word_type": row_clean.get("Loại từ", "").strip(),
                    "meaning": row_clean.get("Ý nghĩa", "").strip(),
                    "example": row_clean.get("Ví dụ", "").strip(),
                    "notes": row_clean.get("Ghi chú", "").strip(),
                }
            )
    return words


def get_distractors(correct: dict, all_words: list[dict], count: int = 3) -> list[str]:
    """Pick *count* random distractor words, preferring the same word type."""
    same_type = [
        w
        for w in all_words
        if w["word"] != correct["word"] and w["word_type"] == correct["word_type"]
    ]
    other_type = [
        w
        for w in all_words
        if w["word"] != correct["word"] and w["word_type"] != correct["word_type"]
    ]
    random.shuffle(same_type)
    random.shuffle(other_type)

    result: list[str] = []
    seen: set[str] = set()
    for w in same_type + other_type:
        if w["word"] not in seen:
            result.append(w["word"])
            seen.add(w["word"])
        if len(result) == count:
            break
    return result


def blank_sentence(sentence: str, word: str) -> str:
    """Replace *word* in *sentence* with a blank (_____).

    For single words, matches on word boundaries to avoid partial matches.
    For multi-word phrases, uses exact substring matching.
    """
    if " " in word:
        # Multi-word phrase — exact match
        pattern = re.compile(re.escape(word), re.IGNORECASE)
    else:
        # Single word — word-boundary match (handles plurals, punctuation)
        pattern = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)

    blanked = pattern.sub("_____", sentence, count=1)
    if blanked and blanked[0].islower():
        blanked = blanked[0].upper() + blanked[1:]
    return blanked


# ═══════════════════════════════════════════════════════════════════
#  Audio generation (gTTS)
# ═══════════════════════════════════════════════════════════════════


def generate_audio(word: str, filepath: str) -> bool:
    """Generate TTS mp3 for *word* at *filepath*.  Returns True if created."""
    if os.path.exists(filepath):
        return False
    tts = gTTS(text=word, lang="en", slow=False)
    tts.save(filepath)
    return True


# ═══════════════════════════════════════════════════════════════════
#  Card Model 1 — Word → Meaning  (with audio)
# ═══════════════════════════════════════════════════════════════════

WORD_MODEL = genanki.Model(
    MODEL_WORD_ID,
    "IELTS Vocab (Word → Meaning)",
    css="""\
.card {
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  color: #333;
  background-color: #fff;
  padding: 12px;
}
.hidden { display: none; }
""",
    fields=[
        {"name": "Word"},
        {"name": "Pronunciation"},
        {"name": "WordType"},
        {"name": "Meaning"},
        {"name": "Example"},
        {"name": "Notes"},
        {"name": "AudioFile"},
    ],
    templates=[
        {
            "name": "Word Card",
            "qfmt": (
                '<div style="text-align:center;font-size:34px;font-weight:bold;'
                'margin:24px 0 8px;">{{Word}}</div>\n'
                '<div style="text-align:center;color:#888;font-size:18px;'
                'margin-bottom:6px;">/{{Pronunciation}}/</div>\n'
                '<div style="text-align:center;color:#999;font-size:14px;'
                'margin-bottom:24px;">({{WordType}})</div>\n'
                '<div style="text-align:center;">{{AudioFile}}</div>'
            ),
            "afmt": (
                "{{FrontSide}}\n"
                '<hr id="answer">\n'
                '<div style="text-align:center;font-size:28px;color:#2e7d32;'
                'font-weight:bold;margin:16px 0;">{{Meaning}}</div>\n'
                "{{#Example}}"
                '<div style="margin:16px 0;padding:12px;background:#f5f5f5;'
                'border-left:4px solid #4caf50;border-radius:4px;font-size:15px;">'
                '<i>"{{Example}}"</i></div>\n'
                "{{/Example}}"
                "{{#Notes}}"
                '<div style="margin-top:10px;color:#888;font-size:13px;">'
                "📝 {{Notes}}</div>\n"
                "{{/Notes}}"
            ),
        }
    ],
)

# ═══════════════════════════════════════════════════════════════════
#  Card Model 2 — MCQ Cloze  (adapted from the sample addon)
# ═══════════════════════════════════════════════════════════════════

_PERSISTENCE_JS = """\
<script>
if(void 0===window.Persistence){var _persistenceKey="github.com/SimonLammer/anki-persistence/",
_defaultKey="_default";
if(window.Persistence_sessionStorage=function(){var e=!1;try{"object"==typeof window.sessionStorage&&(
e=!0,this.clear=function(){for(var e=0;e<sessionStorage.length;e++){
var t=sessionStorage.key(e);0==t.indexOf(_persistenceKey)&&(sessionStorage.removeItem(t),e--)}},
this.setItem=function(e,t){void 0==t&&(t=e,e=_defaultKey),
sessionStorage.setItem(_persistenceKey+e,JSON.stringify(t))},
this.getItem=function(e){return void 0==e&&(e=_defaultKey),
JSON.parse(sessionStorage.getItem(_persistenceKey+e))},
this.removeItem=function(e){void 0==e&&(e=_defaultKey),
sessionStorage.removeItem(_persistenceKey+e)})}catch(e){}
this.isAvailable=function(){return e}},
window.Persistence_windowKey=function(e){var t=window[e],i=!1;
"object"==typeof t&&(i=!0,this.clear=function(){t[_persistenceKey]={}},
this.setItem=function(e,i){void 0==i&&(i=e,e=_defaultKey),t[_persistenceKey][e]=i},
this.getItem=function(e){return void 0==e&&(e=_defaultKey),t[_persistenceKey][e]||null},
this.removeItem=function(e){void 0==e&&(e=_defaultKey),delete t[_persistenceKey][e]},
void 0==t[_persistenceKey]&&this.clear()),this.isAvailable=function(){return i}},
window.Persistence=new Persistence_sessionStorage,
Persistence.isAvailable()||(window.Persistence=new Persistence_windowKey("py")),
!Persistence.isAvailable()){var titleStartIndex=window.location.toString().indexOf("title"),
titleContentIndex=window.location.toString().indexOf("main",titleStartIndex);
titleStartIndex>0&&titleContentIndex>0&&titleContentIndex-titleStartIndex<10&&(
window.Persistence=new Persistence_windowKey("qt"))}}
</script>
"""

_MCQ_FRONT_JS = """\
<script>
function generateTable(){
  var type=+document.getElementById("Card_Type").innerHTML||2;
  var tbody=document.createElement("tbody");
  stripHtmlTagsFromSolutionString();
  var solutions=getCorrectAnswers();
  var lines=[];
  for(var i=0;true;i++){
    var el=document.getElementById("Q_"+(i+1));
    if(!el||el.innerHTML.trim()==="")break;
    var txt=el.innerHTML;
    var html='<tr><td onInput="onCheck()" style="text-align:left;padding:6px 8px;">'
      +'<input id="inputQuestion'+(i+1)+'" name="ans_A" type="radio" value="1"> '
      +'<label for="inputQuestion'+(i+1)+'">'+txt+'</label></td></tr>';
    lines.push({html:html,solution:solutions[i]});
  }
  var shuffled=shuffleLines(lines,type);
  tbody.innerHTML=shuffled.map(function(o){return o.html}).join("");
  var table=document.createElement("table");
  table.style.border="1px solid #ccc";table.style.width="100%";
  table.appendChild(tbody);
  document.getElementById("qtable").innerHTML=table.innerHTML;
  storeCorrectAnswersInHtml(shuffled.map(function(o){return o.solution}));
  onCheck();
}
function stripHtmlTagsFromSolutionString(){
  var el=document.getElementById("Q_solutions");
  el.innerHTML=el.innerHTML.replace(/(<([^>]+)>)/gi,"");
}
function getCorrectAnswers(){
  return document.getElementById("Q_solutions").innerHTML.split(" ")
    .map(function(s){return Number(s)});
}
function storeCorrectAnswersInHtml(a){
  document.getElementById("Q_solutions").innerHTML=a.join(" ");
}
function shuffleLines(lines,type){
  var correct=lines.filter(function(o){return o.solution==1});
  var wrong=lines.filter(function(o){return o.solution==0});
  wrong.sort(function(){return Math.random()<0.5?-1:1});
  var idx=Math.floor(Math.random()*(wrong.length+1));
  wrong.splice(idx,0,correct[0]);
  return wrong;
}
function getUserAnswers(){
  var rows=document.getElementById("qtable")
    .getElementsByTagName("tbody")[0].getElementsByTagName("tr");
  var a=[];
  for(var i=0;i<rows.length;i++)
    a.push(rows[i].getElementsByTagName("td")[0]
      .getElementsByTagName("input")[0].checked?1:0);
  return a;
}
function onCheck(){
  if(Persistence.isAvailable()){
    Persistence.clear();
    Persistence.setItem("user_answers",getUserAnswers());
    Persistence.setItem("Q_solutions",getCorrectAnswers());
    Persistence.setItem("qtable",document.getElementById("qtable").innerHTML);
  }
}
function isMobile(){
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i
    .test(navigator.userAgent);
}
function sleep(ms){return new Promise(function(r){setTimeout(r,ms)});}
function run(){
  var ds="1 0 0 0";
  if(document.getElementById("Q_solutions").innerHTML
      ==="{"+"{"+"QSolutions"+"}"+"}")
    document.getElementById("Q_solutions").innerHTML=ds;
  setTimeout(generateTable,1);
}
(async function(){
  for(var i=0;i<100;i++){
    if(document.readyState==="complete"){run();break;}
    await sleep(100);
  }
})();
</script>
"""

_MCQ_BACK_JS = """\
<script>
function onLoad(){
  if(!Persistence.isAvailable||Persistence.getItem("Q_solutions")===null)return;
  var solutions=Persistence.getItem("Q_solutions");
  var answers=Persistence.getItem("user_answers");
  var type=+document.getElementById("CardType").innerHTML||2;
  var qtable=document.getElementById("qtable");
  qtable.innerHTML=Persistence.getItem("qtable");

  var output=document.getElementById("output");
  var atable=qtable.cloneNode(true);
  atable.setAttribute("id","atable");
  output.innerHTML="<hr id='answer'><h4>Correct Answer:</h4>"+atable.outerHTML;

  var qrows=qtable.getElementsByTagName("tbody")[0].getElementsByTagName("tr");
  var arows=document.getElementById("atable")
    .getElementsByTagName("tbody")[0].getElementsByTagName("tr");
  var canswers=0;

  for(var i=0;i<answers.length;i++){
    var s=solutions[i],a=answers[i];

    var qr=qrows[i].getElementsByTagName("td")[0].getElementsByTagName("input")[0];
    qr.checked=(a===1);qr.disabled=true;
    if(s===1&&a===1)qrows[i].setAttribute("class","correct");
    else if(s===0&&a===0)qrows[i].setAttribute("class","correct");
    else if(s===0&&a===1)qrows[i].setAttribute("class","wrong");
    else if(s===1&&a===0)qrows[i].setAttribute("class","wrong");

    var ar=arows[i].getElementsByTagName("td")[0].getElementsByTagName("input")[0];
    ar.setAttribute("name","ans_A_solution");
    ar.checked=(s===1);ar.disabled=true;

    if((s===1&&a===1)||(s===0&&a===0))canswers++;
  }

  var result=document.getElementById("canswerresult");
  result.innerHTML="<b>"+(canswers===solutions.length?"Correct!":"Nope.")+"</b>";
  Persistence.clear();
}
function isMobile(){
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i
    .test(navigator.userAgent);
}
function sleep(ms){return new Promise(function(r){setTimeout(r,ms)});}
function run(){
  if(!isMobile()&&typeof tickCheckboxOnNumberKeyDown!=="undefined")
    document.removeEventListener("keydown",tickCheckboxOnNumberKeyDown,!1);
  setTimeout(onLoad,1);
}
(async function(){
  if(document.readyState==="complete"){run();return;}
  if(isMobile()){document.addEventListener("DOMContentLoaded",
    function(){setTimeout(onLoad,1)},!1);return;}
  for(var i=0;i<100;i++){
    if(document.readyState==="complete"){run();break;}
    await sleep(100);
  }
})();
</script>
<style>
.correct{background-color:#c8e6c9;}
.wrong{background-color:#ffcdd2;}
</style>
"""

MCQ_MODEL = genanki.Model(
    MODEL_MCQ_ID,
    "IELTS Vocab (MCQ Cloze)",
    css="""\
.card {
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  color: #333;
  background-color: #fff;
  padding: 12px;
}
.hidden { display: none; }
.tappable {
  margin: 16px 0;
  user-select: none;
}
.tappable table {
  border-collapse: collapse;
  width: 100%;
}
.tappable td {
  padding: 10px 14px;
  border: 1px solid #ddd;
  cursor: pointer;
}
.tappable tr:hover {
  background-color: #f0f4f8;
}
.tappable label {
  cursor: pointer;
  display: inline-block;
  width: 100%;
}
.tappable input[type="radio"] {
  margin-right: 10px;
  transform: scale(1.2);
}
.correct { background-color: #c8e6c9 !important; }
.wrong   { background-color: #ffcdd2 !important; }
#canswerresult {
  margin-top: 18px;
  font-size: 18px;
}
.small { font-size: 12px; color: #888; }
""",
    fields=[
        {"name": "Question"},
        {"name": "Q1"},
        {"name": "Q2"},
        {"name": "Q3"},
        {"name": "Q4"},
        {"name": "QSolutions"},
        {"name": "Meaning"},
        {"name": "FullSentence"},
        {"name": "WordType"},
        {"name": "Notes"},
    ],
    templates=[
        {
            "name": "MCQ Card",
            "qfmt": (
                "<h3>Choose the correct word:</h3>\n"
                '<p style="font-size:18px;line-height:1.6;">'
                '<i>"{{Question}}"</i></p>\n'
                '<div class="tappable">'
                '<table style="border:1px solid #ccc;width:100%;" id="qtable">'
                "</table></div>\n"
                '<div class="hidden" id="Q_solutions">{{QSolutions}}</div>\n'
                '<div class="hidden" id="Card_Type">2</div>\n'
                '<div class="hidden" id="Q_1">{{Q1}}</div>\n'
                '<div class="hidden" id="Q_2">{{Q2}}</div>\n'
                '<div class="hidden" id="Q_3">{{Q3}}</div>\n'
                '<div class="hidden" id="Q_4">{{Q4}}</div>\n'
                + _PERSISTENCE_JS
                + _MCQ_FRONT_JS
            ),
            "afmt": (
                '<h3 style="color:#2e7d32;">{{Meaning}}</h3>\n'
                '<p style="font-size:15px;color:#888;">({{WordType}})</p>\n'
                '<p style="font-size:16px;line-height:1.6;">'
                '<i>"{{FullSentence}}"</i></p>\n'
                '<table id="qtable"></table>\n'
                '<p id="output"></p>\n'
                '<div class="hidden" id="MC_solutions">solutions_here</div>\n'
                '<div class="hidden" id="user_answers">user_answers_here</div>\n'
                '<div class="hidden" id="CardType">2</div>\n'
                '<p id="canswerresult"><b></b></p>\n'
                "{{#Notes}}"
                '<p style="color:#888;font-size:13px;margin-top:10px;">'
                "📝 {{Notes}}</p>\n"
                "{{/Notes}}" + _PERSISTENCE_JS + _MCQ_BACK_JS
            ),
        }
    ],
)

# ═══════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════


# (AI) Main entrypoint: resolve arguments, parse vocab, generate audio, and compile Anki deck
def main() -> None:
    csv_file, no_audio = resolve_cli_args()
    output_file = get_output_path(csv_file)

    print("=" * 60)
    print("  Deckmaker — IELTS Vocabulary Anki Deck Generator")
    print("=" * 60)

    # ── 1. Parse CSV ──────────────────────────────────────────────
    print(f"\n[1/4] Parsing CSV: {csv_file}")
    words = parse_csv(csv_file)
    print(f"  Found {len(words)} vocabulary entries.")
    if not words:
        print("  No words found. Exiting.")
        return

    # Scramble study order so the deck isn't grouped by CSV layout (categories
    # etc.). Safe for incremental imports: note GUIDs are content-derived
    # (word + example), not position-derived, so re-import dedup is unaffected.
    random.shuffle(words)

    # ── 2. Audio ──────────────────────────────────────────────────
    os.makedirs(AUDIO_DIR, exist_ok=True)
    media_files: list[str] = []

    if no_audio:
        print("\n[2/4] Skipping audio generation (--no-audio).")
        for w in words:
            media_files.append(os.path.join(AUDIO_DIR, sanitize_filename(w["word"])))
    else:
        print("\n[2/4] Generating audio with gTTS …")
        new_count = 0
        t0 = time.time()
        for i, w in enumerate(words):
            filename = sanitize_filename(w["word"])
            filepath = os.path.join(AUDIO_DIR, filename)
            if i > 0 and i % 40 == 0:
                elapsed = time.time() - t0
                eta = elapsed / i * (len(words) - i)
                print(f"  … {i}/{len(words)}  (ETA {eta:.0f}s)")
            if generate_audio(w["word"], filepath):
                new_count += 1
            media_files.append(filepath)
        print(f"  Done. {new_count} new files ({len(media_files)} total).")

    # ── 3. Build deck ─────────────────────────────────────────────
    print("\n[3/4] Building Anki deck …")
    deck = genanki.Deck(DECK_ID, "IELTS Vocabulary")
    word_notes = mcq_notes = skipped = 0

    for w in words:
        audio_filename = sanitize_filename(w["word"])
        audio_ref = f"[sound:{audio_filename}]"

        # --- Word Card ---
        deck.add_note(
            genanki.Note(
                model=WORD_MODEL,
                fields=[
                    w["word"],
                    w["pronunciation"],
                    w["word_type"],
                    w["meaning"],
                    w["example"],
                    w["notes"],
                    audio_ref,
                ],
            )
        )
        word_notes += 1

        # --- MCQ Cloze Card ---
        if not w["example"]:
            skipped += 1
            continue

        blanked = blank_sentence(w["example"], w["word"])
        distractors = get_distractors(w, words, count=3)
        if len(distractors) < 3:
            skipped += 1
            continue

        options = [w["word"]] + distractors
        deck.add_note(
            genanki.Note(
                model=MCQ_MODEL,
                # Stable GUID keyed on (word, example), NOT on the full field
                # list: MCQ fields include randomly-shuffled distractors, so a
                # content-derived GUID would change every build and re-import
                # would duplicate every MCQ card (resetting progress). Anki
                # dedupes on GUID — a stable one means re-importing only adds
                # genuinely new cards. The example is included so a word with
                # several example rows keeps one distinct card per row.
                guid=guid_for("mcq", w["word"], w["example"]),
                fields=[
                    blanked,
                    options[0],
                    options[1],
                    options[2],
                    options[3],
                    "1 0 0 0",
                    w["meaning"],
                    w["example"],
                    w["word_type"],
                    w["notes"],
                ],
            )
        )
        mcq_notes += 1

    print(
        f"  {word_notes} word cards  |  {mcq_notes} MCQ cards"
        + (f"  |  {skipped} skipped (no example)" if skipped else "")
    )

    # ── 4. Write package ──────────────────────────────────────────
    print(f"\n[4/4] Writing {output_file} …")
    existing_media = [f for f in media_files if os.path.exists(f)]
    if len(existing_media) < len(media_files):
        print(
            f"  Note: {len(media_files) - len(existing_media)} audio files missing"
            " — [sound:…] links will be silent."
        )
    pkg = genanki.Package(deck, media_files=existing_media)
    pkg.write_to_file(output_file)

    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"\n{'=' * 60}")
    print(f"  ✅  {output_file}  ({size_mb:.1f} MB)")
    print(f"  {word_notes} word cards  +  {mcq_notes} MCQ cards")
    print(f"  Import into Anki →  File → Import")
    print(f"{'=' * 60}")
    if getattr(sys, "frozen", False):
        pause_if_needed()


# (AI) Safe top-level runner catching errors and pausing on Windows/interactive runs
if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code != 0:
            pause_if_needed()
        sys.exit(e.code)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        pause_if_needed()
        sys.exit(1)
