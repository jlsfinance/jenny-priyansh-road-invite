from bisect import bisect_right
from pathlib import Path
import cv2,numpy as np,json,subprocess,sys
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'; OUT=ROOT/'analysis'/'face-review';OUT.mkdir(parents=True,exist_ok=True)
VIDEO=r'C:\Users\Admin\.codex\codex-remote-attachments\01a1f958-f61d-79e3-ad6f-412a6a0f06fe\4078B47B-C346-4CD7-BBC1-85DBF2880A4D\1-Video-24639.mp4'
FIT_REFERENCE=Path(r'C:\Users\Admin\.codex\codex-remote-attachments\01a1f958-f61d-79e3-ad6f-412a6a0f06fe\E1255FF7-43E7-4454-ACD5-E4D2D3BB7AC3\1-Photo-1.jpg')
sprites={name:[Image.open(ASSETS/f'{name}-{state}.png').convert('RGBA')
               for state in ('smile','wink','surprised')]
         for name in ('jenny','priyansh')}

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

# Compare the source expression area against the visually confirmed poses at
# frames 37, 45 and 201. Both characters switch together on these source frames.
smile_wink_frames=(22,32,43,54,64,75,86,97,108,118,129,140,151,162,172,183)
surprise_smile_frames=(196,206,216,225,234,243,252,262,270,280,289,299,
                       308,318,327,337,346,356,365,377,384,394,403,413)

def expression_at(frame):
 if frame < surprise_smile_frames[0]:
  return bisect_right(smile_wink_frames,frame)%2
 return 2 if bisect_right(surprise_smile_frames,frame)%2 else 0

background=Image.open(ROOT/'analysis'/'frame-0.png').convert('RGB')

# Build the full upper neckline as one plate, including both shoulder caps.
# Keep the original moving hand and cup above this plate as foreground.
fit_photo=Image.open(FIT_REFERENCE).convert('RGB')
neck_box=(193,704,363,779)
neckline=fit_photo.crop(neck_box)
neck_alpha=Image.new('L',neckline.size)
outline=[(253,705),(299,705),(306,718),(318,726),(333,725),
         (345,733),(353,752),(355,764),(347,774),(251,774),
         (245,757),(239,747),(223,738),(220,732),(243,728),(248,721)]
ImageDraw.Draw(neck_alpha).polygon([(x-neck_box[0],y-neck_box[1]) for x,y in outline],fill=255)
neck_fade=np.clip((neck_box[3]-1-np.arange(neck_box[1],neck_box[3]))/15,0,1)[:,None]
neckline.putalpha(Image.fromarray(np.round(np.asarray(neck_alpha.filter(ImageFilter.GaussianBlur(1.1)))*neck_fade).astype(np.uint8)))
neckline=neckline.resize((171,71),Image.Resampling.LANCZOS)

preview='--preview' in sys.argv
preview_frames={18,24,30,37,45,90,150,200,215,270,330,390,410}

cap=cv2.VideoCapture(VIDEO)
ff=None if preview else subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','720x800','-r','30','-i','-','-an','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(ASSETS/'personalized-couple.mp4')],stdin=subprocess.PIPE)
diagnostics=[];states=[]
try:
 for n,tr in enumerate(tracks):
  ok,f=cap.read();assert ok
  if preview and n not in preview_frames:continue
  canvas=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))
  original=canvas.copy()
  mask=Image.new('L',(720,1280));draw=ImageDraw.Draw(mask)
  frame_states={}
  for name,(bx,by,w,h) in boxes.items():
   x,y=tr[name]['x'],tr[name]['y'];score=tr[name]['score']
   if n<4 or score<.40:frame_states[name]={'visible':False};continue
   # Match the original head silhouette; replace the underlying pixels with its clean backdrop.
   poly=[(.16,.03),(.48,-.02),(.84,.02),(1.06,.23),(1.06,.86),(.75,.96),(.22,.96),(-.02,.84),(-.03,.29)] if name=='jenny' else [(.12,.02),(.49,-.02),(.9,.04),(1.03,.28),(1.01,.65),(.85,.81),(.61,.91),(.35,.91),(.04,.79),(-.03,.30)]
   draw.polygon([(int(x+px*w),int(y+py*h)) for px,py in poly],fill=255)
   if name=='jenny':
    draw.polygon([(x+18,y+222),(x+170,y+213),(x+183,y+242),(x+16,y+241)],fill=255)
   state=expression_at(n)
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
   height=round((d['h']+5)*(.50 if name=='jenny' else .64))
   width=round(height*source.width/source.height)
   im=source.resize((width,height),Image.Resampling.LANCZOS)
   # Align the chin to each costume's neckline, rather than to its hair bounds.
   neck_offset=5 if name=='jenny' else -9
   left=round(d['x']+d['w']/2-width/2+neck_offset)
   top=round(d['y']+d['h']-2-height)
   if name=='jenny':
    top-=13
    neck_left=round(left+width/2-85)
    neck_top=round(d['y']+d['h']-42)
    canvas.paste(neckline,(neck_left,neck_top),neckline)
    x,y=d['x'],d['y']
    foreground=Image.new('L',(720,1280))
    cup_and_hand=[(30,265),(34,249),(42,232),(49,228),(56,225),
                  (60,218),(64,217),(75,217),(75,234),(72,246),
                  (61,250),(55,256),(49,262)]
    ImageDraw.Draw(foreground).polygon([(x+px,y+py) for px,py in cup_and_hand],fill=255)
    canvas.paste(original,(0,0),foreground.filter(ImageFilter.GaussianBlur(.65)))
    # Fade only the very bottom of the sprite neck into the photographed collar.
    # The face, jaw and hair retain their original pixels above this narrow join.
    alpha=np.array(im.getchannel('A'),dtype=np.float32)
    rows=np.clip((np.arange(height)-(height-9))/8,0,1)[:,None]
    center=np.clip((.31-np.abs(np.arange(width)/width-.5))/.09,0,1)[None,:]
    im.putalpha(Image.fromarray(np.round(alpha*(1-rows*center)).astype(np.uint8)))
   canvas.paste(im,(left,top),im)
  states.append(frame_states)
  if n in preview_frames:
   canvas.save(OUT/f'face-frame-{n:03d}.jpg',quality=95)
   diagnostics.append(canvas.resize((180,320)))
  if ff:ff.stdin.write(canvas.crop((0,480,720,1280)).tobytes())
finally:
 cap.release()
 if ff:
  ff.stdin.close()
  if ff.wait():raise RuntimeError('Face animation encoding failed')
contact=Image.new('RGB',(180*4,350*((len(diagnostics)+3)//4)),'white')
for i,im in enumerate(diagnostics):contact.paste(im,((i%4)*180,(i//4)*350+25))
contact.save(OUT/'face-contact.jpg',quality=95)
if preview:sys.exit(0)
(ASSETS/'face-motion.json').write_text(json.dumps(states,separators=(',',':')),encoding='utf8')
print('Personalised all 420 frames with photo-based head variants; output:',ASSETS/'personalized-couple.mp4')
