# Georgian speech with Gemini

Configuration tested in this project on 2026-09-07. The user found the initial plain-text/Iapetus samples American-accented. Switching to **Charon plus explicit Georgian pronunciation guidance** produced speech they considered good enough, though imperfect. This is a working recipe, not a guarantee of native pronunciation; voice and prompt were changed together.

## Model and request

- OpenRouter model: `google/gemini-3.1-flash-tts-preview`
- Voice: `Charon` (preserve capitalization)
- Endpoint: `POST https://openrouter.ai/api/v1/audio/speech`
- Headers: `Authorization: Bearer <OPENROUTER_API_KEY>` and `Content-Type: application/json`
- Body: `{ "model": "google/gemini-3.1-flash-tts-preview", "voice": "Charon", "input": "<guidance>\n\n<Georgian text>", "response_format": "pcm" }`

This uses paid OpenRouter credits. Read the key from the environment; never embed or print it. Load it from wherever you keep local secrets, e.g. `set -a; . ~/.zsh_secrets; set +a`.

## Exact pronunciation guidance

Put this guidance at the beginning of `input`, followed by a blank line and the target text in **Georgian script**:

```text
Speak as a native Georgian speaker from Tbilisi, Georgia (the country), reading standard Georgian naturally and clearly. Preserve Georgian ejective consonants პ, ტ, წ, ყ and distinguish them from aspirated ფ, თ, ც. Use Georgian vowels and a Georgian tapped/trilled რ. Read only the sentence below, exactly once, without a preamble, translation, or commentary.
```

Example target: `ბაყაყი წყალში ყიყინებს.` (“The frog croaks in water.”) Send only the Georgian target after the guidance; keep translations and transliterations out of the spoken text.

For a specific contrast, append a short instruction to the guidance. Example:

```text
Preserve the word-initial contrast: ფური begins with aspirated [pʰ], while პური begins with ejective [pʼ]. The letter ფ is an aspirated stop, not the English f sound. Read the complete Georgian phrase naturally, exactly once.
```

Use real word pairs when the user asks for pronunciation contrasts:

| Contrast | Target phrase | Meaning |
| --- | --- | --- |
| p / p’ | ფური და პური. | Cow and bread |
| t / t’ | თარო და ტარო. | Shelf and corn cob |
| ts / ts’ | ცელი და წელი. | Scythe and year |
| k’ / k | კაცი და ქალი. | Man and woman (also differs beyond the initial consonant) |

## Save and check the audio

The tested Gemini endpoint **rejects `response_format: "mp3"`**. Request `pcm`; the response is raw signed 16-bit little-endian, mono, 24,000 Hz audio. Wrap it in a WAV header with those settings to produce a playable `.wav`; simply renaming raw PCM is insufficient.

Check HTTP success and the audio content type before saving. Generate one clip per phrase, preserve existing files, and retain the exact prompt with each output. `afinfo <file.wav>` on macOS checks format and duration, not pronunciation. Listen for the intended words and consonant contrasts; ask for listener feedback before describing the accent as correct.

The local [generate-practice.mjs](generate-practice.mjs) contains a working Node implementation, including PCM-to-WAV wrapping. Run it with `node generate-practice.mjs` after loading the key. It generates missing clips from its sample list and preserves existing ones; use new IDs when changing text or prompts.

References: [OpenRouter model](https://openrouter.ai/google/gemini-3.1-flash-tts-preview), [OpenRouter speech endpoint](https://openrouter.ai/docs/guides/overview/multimodal/tts), [Google speech generation](https://ai.google.dev/gemini-api/docs/speech-generation).
