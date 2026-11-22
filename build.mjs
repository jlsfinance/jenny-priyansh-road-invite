import {readFile,writeFile,readdir} from 'node:fs/promises';
const base=new URL('./',import.meta.url);
let html=await readFile(new URL('template.html',base),'utf8');
const mimes={png:'image/png',webp:'image/webp',svg:'image/svg+xml',ttf:'font/ttf',mp3:'audio/mpeg'};
for(const name of await readdir(new URL('assets/',base))){
 if(!html.includes(`assets/${name}`))continue;
 const ext=name.split('.').pop(),mime=mimes[ext];if(!mime)continue;
 const buffer=await readFile(new URL(`assets/${name}`,base));
 html=html.replaceAll(`assets/${name}`,`data:${mime};base64,${buffer.toString('base64')}`);
}
if(/(?:src=|url\()\s*['"]assets\//.test(html))throw new Error('Unembedded asset');
await writeFile(new URL('index.html',base),html);
console.log('Built portable HTML invitation ('+(html.length/1024/1024).toFixed(2)+' MB)');
