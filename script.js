const UFO_PROBABILITY = 0.3; // 30% chance on each scan check (every 3.5 seconds)
// I split the timing into two named pieces, but the numbers that
// matter are their sum and their difference: the check interval at
// the bottom is the sum (3.5 seconds) and the delay before each roll
// is the difference (0.5 seconds). Changing either constant moves
// both numbers, which is not obvious from the names.
const SCAN_DURATION = 2;
const DETECTION_WINDOW = 1.5;

// This file loads as a module, and module scripts run after the page
// has been parsed, so both elements already exist when I look them
// up here. As a classic script in the head this would have failed.
const message = document.getElementById('message');
const blip = document.getElementById('blip');
// This flag is the only guard against overlapping detections. The
// interval at the bottom reads it before scheduling a roll, and
// randomDetection flips it before showing anything.
let isScanning = true;

// Configure sound effects. Howler is loaded from a CDN, so the detector
// must keep working (silently) if that CDN is unreachable.
// The sound files themselves are remote too. If Mixkit is down while
// Howler loads, these objects exist but their files never arrive, and
// play() then does nothing anyone can hear. I let that pass silently,
// same as a missing Howler.
const hasHowler = typeof window.Howl !== 'undefined';
const sounds = {
    detection: hasHowler ? new window.Howl({
        src: ['https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3'],
        volume: 0.5
    }) : null,
    ambient: hasHowler ? new window.Howl({
        src: ['https://assets.mixkit.co/active_storage/sfx/2401/2401-preview.mp3'],
        loop: true,
        volume: 0.2
    }) : null
};

function playSound(sound) {
    if (sound) {
        try {
            sound.play();
        } catch (err) {
            // Audio is decorative here; never let it break detection.
        }
    }
}

// Start ambient sound. I call this at load and never retry it:
// browsers often hold audio until the first interaction with the
// page, so on a fresh load this may stay silent until the user
// clicks or taps, and I accept that instead of wiring a retry.
playSound(sounds.ambient);

function animateBlip() {
    if (window.gsap) {
        // The pulse runs 0.3 seconds per leg, repeated 3 times with
        // yoyo, so about 1.2 seconds of pulsing, then the onComplete
        // fade takes the blip back to invisible over 0.5 seconds.
        window.gsap.to(blip, {
            opacity: 1,
            scale: 2.5,
            duration: 0.3,
            repeat: 3,
            yoyo: true,
            onComplete: () => {
                window.gsap.to(blip, { opacity: 0, duration: 0.5 });
            }
        });
    } else {
        // GSAP CDN unreachable: show and hide the blip directly so the
        // detection is still visible and the reset below still runs.
        // The 1200 ms here matches the pulse span of the GSAP branch
        // above, without the fade at the end.
        blip.style.opacity = '1';
        setTimeout(() => {
            blip.style.opacity = '0';
        }, 1200);
    }
}

function randomDetection() {
    // This function trusts its caller: the interval only schedules it
    // while isScanning is true. It does not check the flag itself.
    if (Math.random() < UFO_PROBABILITY) {
        // I flip the flag first, before any display work, so interval
        // ticks that land during the 3 seconds below do nothing and
        // a second detection cannot stack on top of this one.
        isScanning = false;
        message.textContent = "UFO DETECTED!";
        playSound(sounds.detection);
        animateBlip();

        // Reset after detection. This is scheduled last on purpose:
        // playSound and animateBlip are built so they cannot throw
        // when a CDN is missing, because an exception above this line
        // would leave the page stuck on the detection message with
        // isScanning false and no way back to scanning.
        setTimeout(() => {
            message.textContent = "Scanning for UFOs...";
            isScanning = true;
        }, 3000);
    }
}

// Start random detection loop. The tick itself does no rolling; it
// only schedules the roll half a second later, and only while
// scanning. Ticks that arrive during a detection are dropped, not
// queued, so a long detection display never builds up a backlog.
setInterval(() => {
    if (isScanning) {
        setTimeout(randomDetection, (SCAN_DURATION - DETECTION_WINDOW) * 1000);
    }
}, (SCAN_DURATION + DETECTION_WINDOW) * 1000);

// Initial console check. I leave these two lines in on purpose: when
// the page misbehaves, the first question is whether the CDN
// libraries arrived, and this answers it without a network tab.
console.log("GSAP available:", window.gsap !== undefined);
console.log("Howler available:", window.Howl !== undefined);
