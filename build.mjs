import { readFile, writeFile } from 'node:fs/promises';
const root = new URL('./', import.meta.url);
const sources = {
  ROAD: ['palm-road.webp', 'image/webp'],
  CAR: ['red-car.png', 'image/png'],
  SERIF: ['serif.ttf', 'font/ttf'],
  SCRIPT: ['script.ttf', 'font/ttf'],
  GOOGLE400: ['google-sans-400.ttf', 'font/ttf'],
  GOOGLE500: ['google-sans-500.ttf', 'font/ttf'],
  AUDIO: ['reference-audio.mp3', 'audio/mpeg']
};
let html = await readFile(new URL('template.html', root), 'utf8');
for (const [token, [filename, mime]] of Object.entries(sources)) {
  const data = await readFile(new URL(`assets/${filename}`, root));
  html = html.replaceAll(`{{${token}}}`, `data:${mime};base64,${data.toString('base64')}`);
}
if (/\{\{[A-Z]+\}\}/.test(html)) throw new Error('Unresolved asset placeholders');
await writeFile(new URL('index.html', root), html);
console.log('Built self-contained index.html');
