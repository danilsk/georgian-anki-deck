"""Create a deduplicated speech manifest from the deck's Georgian targets."""
import csv
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parent
clips = json.loads((root / "pronunciation.json").read_text(encoding="utf-8"))

def normalized(text):
    return text.strip().rstrip(".?!…")

by_text = {normalized(clip["text"]): clip for clip in clips}
cards = {}
with (root / "practical.tsv").open(encoding="utf-8", newline="") as stream:
    for row in csv.reader(stream, delimiter="\t"):
        if not row or row[0].startswith("#"):
            continue
        front, back, notes, tags = row
        text = front.split(":", 1)[1].strip() if "recognition" in tags.split() else back
        assert re.fullmatch(r"[\u10d0-\u10ff\s.,?!…\-]+", text), text
        key = normalized(text)
        if key not in by_text:
            clip = {
                "id": "practical-" + hashlib.sha256(text.encode()).hexdigest()[:16],
                "text": text,
                "extra": "Also preserve ejective კ and ჭ and distinguish them from aspirated ქ and ჩ. Read the Georgian word or phrase exactly as written, once, without adding any words.",
            }
            by_text[key] = clip
            clips.append(clip)
        cards[front] = by_text[key]["id"]
manifest = {"clips": clips, "cards": cards}
(root / "audio-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{len(cards)} practical notes; {len(clips)} unique recordings including existing pronunciation clips")
