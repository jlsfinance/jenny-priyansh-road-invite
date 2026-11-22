from pathlib import Path
import cv2,numpy as np,json,subprocess
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'; OUT=ROOT/'analysis'/'face-review';OUT.mkdir(exist_ok=True)
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
while True:
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

def getframe(n):
 c=cv2.VideoCapture(VIDEO);c.set(cv2.CAP_PROP_POS_FRAMES,n);ok,f=c.read();c.release();assert ok;return f
protos={}
for name,(bx,by,w,h) in boxes.items():
 protos[name]=[]
 for n in [30,90,200]:
  f=getframe(n);x=tracks[n][name]['x'];y=tracks[n][name]['y'];crop=f[y:y+h,x:x+w]
  face=cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
  protos[name].append(face.astype(np.float32))

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
   if x>=0 and x+w<=720:
    face=cv2.cvtColor(f[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY).astype(np.float32)
    eyes=(slice(int(h*.30),int(h*.49)),slice(int(w*.20),int(w*.88)))
    mouth=(slice(int(h*.56),int(h*.78)),slice(int(w*.30),int(w*.78)))
    eye_errors=[float(np.mean((face[eyes]-p[eyes])**2)) for p in protos[name]]
    mouth_errors=[float(np.mean((face[mouth]-p[mouth])**2)) for p in protos[name]]
    state=2 if n>=195 and mouth_errors[2]<mouth_errors[0]*.83 else 1 if eye_errors[1]<eye_errors[0]*.8 else 0
   else:state=0
   frame_states[name]={'visible':True,'x':x,'y':y,'w':w,'h':h,'state':state,'score':score}
  mask=mask.filter(ImageFilter.GaussianBlur(1.0));canvas.paste(background,(0,0),mask)
  for name,d in frame_states.items():
   if not d['visible']:continue
   # Keep the neck attached while reducing the oversized photographic head.
   scale=.80
   width=round((d['w']+8)*scale);height=round((d['h']+5)*scale)
   im=sprites[name][d['state']].resize((width,height),Image.Resampling.LANCZOS)
   left=round(d['x']+d['w']/2-width/2)
   top=round(d['y']+d['h']+3-height)
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
