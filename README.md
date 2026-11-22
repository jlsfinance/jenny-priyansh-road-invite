# Jenny & Priyansh — Two States, One Forever

Open **index.html** in Chrome or Edge. It contains all artwork, fonts, state outlines and music in one file and works offline. Tap the speaker to enable music. The five chapter buttons jump directly to each part.

## Personal details

- Jenny: **Rajasthan** — the upper palace section in the opening.
- Priyansh: **Gujarat** — the lower temple section in the opening.
- Wedding: **16 February 2026**, Arawali Ananta Elite, Ranakpur, Rajasthan.
- Barat Swagat: 16 February, 6–7 pm; Shubh Phere: 16 February, 11 pm.
- Sangeet: **15 February 2026, 7 pm onwards**, at the same venue.

The dates, venue and event times come from the earlier Jenny–Priyansh invitation in this workspace, with the wedding date changed to the user's latest instruction. No surnames or family details were invented.

## Reference and recreation

rea-video survey, decompose, review and apply-review were run on Video-8684.mp4. The visible video lasts **1223 frames / 24 fps = 50.958 seconds**, in a 720×1280 portrait frame. The tool splits it into seven segments, including a two-frame black leader and smoke transition; the visual design has five substantive scenes:

| Time | Scene | Personalisation |
|---|---|---|
| 0–9.5 s | Watercolor regional opening | Rajasthan/Jenny above; Gujarat/Priyansh below |
| 9.5–22.7 s | Floral monogram and names | JP, Jenny & Priyansh |
| 22.7–32.3 s | Pink lotus wedding card | 16 February, Barat Swagat, Phere, Ranakpur venue |
| 32.3–42 s | Black-gold sangeet card | 15 February, 7 pm, Ranakpur venue |
| 42–51 s | Blue closing with lanterns and fireworks | JP and Jenny & Priyansh |

The recreation uses separate cropped illustration assets, editable HTML text, the existing floral JP mark and sprigs from this repository's `logo` branch, and deterministic canvas effects. The logo is toned to sage/ivory on the watercolor scene and warm ivory/gold on the blue closing, with animated sprig growth. It does not play the original full-frame video under replacement text. The reference's illustrated people remain decorative illustrations and are not photos of Jenny and Priyansh. Typography, watercolor transitions, sparks and fireworks are approximations of the reference, not a claim that its exact source fonts or animation project were recovered.

The classifier's AI provenance guesses are uncertain: the visual review supports a composited motion invitation, but cannot establish how individual illustrations were created. The original supplied soundtrack is preserved; no claim is made about its source. Audio separation, OCR and automatic packaging detection were skipped because the soundtrack was reused and the source text and layout were manually inspected.

## Editing

Edit the `DETAILS` object and HTML text in `template.html`, then run `node build.mjs` to rebuild the portable file. `assets/` contains the separate artwork. No API key, paid model or npm packages are required to build it.

For deterministic review: `index.html?render=1&t=7.5` displays the opening without playback controls, and `window.__seekTo(seconds)` seeks the animation. Browser screenshots and automated checks are in `verification/`; the rea-video report is in `analysis/report.html`.

## Independent branch deployment

This branch is `two-states-invitation`. Its root displays the complete five-scene Rajasthan–Gujarat invitation. It does not redirect to the road or standalone logo-reveal page. Its Vercel project is `jenny-priyansh-two-states`, with this branch tracked for production. The `main` and `logo` branches retain their existing contents and deployment.

## State outline attribution

Rajasthan and Gujarat silhouettes use geoBoundaries gbOpen IND ADM1 geometry (2011), filtered by ISO codes IN-RJ and IN-GJ. License: Creative Commons Attribution 2.5 India. Source: https://www.geoboundaries.org/api/current/gbOpen/IND/ADM1/ . Additional attribution is in `assets/MAP-LICENSE.txt`.
