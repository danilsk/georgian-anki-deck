# Georgian - Essentials

396 cards from 378 notes: 360 practical cards, 18 read-aloud pronunciation cards, and 18 listening cards. Every Georgian target has audio: 373 unique recordings, with identical phrases sharing a clip. Georgian script only; no transliteration. English prompts; notes only where they earn their place. No grammar instruction: phrases are learned whole, not built from case tables or verb paradigms.

## Import into Anki

Use **File → Import** and select **Georgian-Essentials.apkg**. The package contains the note type, card layouts and all 373 audio files. No manual media copying is needed. It adds a deck; it is not a replacement collection. If you imported the earlier version, import this APKG with note updates enabled: existing note identities and the four-field note type are preserved, so your review history survives and the deck is renamed in place rather than duplicated.

`cards.tsv` is the editable alternative, not an additional deck to import after the package. Its columns are **Front | Back | Notes | Audio | Tags**, separated by tabs. The third column holds notes and is deliberately empty on most cards. It is UTF-8, with Anki import headers and HTML enabled.

Practical recordings are embedded as `[sound:filename.wav]` in the field containing the Georgian target: Back for English prompts, Front for recognition cards. The separate Audio column remains reserved for the pronunciation exercises and their listening cards. Each new practical note adds one card. Explanatory examples in Notes are not separately narrated. Use the APKG to update an earlier import: recognition Front fields now include audio, which changes TSV first-field matching.

For a TSV-only import:

1. Clone the Basic note type and name it `Georgian Essentials — Practical + Listening`. Use four fields, in order: `Front`, `Back`, `Notes`, `Audio`.
2. In Cards, use `templates/1-front.html` and `templates/1-back.html` for the first card, and `templates/style.css` for Styling. Optionally add a second card using `templates/2-front.html` and `templates/2-back.html`; its Audio condition creates listening cards only for the 18 pronunciation notes. Without the second template you get 378 cards.
3. Copy the WAV files **inside** `media/` directly into your Anki profile's `collection.media` folder. Do not copy the enclosing folder.
4. Import `cards.tsv`, select that note type and your destination deck, enable HTML, and confirm columns 1–4 map to the four fields and column 5 maps to Tags. Preview the Georgian before importing.

These file headers, field mappings and media references follow the [Anki text import manual](https://docs.ankiweb.net/importing/text-files.html).

## How to study

For ordinary English prompts, say the Georgian answer aloud before revealing it and its recording. Cards beginning “You hear” or “Read the sign” show and play the Georgian phrase on the front. Automatic playback depends on your Anki audio settings; replay controls are also available.

For “Read aloud” cards, pronounce the Georgian before revealing the answer and audio. For “Listen and repeat” cards, listen without seeing the text, repeat what you hear, then reveal the phrase and its meaning. If useful, say what each word means as well.

Start with `tag:core` and add the other topics gradually. The file/package puts core notes first; Anki's new-card settings control whether that order is used. Topic tags: `courtesy`, `shopping`, `restaurant`, `food`, `transport`, `numbers`, `basics`, `help`, `pronunciation`, `clarification`, `time`, `accommodation`, `social`, `boundaries`, `replies`. Additional tags: `recognition`, `audio`.

The 92 new cards are tagged `expansion`. They cover correcting misunderstandings, food restrictions, urgent requests, weekdays and scheduling, accommodation problems, transport mix-ups, social exchanges, boundaries and common replies. Search `tag:expansion` in Anki's browser to see just these additions. Allergy cards describe specific allergies, not preferences; learn the ones that actually apply to you.

Open `preview.html` in a browser to search and review the notes or play any target's recording before importing. Keep it beside the `media` folder. It is also published at <https://danilsk.github.io/georgian-anki-deck/>.

## Pronunciation focus

The five pairs are **ფ/პ, თ/ტ, ქ/კ, ც/წ, ჩ/ჭ**. The first member is aspirated (released with a puff of breath); the second is ejective (a brief closure in the throat helps create a compact release). Ejectives are a different articulation, not simply louder versions of the first sound. Natural Georgian ejectives need not be exaggerated. ფ is not English f, and თ is not English th.

The deck also practices ყ, the difference between ღ and ხ, and clusters in useful phrases such as წყალი, თუ შეიძლება and ქართულს ვსწავლობ. The frog sentence is a traditional tongue twister. The shorter food and number drills are deliberately simple articulation exercises, not presented as traditional sayings. Rare words such as scythe and affliction appear only to make genuine sound contrasts.

All clips use the exact base guidance from the supplied `../voice.md`, Gemini `google/gemini-3.1-flash-tts-preview`, and Charon. Pronunciation exercises add a contrast-specific instruction; practical targets add guidance covering კ/ქ and ჭ/ჩ and request the word or phrase once. The original 18 clips are preserved. PCM is wrapped as mono, 24 kHz, 16-bit WAV. Exact requests are retained in `audio-prompts/`, with no credentials.

The recordings were generated with Google's `gemini-3.1-flash-tts-preview` (Charon voice) and checked for format, non-silent signal and complete packaging. A native speaker confirmed they sound very good, catching a couple of slips. A [recording of the frog sentence](https://forvo.com/word/ბაყაყი_წყალში_ყიყინებს_лягушка_в_воде_квакает/) is linked for comparison; it is not copied into the deck.

## Language and source notes

This is a curated practical deck, not a verbatim phrasebook export or a complete Georgian course. It teaches no grammar: notes point out only the patterns worth reusing. Phrases generally use polite/plural forms with strangers. A note appears only where it does one of three jobs: flags a trap (minimal pairs such as ნიგოზი/თხილი or დავკარგე/დავიკარგე), states a reusable rule (-ით for with, უ-…-ოდ for without, [item] + გაქვთ?), or gives a register or reply form that changes what you would actually say. 124 of the 360 practical notes carry one; the rest are blank on purpose. The meanings and notes were drafted for this deck and selected details were checked against the references below. The text has not had a native editor's full pass.

- [Peace Corps Georgian language guide](https://files.peacecorps.gov/multimedia/audio/languagelessons/georgia/GE_Georgian_Language_Lessons.pdf): reference for basic language and number construction.
- [Georgian numerals](https://en.wikipedia.org/wiki/Georgian_numerals) and [NPLG's numeral entry](https://www.nplg.gov.ge/wikidict/index.php/რიცხვითი_სახელი): reference checks for twenties, teens and compound-number structure. Standard 18 is თვრამეტი; 2,000 is ორი ათასი.
- [Georgian alphabet lesson 4](https://www.georgian-alphabet.com/en/lesson4.php) and [lesson 5](https://www.georgian-alphabet.com/en/lesson5.php): aspirated and ejective distinctions, with audio.
- [International Journal of Multilingual Education paper](https://multilingualeducation.openjournals.ge/index.php/ijml/article/download/6551/6551/10865): examples of contrasts including თარო/ტარო, ქარი/კარი, ცელი/წელი and ჭირი/ჩირი.
- [Georgian learning exercises](https://ena.ge/elearning/5/________oxu__yaz.html): native-script contrast practice.
- [Georgian conversation book](https://gruzinskij.ru/wp-content/uploads/2011/12/vaxtangashvili_razgovornik.pdf): check for the restaurant question აქ მიირთმევთ თუ წაიღებთ?
- [NPLG Georgian–English conversation guide: visiting a doctor](https://www.nplg.gov.ge/saskolo/index.php?a=term&d=24&t=58): checks for requesting an ambulance and recognizing სად გტკივათ?
- [Ilia State University international student guide](https://www.timeshighereducation.com/cms-academic/sites/default/files/institution_downloads/2026-01/2024%20-%20International%20Student%20Guide%20%28web%29.pdf): checks for polite introductions and urgent requests.
- [Magticom's Georgian-language examples](https://www.magticom.ge/ka/useful-info/fraud-prevention/fraud-types): attestation of ტელეფონი დამიჯდა for a phone with a flat battery.
- [Wikivoyage Georgian phrasebook](https://en.wikivoyage.org/wiki/Georgian_phrasebook): secondary cross-check of everyday vocabulary; not treated as authoritative for spelling or pronunciation.
- [OpenRouter speech documentation](https://openrouter.ai/docs/guides/overview/multimodal/tts) and [genanki](https://github.com/kerrickstaley/genanki): audio request and deck packaging references.

## Rebuild or edit

The parent directory contains `practical.tsv` (four source columns: Front, Back, Notes, Tags), `pronunciation.json`, `prepare-audio.py`, `audio-manifest.json`, `generate-practice.mjs` and `build-deck.py`.

After editing source files, run `uv run prepare-audio.py` to refresh the deduplicated audio manifest. Generate any missing clips, then run `uv run build-deck.py` from the parent directory. This rebuilds the APKG, final five-column TSV, preview, templates and `validation.json`. It does not open or modify your Anki profile. Stable IDs use the original text prompt, excluding embedded audio, so this audio upgrade retains existing note identities. Changing the text of a front gives the note a new identity.

To generate missing audio, load `OPENROUTER_API_KEY` into the environment as described in `voice.md`, then run `node generate-practice.mjs --all`. This spends OpenRouter credits. Existing clips are preserved; a changed text gets a new content-derived ID. If changing generation guidance, use new IDs as well. Without `--all`, only the original pronunciation set is processed. Audio generation is not part of the normal deck rebuild.
