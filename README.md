![UFO Detector banner](banner.png)

# UFO-Detector

A novelty radar page that pretends to scan for UFOs. A green radar sweep
animates in a circle, and at random the page flashes `UFO DETECTED!` with
a red blip and a sound effect, then goes back to scanning. It detects
nothing real; the detections are dice rolls.

## Run

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server
# then visit http://localhost:8000/
```

The page loads GSAP and Howler from public CDNs and the two sound effects
from Mixkit, so the animations and sounds need network access. If a CDN
is unreachable the page still loads and still scans and detects, only
silently and without the blip animation flourish: the blip is shown and
hidden directly instead.

## How it behaves

- A scan check runs every 3.5 seconds, with the detection roll delayed
  0.5 seconds after each check.
- Each roll has a 30 percent chance of a detection.
- On a detection the message changes to `UFO DETECTED!`, the detection
  sound plays (when Howler loaded), and the blip pulses. After 3 seconds
  the message returns to `Scanning for UFOs...` and scanning resumes.
- An ambient loop starts on page load when Howler loaded. Browsers may
  hold audio until the first interaction with the page.

## Files

- `index.html` - the page
- `script.js` - scan loop, detection roll, sounds, and blip animation
- `style.css` - layout and the radar sweep animation
- `LICENSE` - MIT license
- `logo.png`, `banner.png` - project branding

## Honest limits

The logic was verified headlessly in Node with mocked document, timer,
GSAP, and Howler objects, including the cases where one or both CDN
libraries are missing. It was not run in a real browser for this pass, so
the visual result and the actual audio playback were not observed.
