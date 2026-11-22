"""Check rendered face changes, not just the scheduled state labels."""
from pathlib import Path
import cv2,json,numpy as np
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
tracks=json.loads((root/'assets/face-motion.json').read_text())
cap=cv2.VideoCapture(str(root/'assets/personalized-couple.mp4'))
samples={'jenny':[37,45,201],'priyansh':[37,45,201]}
contact=Image.new('RGB',(360,340),'#f5f0e5');draw=ImageDraw.Draw(contact)
report={}
for row,(name,frames) in enumerate(samples.items()):
 crops=[];neck_samples=[]
 for col,n in enumerate(frames):
  cap.set(cv2.CAP_PROP_POS_FRAMES,n);ok,frame=cap.read();assert ok
  tr=tracks[n][name];x,y=tr['x'],tr['y']-480
  if name=='jenny':
   crop=frame[y+80:y+250,x+30:x+160]
   b,g,r=map(int,frame[y+226,x+100]);neck_samples.append([r,g,b])
   assert r>g+15 and g>b+10 and r<235,('Jenny neck missing',n,[r,g,b])
  else:crop=frame[y+70:y+220,x+25:x+155]
  crop=cv2.resize(crop,(110,140));crops.append(crop.astype(float))
  contact.paste(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),(col*120,row*170+25))
  draw.text((col*120+4,row*170+4),f'{name} {n/30:.1f}s',fill='#503a2c')
 differences=[float(np.abs(crops[a]-crops[b]).mean()) for a,b in [(0,1),(0,2),(1,2)]]
 assert min(differences)>4,(name,'Rendered face did not change',differences)
 states=[t[name].get('state') for t in tracks[24:]]
 transitions=sum(a!=b for a,b in zip(states,states[1:]))
 assert transitions>=12,(name,'Expressions stopped changing')
 report[name]={'actualPixelDifferences':differences,'expressionTransitions':transitions,'visibleNeckSamples':neck_samples}
cap.release()
contact.save(root/'verification/face-expressions.jpg',quality=95)
(root/'verification/face-checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
