# /// script
# requires-python = ">=3.11"
# dependencies = ["genanki==0.13.1"]
# ///
"""Build the portable Anki packages and TSVs (English and Russian); never touch a live Anki profile."""

import csv
import hashlib
import html
import json
from pathlib import Path
import re
import sqlite3
import struct
import tempfile
import wave
import zipfile
from collections import Counter

import genanki

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "georgian-essentials"
OUT.mkdir(exist_ok=True)
GEORGIAN = r"[ა-ჿ\s.,?!…\-]+"

CSS = """
.card { font-family: 'Noto Sans Georgian', 'DejaVu Sans', Arial, sans-serif;
  font-size: 24px; text-align: center; line-height: 1.65; color: #20242b;
  background: #faf8f3; padding: 24px; }
.prompt, .answer, .notes { max-width: 760px; margin: 0 auto; }
.answer { font-size: 32px; margin-top: 18px; }
.notes { font-size: 17px; text-align: left; margin-top: 24px; padding-top: 16px;
  border-top: 1px solid #b8b6ae; }
.hint { font-size: 15px; color: #656a70; margin-bottom: 14px; }
.audio { margin: 16px 0; }
hr { border: 0; border-top: 1px solid #b8b6ae; margin: 24px 0; }
.nightMode.card { color: #eeeeee; background: #202329; }
.nightMode .hint { color: #b8bec8; }
"""

LANGS = {
    "en": {
        "html_lang": "en", "source": "practical.tsv", "pronunciation": None,
        "deck_name": "Georgian - Essentials", "deck_id": 1824906731,
        "model_name": "Georgian Essentials — Practical + Listening", "model_id": 1928316457,
        "guid": "georgian-essentials-v1",
        "description": "Practical Georgian with usage notes, recognition prompts and synthetic pronunciation audio. No transliteration. See the included README for study and import instructions.",
        "apkg": "Georgian-Essentials.apkg", "cards": "cards.tsv", "preview": "preview.html",
        "validation": "validation.json", "templates": "templates",
        "card_names": ["Recall or pronounce", "Listen and repeat"],
        "listen_front": "Listen, repeat aloud, then identify the words.", "listen_back": "Listen and repeat",
        "read_aloud": "Read aloud:",
        "intro": "Practice the answer aloud before revealing it.",
        "search": "Find a word, phrase or tag", "placeholder": "e.g. core, transport, pronunciation, წყალი",
        "show": "Show answer", "switch": ("preview.ru.html", "ru", "Русская версия"),
    },
    "ru": {
        "html_lang": "ru", "source": "practical.ru.tsv", "pronunciation": "pronunciation.ru.json",
        "deck_name": "Грузинский - Самое нужное", "deck_id": 1739485210,
        "model_name": "Грузинский: самое нужное — практика + аудирование", "model_id": 1672094385,
        "guid": "georgian-essentials-ru-v1",
        "description": "Практический грузинский с заметками, карточками на узнавание и синтезированной озвучкой. Без транслитерации.",
        "apkg": "Georgian-Essentials-RU.apkg", "cards": "cards.ru.tsv", "preview": "preview.ru.html",
        "validation": "validation.ru.json", "templates": "templates/ru",
        "card_names": ["Вспомнить или произнести", "Послушать и повторить"],
        "listen_front": "Послушайте, повторите вслух и вспомните, что это значит.", "listen_back": "Послушайте и повторите",
        "read_aloud": "Прочитайте вслух:",
        "intro": "Сначала произнесите ответ вслух, потом открывайте.",
        "search": "Поиск по слову, фразе или тегу", "placeholder": "например: core, transport, pronunciation, წყალი",
        "show": "Показать ответ", "switch": ("preview.html", "en", "English version"),
    },
}


def read_tsv(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as stream:
        rows = [row for row in csv.reader(stream, delimiter="\t") if row and not row[0].startswith("#")]
    for lineno, row in enumerate(rows, 1):
        if len(row) != 4 or not all(row[:2] + row[3:]):
            raise ValueError(f"{name}: row {lineno}: Front, Back and Tags are required")
    return rows


def georgian_side(row):
    front, back, _, tags = row
    return front.split(":", 1)[1].strip() if "recognition" in tags.split() else back


manifest = json.loads((ROOT / "audio-manifest.json").read_text(encoding="utf-8"))
english_rows = read_tsv("practical.tsv")
clips = json.loads((ROOT / "pronunciation.json").read_text(encoding="utf-8"))

media_files = []
audio_checks = []
for clip in manifest["clips"]:
    filename = f'ge_essentials_{clip["id"]}.wav'
    file = OUT / "media" / filename
    with wave.open(str(file), "rb") as wav:
        assert (wav.getnchannels(), wav.getsampwidth(), wav.getframerate()) == (1, 2, 24000)
        assert wav.getcomptype() == "NONE"
        pcm = wav.readframes(wav.getnframes())
        duration = wav.getnframes() / wav.getframerate()
    samples = [sample[0] for sample in struct.iter_unpack("<h", pcm)]
    peak = max(abs(sample) for sample in samples)
    rms = (sum(sample * sample for sample in samples) / len(samples)) ** 0.5
    assert 0.4 <= duration <= 25 and peak > 100 and rms > 20, filename
    prompt = json.loads((OUT / "audio-prompts" / f'{clip["id"]}.json').read_text(encoding="utf-8"))
    assert prompt["request"]["input"].endswith("\n\n" + clip["text"])
    assert prompt["request"]["voice"] == "Charon"
    media_files.append(str(file))
    audio_checks.append({"filename": filename, "seconds": round(duration, 3),
                         "peak": peak, "rms": round(rms, 1),
                         "sha256": hashlib.sha256(file.read_bytes()).hexdigest()})


def build(lang):
    cfg = LANGS[lang]
    templates = [
        {
            "name": cfg["card_names"][0],
            "qfmt": '<div class="prompt">{{Front}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer"><div class="answer">{{Back}}</div>'
            '{{#Audio}}<div class="audio">{{Audio}}</div>{{/Audio}}'
            '{{#Notes}}<div class="notes">{{Notes}}</div>{{/Notes}}',
        },
        {
            "name": cfg["card_names"][1],
            "qfmt": f'{{{{#Audio}}}}<div class="hint">{cfg["listen_front"]}</div>'
            '<div class="audio">{{Audio}}</div>{{/Audio}}',
            "afmt": f'<div class="hint">{cfg["listen_back"]}</div><div class="audio">{{{{Audio}}}}</div>'
            '<hr id="answer"><div class="prompt">{{Front}}</div><div class="answer">{{Back}}</div>'
            '<div class="notes">{{Notes}}</div>',
        },
    ]

    source_rows = read_tsv(cfg["source"])
    if len(source_rows) != len(english_rows):
        raise ValueError(f'{cfg["source"]} has {len(source_rows)} rows; practical.tsv has {len(english_rows)}')
    rows = []
    original_fronts = {}
    for row, english in zip(source_rows, english_rows):
        front, back, notes, tags = row
        if tags != english[3] or georgian_side(row) != georgian_side(english):
            raise ValueError(f'{cfg["source"]}: "{front}" does not line up with "{english[0]}" in practical.tsv')
        if "recognition" not in tags.split() and not re.fullmatch(GEORGIAN, back):
            raise ValueError(f"Unexpected non-Georgian characters in answer: {back}")
        clip_id = manifest["cards"][english[0]]
        sound = f"<br>[sound:ge_essentials_{clip_id}.wav]"
        front_html, back_html = html.escape(front), html.escape(back)
        original_front = front_html
        if "recognition" in tags.split():
            front_html += sound
        else:
            back_html += sound
        original_fronts[front_html] = original_front
        rows.append([front_html, back_html, html.escape(notes), "", "georgian audio " + tags])

    # Preserve topic order within priority tiers. Actual review order is controlled by Anki settings.
    rows.sort(key=lambda row: "core" not in row[4].split())
    practical_count = len(rows)
    translations = {}
    if cfg["pronunciation"]:
        translations = {item["id"]: item for item in json.loads((ROOT / cfg["pronunciation"]).read_text(encoding="utf-8"))}
        assert set(translations) == {clip["id"] for clip in clips}
    for clip in clips:
        text = translations.get(clip["id"], clip)
        rows.append([
            cfg["read_aloud"] + "<br>" + html.escape(clip["text"]),
            html.escape(text["meaning"]),
            html.escape(text["notes"]),
            f'[sound:ge_essentials_{clip["id"]}.wav]',
            "georgian pronunciation audio",
        ])

    fronts = [row[0] for row in rows]
    if len(fronts) != len(set(fronts)):
        raise ValueError("Duplicate front fields")

    model = genanki.Model(
        cfg["model_id"], cfg["model_name"],
        fields=[{"name": name} for name in ["Front", "Back", "Notes", "Audio"]],
        templates=templates, css=CSS,
    )
    deck = genanki.Deck(cfg["deck_id"], cfg["deck_name"])
    deck.description = cfg["description"]
    for index, row in enumerate(rows, 1):
        deck.add_note(genanki.Note(
            model=model, fields=row[:4], tags=row[4].split(),
            guid=genanki.guid_for(cfg["guid"], original_fronts.get(row[0], row[0])), due=index,
        ))
    package = genanki.Package(deck)
    package.media_files = media_files
    apkg = OUT / cfg["apkg"]
    package.write_to_file(str(apkg))

    with (OUT / cfg["cards"]).open("w", encoding="utf-8", newline="") as stream:
        stream.write("#separator:Tab\n#html:true\n#tags column:5\n")
        stream.write(f'#notetype:{cfg["model_name"]}\n#deck:{cfg["deck_name"]}\n')
        stream.write("#columns:Front\tBack\tNotes\tAudio\tTags\n")
        csv.writer(stream, delimiter="\t", lineterminator="\n").writerows(rows)

    templates_dir = OUT / cfg["templates"]
    templates_dir.mkdir(exist_ok=True)
    (templates_dir / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    for index, template in enumerate(templates, 1):
        for side, key in [("front", "qfmt"), ("back", "afmt")]:
            (templates_dir / f"{index}-{side}.html").write_text(template[key] + "\n", encoding="utf-8")

    # Read-only preview, with local audio and no network requests.
    preview = []
    def browser_audio(field):
        return re.sub(r"\[sound:([^\]]+)\]", lambda match: '<audio controls preload="none" src="media/' + html.escape(match[1]) + '"></audio>', field)

    for row in rows:
        sound = re.fullmatch(r"\[sound:([^\]]+)\]", row[3])
        player = f'<audio controls preload="none" src="media/{html.escape(sound[1])}"></audio>' if sound else ""
        preview.append(f'<article><small>{html.escape(row[4])}</small><h2>{browser_audio(row[0])}</h2>'
                       f'<details><summary>{cfg["show"]}</summary><h3>{browser_audio(row[1])}</h3>{player}<p>{row[2]}</p></details></article>')
    switch_href, switch_lang, switch_text = cfg["switch"]
    (OUT / cfg["preview"]).write_text(f"""<!doctype html>
<html lang="{cfg["html_lang"]}"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{cfg["deck_name"]}</title>
<style>body{{font-family:'Noto Sans Georgian',Arial,sans-serif;max-width:850px;margin:32px auto;padding:0 20px;background:#faf8f3;color:#20242b;line-height:1.7}}article{{padding:20px 0;border-bottom:1px solid #ccc}}h2,h3{{font-weight:500;font-size:24px}}small{{color:#60656d}}summary{{cursor:pointer}}input{{box-sizing:border-box;width:100%;font:inherit;padding:12px}}audio{{max-width:100%}}[hidden]{{display:none}}</style>
<p><a href="{switch_href}" hreflang="{switch_lang}" lang="{switch_lang}">{switch_text}</a></p>
<h1>{cfg["deck_name"]}</h1>
<p>{cfg["intro"]}</p>
<label for="search">{cfg["search"]}</label><input id="search" type="search" placeholder="{cfg["placeholder"]}">
""" + "\n".join(preview) + """
<script>document.querySelector('#search').addEventListener('input',e=>{const q=e.target.value.toLocaleLowerCase();document.querySelectorAll('article').forEach(a=>{a.hidden=!a.textContent.toLocaleLowerCase().includes(q)})})</script></html>
""", encoding="utf-8")

    # Inspect the finished archive and its database, without opening a user's collection.
    with zipfile.ZipFile(apkg) as archive:
        assert archive.testzip() is None
        media_map = json.loads(archive.read("media"))
        assert set(media_map.values()) == {Path(file).name for file in media_files}
        referenced_media = {name for row in rows for field in row[:4] for name in re.findall(r"\[sound:([^\]]+)\]", field)}
        assert referenced_media == set(media_map.values())
        assert all(any("[sound:" in field for field in row[:4]) for row in rows)
        for key, filename in media_map.items():
            assert archive.read(key) == (OUT / "media" / filename).read_bytes()
        with tempfile.TemporaryDirectory(prefix="georgian-anki-check-") as temp:
            db = Path(temp) / "collection.anki2"
            db.write_bytes(archive.read("collection.anki2"))
            connection = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
            note_count = connection.execute("SELECT count(*) FROM notes").fetchone()[0]
            card_count = connection.execute("SELECT count(*) FROM cards").fetchone()[0]
            listening_count = connection.execute("SELECT count(*) FROM cards WHERE ord = 1").fetchone()[0]
            assert note_count == len(rows)
            assert card_count == len(rows) + len(clips)
            assert listening_count == len(clips)
            stored_fields = [record[0].split("\x1f") for record in connection.execute("SELECT flds FROM notes")]
            assert all(len(fields) == 4 for fields in stored_fields)
            assert sorted(stored_fields) == sorted(row[:4] for row in rows)
            connection.close()
    with (OUT / cfg["cards"]).open(encoding="utf-8", newline="") as stream:
        imported = list(csv.reader((line for line in stream if not line.startswith("#")), delimiter="\t"))
        assert imported == rows

    report = {
        "notes": note_count, "cards": card_count, "practical_cards": practical_count,
        "pronunciation_read_aloud_cards": len(clips), "listening_cards": listening_count,
        "core_notes": sum("core" in row[4].split() for row in rows),
        "tags": dict(Counter(tag for row in rows for tag in row[4].split())),
        "media_files": len(media_files), "audio": audio_checks,
        "notes_with_audio": sum(any("[sound:" in field for field in row[:4]) for row in rows),
        "validation": "TSV round-trip, unique fronts, Georgian-only production answers, archive CRC, SQLite integrity, card counts, field equality, media hashes, prompt/text matching, WAV format and non-silent signal passed.",
        "limits": "No live Anki profile modified. No Anki UI import tested.",
    }
    (OUT / cfg["validation"]).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ["notes", "cards", "practical_cards", "pronunciation_read_aloud_cards", "listening_cards", "core_notes", "media_files"]}, indent=2))
    print(f"Created {apkg}")


for lang in LANGS:
    build(lang)
