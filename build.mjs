import {readFile,writeFile,readdir} from 'node:fs/promises';
const base=new URL('./',import.meta.url);let html=await readFile(new URL('template.html',base),'utf8');
const mimes={png:'image/png',jpg:'image/jpeg',webp:'image/webp',svg:'image/svg+xml',ttf:'font/ttf',mp3:'audio/mpeg',mp4:'video/mp4'};
for(const name of await readdir(new URL('assets/',base))){if(!html.includes(`assets/${name}`))continue;const mime=mimes[name.split('.').pop()];if(!mime)continue;const data=await readFile(new URL(`assets/${name}`,base));html=html.replaceAll(`assets/${name}`,`data:${mime};base64,${data.toString('base64')}`)}
if(/(?:src=|url\()\s*['"]assets\//.test(html))throw new Error('Missing asset');await writeFile(new URL('index.html',base),html);console.log('Built portable HTML: '+(html.length/1024/1024).toFixed(2)+' MB');
