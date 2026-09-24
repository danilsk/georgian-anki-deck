# Georgian - Essentials

An Anki deck of practical Georgian for everyday use: shops and bazaars, restaurants, transport, numbers and money, accommodation, health and emergencies, and the replies you will hear back. Georgian script throughout, no transliteration. It teaches no grammar. It also drills the sounds most learners struggle with: the aspirated/ejective pairs ფ/პ, თ/ტ, ქ/კ, ც/წ and ჩ/ჭ as real minimal pairs (ფური/პური, ქარი/კარი), the uvular ყ, and awkward clusters like წყ and ვსწ, up to the ბაყაყი წყალში ყიყინებს tongue twister. 

Every Georgian target has audio, generated with Google's `gemini-3.1-flash-tts-preview` and confirmed by a native speaker to sound very good, though he did catch a couple of slips.

**396 cards** from 378 notes — 360 practical, 18 read-aloud pronunciation drills, 18 listening cards — with 373 recordings.

## Get the deck

Download **`georgian-essentials/Georgian-Essentials.apkg`** and use **File → Import** in Anki. The package carries the note type, card layouts and all audio; nothing needs to be copied by hand.

`georgian-essentials/README.md` covers importing, study order, the tag list and the TSV route for people who want to edit the cards.

**[Browse all 396 cards in your browser](https://danilsk.github.io/georgian-anki-deck/)** — search the whole deck and play any recording without installing anything. AnkiWeb's own listing only previews a handful of cards. The same page is in the repo as `georgian-essentials/preview.html` if you would rather open it locally.

## Русская версия

Та же колода с русскими подсказками и заметками: **`georgian-essentials/Georgian-Essentials-RU.apkg`** (колода «Грузинский - Самое нужное»), импорт через **Файл → Импорт**. Грузинский текст и озвучка те же. У неё свои ID колоды и заметок, поэтому она спокойно живёт рядом с английской в одной коллекции.

[Посмотреть все карточки в браузере](https://danilsk.github.io/georgian-anki-deck/georgian-essentials/preview.ru.html) — или локально: `georgian-essentials/preview.ru.html`.

## What the notes do

Most cards have no note, on purpose. A note is there only when it does one of three jobs:

- **Flags a trap** — `დავიკარგე` (I'm lost) vs `დავკარგე` (I lost it); `ნიგოზი` walnut / `თხილი` hazelnut / `მიწის თხილი` peanut; `ჩეკი` receipt vs `ანგარიში` bill.
- **States a reusable rule** — `-ით` = with, `უ-…-ოდ` = without, `[item] + გაქვთ?`, `[place] + სად არის?`.
- **Gives a register or reply form** — `გმადლობთ` for `მადლობა`, `გაგიმარჯოს` as the answer to `გამარჯობა`, informal singulars.

124 of the 360 practical notes carry one. The rest are blank so the card stays readable.

## Rebuild

```sh
uv run build-deck.py
```

Reads `practical.tsv` (Front / Back / Notes / Tags), `pronunciation.json` and `audio-manifest.json`, and writes the package, `cards.tsv`, `preview.html`, the card templates and `validation.json` into `georgian-essentials/`. The Russian deck is built in the same run from `practical.ru.tsv` and `pronunciation.ru.json`, into the same files with an `-RU` / `.ru` suffix and `templates/ru/`. `practical.ru.tsv` must keep the same rows, order, tags and Georgian text as `practical.tsv`; the build fails otherwise. It never touches a live Anki profile. Editing `practical.tsv` and rebuilding is the intended way to change the deck.

`prepare-audio.py` and `generate-practice.mjs` handle the audio side; `voice.md` records the TTS recipe. Regenerating audio needs an OpenRouter key in the environment and spends credits — the existing WAVs are committed, so a normal rebuild does not call any API.

## Audio

Generated with OpenRouter `google/gemini-3.1-flash-tts-preview`, voice Charon, wrapped as mono 24 kHz 16-bit WAV. A native speaker confirmed the clips sound very good, catching a couple of slips. The exact request for every clip is kept in `georgian-essentials/audio-prompts/`, without credentials.

## Caveat

Drafted for personal use and checked against the references listed in the deck README. The text has not had a native editor's full pass — corrections welcome.
