# Jenny & Priyansh — palm road invitation

Open `index.html` in Chrome or Edge. It is a portable, self-contained HTML file: artwork, Google Sans, the script font and reference audio are embedded. Playback starts silently; tap the speaker to enable music. Replay and timeline controls are below the invitation. No server or installation is required.

Details used from the existing `jenny-priyansh-invite/timeline.js`: Jenny & Priyansh; 15–16 February 2026; Arawali Ananta Elite, Ranakpur, Rajasthan. These dates were preserved as supplied, even though they are in the past.

“Save the date” retains calligraphy. Subsequent dates, invitation copy, names and venue use Google Sans, as requested. The passengers remain the reference's illustrated couple; they are not photographs of Jenny and Priyansh.

## Editable source

The `DETAILS` object in the HTML controls names, date and venue. Edit `template.html` and run `node build.mjs` to embed the included artwork, fonts and audio into `index.html`. No packages or API keys are needed. For browser screenshots, append `?render=1&t=10.8`. `window.__seekTo(seconds)` provides deterministic animation seeking.

## Hosting

This is a static site. Vercel serves the committed `index.html` without a build step. GitHub pushes to `main` deploy through the connected Vercel project.

## Reference analysis

`rea-video survey`, `decompose`, `review` and `apply-review` were run. The source has 346 video frames at 30 fps (11.533 seconds), one continuous composition, and no scene cuts. Its audio container is slightly longer than its visible video.

The recreation separates the palm scenery, road, car and editable typography. The car moves approximately 125 pixels/second down a fixed 720×1280 canvas. Approximate text entrances: date 3.5s; message 5.3s; Jenny 6.0s; ampersand 6.8s; Priyansh 7.4s; venue 8.1s; closing 8.8s; heart 9.5s. Fonts and fades are a reconstruction, not a claim of a pixel-identical source project.

The automated rea-video classifier retained an AI-video label despite the visual review. The observed fixed foliage, unchanging car silhouette/passenger pose, and separate text fades support recreating this as a layered motion composition. Whether the original illustration itself was generated with AI is unverified. Soundtrack provenance and automatic SFX/voice guesses are unverified; the HTML preserves the supplied soundtrack instead of inventing replacements. Audio separation was skipped because no replacement soundtrack was needed.

Browser verification covered desktop/mobile layout, font/image loading, timeline seeking, play/pause, replay and the music toggle. Local analysis inputs and verification captures are excluded from this repository.
