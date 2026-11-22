const {chromium}=require('C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const page=await browser.newPage({viewport:{width:720,height:1280},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));const url=pathToFileURL(path.join(__dirname,'index.html')).href;
 await page.goto(url+'?render=1',{timeout:60000});await page.evaluate(()=>document.fonts.ready);
 await page.waitForFunction(()=>[...document.querySelectorAll('video')].every(v=>v.readyState>=2),{timeout:30000});
 const frames=[];
 for(const t of [.2,.6,3.7,5.5,6.8,8.35,10.6,12.8]){await page.evaluate(t=>__seekTo(t),t);await page.waitForTimeout(100);await page.screenshot({path:path.join(__dirname,'verification',`frame-${t}.png`)});const state=await page.locator('#couple').evaluate(v=>({time:v.currentTime,ready:v.readyState}));if(Math.abs(state.time-t)>.05)throw new Error('Body/face motion not aligned');frames.push({t,...state})}
 const info=await page.evaluate(()=>({details:__invite.details,duration:__getDuration(),title:document.title,finalDay:document.getElementById('day').textContent,finalMonth:document.getElementById('month').textContent,crestLoaded:document.getElementById('crest').complete&&document.getElementById('crest').naturalWidth>0,fonts:document.fonts.check('72px Invitation')&&document.fonts.check('76px Signature')}));
 await page.evaluate(()=>__seekTo(7.1));await page.evaluate(()=>__invite.play());await page.waitForTimeout(600);const moving=await page.locator('#couple').evaluate(v=>({time:v.currentTime,playing:!v.paused}));await page.evaluate(()=>__invite.pause());if(!moving.playing||moving.time<7.6)throw new Error('Animation is static');
 await page.setViewportSize({width:390,height:844});await page.goto(url,{timeout:60000});await page.evaluate(()=>document.fonts.ready);await page.evaluate(()=>__seekTo(12.8));await page.waitForTimeout(100);await page.screenshot({path:path.join(__dirname,'verification','mobile.png')});const mobile=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth}));
 await page.locator('#replay').click();await page.waitForTimeout(200);await page.locator('#play').click();const replay=Number(await page.locator('#progress').inputValue())<1;await page.locator('#sound').click();const music=await page.locator('#sound').getAttribute('aria-label');
 const report={info,frames,moving,mobile,replay,music,errors};fs.writeFileSync(path.join(__dirname,'verification','checks.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();if(errors.length||mobile.overflow||!replay||info.finalDay!=='16'||info.finalMonth!=='FEBRUARY 2026'||!info.crestLoaded||!info.fonts)process.exit(1);
})();
