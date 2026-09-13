import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const source = process.argv.includes('--all') ? 'audio-manifest.json' : 'pronunciation.json';
const data = JSON.parse(await fs.readFile(path.join(root, source), 'utf8'));
const clips = Array.isArray(data) ? data : data.clips;
const media = path.join(root, 'georgian-essentials', 'media');
const prompts = path.join(root, 'georgian-essentials', 'audio-prompts');
await fs.mkdir(media, { recursive: true });
await fs.mkdir(prompts, { recursive: true });
const guidance = 'Speak as a native Georgian speaker from Tbilisi, Georgia (the country), reading standard Georgian naturally and clearly. Preserve Georgian ejective consonants პ, ტ, წ, ყ and distinguish them from aspirated ფ, თ, ც. Use Georgian vowels and a Georgian tapped/trilled რ. Read only the sentence below, exactly once, without a preamble, translation, or commentary.';
const model = 'google/gemini-3.1-flash-tts-preview';
const voice = 'Charon';

async function exists(filename) {
  try { await fs.access(filename); return true; }
  catch (e) { if (e.code === 'ENOENT') return false; throw e; }
}

function wav(pcm) {
  if (!pcm.length || pcm.length % 2) throw new Error('Invalid 16-bit PCM length');
  if (pcm.subarray(0, 4).toString() === 'RIFF') throw new Error('Expected raw PCM, received WAV');
  const header = Buffer.alloc(44);
  header.write('RIFF', 0); header.writeUInt32LE(36 + pcm.length, 4);
  header.write('WAVEfmt ', 8); header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20); header.writeUInt16LE(1, 22);
  header.writeUInt32LE(24000, 24); header.writeUInt32LE(48000, 28);
  header.writeUInt16LE(2, 32); header.writeUInt16LE(16, 34);
  header.write('data', 36); header.writeUInt32LE(pcm.length, 40);
  return Buffer.concat([header, pcm]);
}

async function generate(clip) {
  const name = `ge_essentials_${clip.id}.wav`;
  const out = path.join(media, name);
  const metadata = path.join(prompts, `${clip.id}.json`);
  const request = { model, voice, input: `${guidance} ${clip.extra}\n\n${clip.text}`, response_format: 'pcm' };
  if (await exists(out)) {
    if (!(await exists(metadata))) throw new Error(`${name}: missing retained prompt`);
    const saved = JSON.parse(await fs.readFile(metadata, 'utf8'));
    if (JSON.stringify(saved.request) !== JSON.stringify(request)) throw new Error(`${name}: prompt changed; use a new clip ID`);
    console.log(`Preserved ${name}`); return;
  }
  const key = process.env.OPENROUTER_API_KEY;
  if (!key) throw new Error('OPENROUTER_API_KEY is missing; load it from the secret environment');
  const response = await fetch('https://openrouter.ai/api/v1/audio/speech', {
    method: 'POST', headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(request), signal: AbortSignal.timeout(180000),
  });
  const contentType = response.headers.get('content-type') || '';
  if (!response.ok) throw new Error(`${name}: HTTP ${response.status} (response body omitted)`);
  if (!contentType.toLowerCase().startsWith('audio/')) throw new Error(`${name}: unexpected content type ${contentType}`);
  const pcm = Buffer.from(await response.arrayBuffer());
  const seconds = pcm.length / 48000;
  if (seconds < 0.4 || seconds > 25) throw new Error(`${name}: unexpected duration ${seconds.toFixed(2)}s`);
  const metadataContent = JSON.stringify({ request, text: clip.text, contentType, seconds, generatedAt: new Date().toISOString(), quality: 'Synthetic speech; not certified by a native listener.' }, null, 2) + '\n';
  if (await exists(metadata)) {
    const saved = JSON.parse(await fs.readFile(metadata, 'utf8'));
    if (JSON.stringify(saved.request) !== JSON.stringify(request)) throw new Error(`${name}: retained prompt differs`);
  } else {
    await fs.writeFile(metadata, metadataContent, { flag: 'wx' });
  }
  await fs.writeFile(out, wav(pcm), { flag: 'wx' });
  console.log(`Generated ${name}: ${seconds.toFixed(2)}s`);
}

// Four requests at a time; preserve completed clips on reruns. No hidden retries.
let failed = false;
for (let i = 0; i < clips.length; i += 4) {
  const results = await Promise.allSettled(clips.slice(i, i + 4).map(generate));
  for (const result of results) if (result.status === 'rejected') {
    console.error(result.reason.message); failed = true;
  }
  if (failed) break;
}
if (failed) process.exitCode = 1;
