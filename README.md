# Jenny & Priyansh — animated invitation

Open `index.html` in a browser for the self-contained invitation with playback, seeking and optional music. `jenny-priyansh.mp4` is the 14-second, 720 × 1280 shareable export with music. Rebuild the HTML with `node build.mjs` after editing `template.html` or its assets.

Personalization: Jenny & Priyansh, authentic JP floral crest, 16 February 2026, Arawali Ananta Elite · Ranakpur. Heads preserve their natural aspect ratios and are trimmed per expression, fitted to each costume's collar using the user's Photo 1 alignment reference. Mobile layout fits the current viewport height and safe areas, with aligned playback controls. Cartoon bodies, entrances, heart burst and birds retain motion extracted from the supplied reference.

Both characters use the expression changes measured from the reference frames. Before 6.53 seconds they alternate smile and wink. From frame 196 they alternate surprise and smile. Playback loops automatically.

Jenny's existing face cuts are approximately 100 × 125 pixels on the 720-pixel-wide canvas. The full shoulder and neckline plate comes from the supplied Photo 1 alignment reference. The coffee cup and the hand holding it are restored above that plate, so they keep the source motion. The bag, other arm, jeans and shoes retain the reference footage.

The reference was examined at all 420 frames (720 × 1280, 30 fps). Source sheets and analysis remain in the local analysis folder. Browser verification checks eight animation times, continuous playback, names/date/logo/fonts, replay, music control and mobile overflow.

The REA Video review found one continuous composition. The couple enters from both sides in the opening second. The two announcement lines type on from 2 to 5.2 seconds. The heart grows and bursts from about 6.3 to 8.6 seconds. The birds and date reveal follow the burst, and the date settles in the final seconds.

## Face asset provenance

Identity references were the user's `jenny-priyansh-standing-portrait.jpg` and `jenny-priyansh-restaurant.jpg` from the existing invitation assets. Six transparent photographic head variants were produced with image generation: Jenny and Priyansh, each smiling, winking and surprised. These are AI-assisted identity-based expression variants, rather than untouched photograph crops.

Generation brief: use the two supplied couple photographs as identity references; create a transparent 3-column, 2-row sprite sheet of heads only; Jenny on the top row and Priyansh on the bottom; smiling, winking and surprised expressions; retain their facial identity, natural hair and Priyansh's beard; no bodies, text or decorations. Saved variants are `assets/jenny-{smile,wink,surprised}.png` and `assets/priyansh-{smile,wink,surprised}.png`.

`replace_faces.py` reads the committed expression cutouts and the local reference inputs, tracks the reference heads, and composites the existing cutouts onto the original body animation. It requires Python, Pillow, OpenCV, NumPy and FFmpeg. Run it with `--preview` to inspect individual frames before encoding.

The supplied reference's paper illustration, costume/body artwork, bird/heart animation and music are reused. Their original authorship and music source were not identified by visual analysis.
