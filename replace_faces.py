from pathlib import Path
import cv2,numpy as np,json,subprocess
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'; OUT=ROOT/'analysis'/'face-review';OUT.mkdir(parents=True,exist_ok=True)
VIDEO=r'C:\Users\Admin\.codex\codex-remote-attachments\01a1f958-f61d-79e3-ad6f-412a6a0f06fe\940C43EF-ADDE-4D5C-8B18-B4C2D68EDB5C\1-Video-24639.mp4'
SHEET=Path(r'C:\Users\Admin\.codex\generated_images\01a1f958-f61d-79e3-ad6f-412a6a0f06fe\exec-f94551c9-5ccc-4006-8e68-7b50d630d4fa.png')
sheet=Image.open(SHEET).convert('RGBA')
sprites={}
for row,name in enumerate(['jenny','priyansh']):
 cells=[sheet.crop((col*512,row*512,(col+1)*512,(row+1)*512)) for col in range(3)]
 bounds=[]
 for im in cells:
  alpha=im.getchannel('A').point(lambda x:0 if x<38 else min(255,round((x-38)*255/216)))
  im.putalpha(alpha);bounds.append(alpha.getbbox())
 box=(min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds))
 sprites[name]=[]
 for state,im in zip(['smile','wink','surprised'],cells):
  im=im.crop(box);im.save(ASSETS/f'{name}-{state}.png');sprites[name].append(im)

ref=cv2.imread(str(ROOT/'analysis'/'frame-12.png'))
boxes={'jenny':(94,548,190,244),'priyansh':(448,502,183,230)}
templates={name:cv2.cvtColor(ref[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY) for name,(x,y,w,h) in boxes.items()}
cap=cv2.VideoCapture(VIDEO);tracks=[];frame_id=0
tracking_cache=OUT/'tracking-raw.json'
if tracking_cache.exists():tracks=json.loads(tracking_cache.read_text(encoding='utf8'))
while True:
 if len(tracks)==420:break
 ok,frame=cap.read()
 if not ok:break
 gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
 band=cv2.copyMakeBorder(gray[450:835],0,0,200,200,cv2.BORDER_CONSTANT,value=242)
 item={}
 for name,tpl in templates.items():
  result=cv2.matchTemplate(band,tpl,cv2.TM_CCOEFF_NORMED);_,score,_,pos=cv2.minMaxLoc(result)
  item[name]={'x':pos[0]-200,'y':pos[1]+450,'score':round(score,3)}
 tracks.append(item);frame_id+=1
cap.release()
for n in range(4,14):
 tracks[n]['jenny']={'x':round(-182+(n-4)*16.9),'y':548,'score':1.0}
 tracks[n]['priyansh']={'x':round(694-(n-4)*14.9),'y':502,'score':1.0}
# Early entrance contains partial/overlapping heads. Restrict each identity to its source side
# until it becomes trackable, then preserve the observed slide overshoot.
print('Entrance tracking:',json.dumps([{'f':i,**tracks[i]} for i in range(0,24,2)]),flush=True)
(OUT/'tracking-raw.json').write_text(json.dumps(tracks),encoding='utf8')

# Explicit beats avoid the old classifier holding surprise for the last 7.5s.
expression_beats={
 'jenny':[(0,0),(1.1,1),(1.5,0),(2.5,2),(3.3,0),(4.4,1),(4.8,0),(5.7,2),(6.6,0),(7.8,1),(8.2,2),(9.1,0),(10.2,1),(10.6,0),(11.7,2),(12.6,0),(13.3,2)],
 'priyansh':[(0,0),(1.7,1),(2.1,0),(3.1,2),(3.9,0),(5.0,1),(5.4,0),(6.3,2),(7.1,0),(8.4,1),(8.8,0),(9.5,2),(10.3,0),(11.1,1),(11.5,0),(12.1,2),(12.8,0)]
}
def expression_at(name,t):
 return next(state for start,state in reversed(expression_beats[name]) if t>=start)

background=Image.open(ROOT/'analysis'/'frame-0.png').convert('RGB')
cap=cv2.VideoCapture(VIDEO)
ff=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','720x800','-r','30','-i','-','-an','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(ASSETS/'personalized-couple.mp4')],stdin=subprocess.PIPE)
diagnostics=[];states=[]
try:
 for n,tr in enumerate(tracks):
  ok,f=cap.read();assert ok
  canvas=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))
  mask=Image.new('L',(720,1280));draw=ImageDraw.Draw(mask)
  frame_states={}
  for name,(bx,by,w,h) in boxes.items():
   x,y=tr[name]['x'],tr[name]['y'];score=tr[name]['score']
   if n<4 or score<.40:frame_states[name]={'visible':False};continue
   # Match the original head silhouette; replace the underlying pixels with its clean backdrop.
   poly=[(.16,.03),(.48,-.02),(.84,.02),(1.06,.23),(1.06,.86),(.75,.96),(.22,.96),(-.02,.84),(-.03,.29)] if name=='jenny' else [(.12,.02),(.49,-.02),(.9,.04),(1.03,.28),(1.01,.65),(.85,.81),(.61,.91),(.35,.91),(.04,.79),(-.03,.30)]
   draw.polygon([(int(x+px*w),int(y+py*h)) for px,py in poly],fill=255)
   state=expression_at(name,n/30)
   frame_states[name]={'visible':True,'x':x,'y':y,'w':w,'h':h,'state':state,'score':score}
  mask=mask.filter(ImageFilter.GaussianBlur(1.0));canvas.paste(background,(0,0),mask)
  for name,d in frame_states.items():
   if not d['visible']:continue
   # Keep the neck attached while reducing the oversized photographic head.
   source=sprites[name][d['state']]
   # Trim transparent margins per expression and preserve natural head proportions.
   alpha=np.asarray(source.getchannel('A'))>160
   ys=np.flatnonzero(alpha.sum(axis=1)>12);xs=np.flatnonzero(alpha.sum(axis=0)>12)
   source=source.crop((int(xs[0]),int(ys[0]),int(xs[-1])+1,int(ys[-1])+1))
   height=round((d['h']+5)*(.60 if name=='jenny' else .64))
   width=round(height*source.width/source.height)
   im=source.resize((width,height),Image.Resampling.LANCZOS)
   # Align the chin to each costume's neckline, rather than to its hair bounds.
   neck_offset=5 if name=='jenny' else -9
   left=round(d['x']+d['w']/2-width/2+neck_offset)
   top=round(d['y']+d['h']-2-height)
   canvas.paste(im,(left,top),im)
  states.append(frame_states)
  if n in [6,9,12,18,30,90,150,200,225,270,330,390]:
   canvas.save(OUT/f'face-frame-{n:03d}.jpg',quality=95)
   diagnostics.append(canvas.resize((180,320)))
  ff.stdin.write(canvas.crop((0,480,720,1280)).tobytes())
finally:
 cap.release();ff.stdin.close();rc=ff.wait()
 if rc:raise RuntimeError('Face animation encoding failed')
contact=Image.new('RGB',(180*4,350*3),'white');d=ImageDraw.Draw(contact)
for i,im in enumerate(diagnostics):contact.paste(im,((i%4)*180,(i//4)*350+25))
contact.save(OUT/'face-contact.jpg',quality=95)
(ASSETS/'face-motion.json').write_text(json.dumps(states,separators=(',',':')),encoding='utf8')
print('Personalised all 420 frames with photo-based head variants; output:',ASSETS/'personalized-couple.mp4')
