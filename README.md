# Jenny & Priyansh — animated invitation

Open `index.html` in a browser. It is a self-contained, 14-second portrait invitation with playback, seeking and optional music. Rebuild with `node build.mjs` after editing `template.html` or the assets.

Personalization: Jenny & Priyansh, authentic JP floral crest, 16 February 2026, Arawali Ananta Elite · Ranakpur. Heads preserve their natural aspect ratios and are trimmed per expression, fitted to each costume's collar using the user's Photo 1 alignment reference. Mobile layout fits the current viewport height and safe areas, with aligned playback controls. Cartoon bodies, entrances, heart burst and birds retain motion extracted from the supplied reference.

Expressions follow explicit, independent smile/wink/surprise beats throughout the 14 seconds. This replaces a pixel classifier that previously held the surprised expression for the final 7.5 seconds. Playback loops automatically. Body motion is from the reference; facial expression timing is reconstructed.

Jenny's head was reduced a further 17% after the photo comparison, to approximately 100 × 125 pixels on the 720-pixel-wide canvas, with its lower edge fixed at the neckline. Priyansh's dimensions remain unchanged in this adjustment.

The reference was examined at all 420 frames (720 × 1280, 30 fps). Source sheets and analysis remain in the local analysis folder. Browser verification checks eight animation times, continuous playback, names/date/logo/fonts, replay, music control and mobile overflow.

## Face asset provenance

Identity references were the user's `jenny-priyansh-standing-portrait.jpg` and `jenny-priyansh-restaurant.jpg` from the existing invitation assets. Six transparent photographic head variants were produced with image generation: Jenny and Priyansh, each smiling, winking and surprised. These are AI-assisted identity-based expression variants, rather than untouched photograph crops.

Generation brief: use the two supplied couple photographs as identity references; create a transparent 3-column, 2-row sprite sheet of heads only; Jenny on the top row and Priyansh on the bottom; smiling, winking and surprised expressions; retain their facial identity, natural hair and Priyansh's beard; no bodies, text or decorations. Saved variants are `assets/jenny-{smile,wink,surprised}.png` and `assets/priyansh-{smile,wink,surprised}.png`.

`replace_faces.py` records the local reference and generated sheet paths, tracks the reference heads, restores the background beneath them and composites expression variants into the original body animation. It requires the original local inputs, Python, Pillow, OpenCV, NumPy and FFmpeg.

The supplied reference's paper illustration, costume/body artwork, bird/heart animation and music are reused. Their original authorship and music source were not identified by visual analysis.
