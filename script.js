const UFO_PROBABILITY = 0.3; // 30% chance on each scan check (every 3.5 seconds)
const SCAN_DURATION = 2;
const DETECTION_WINDOW = 1.5;

const message = document.getElementById('message');
const blip = document.getElementById('blip');
let isScanning = true;

// Configure sound effects. Howler is loaded from a CDN, so the detector
// must keep working (silently) if that CDN is unreachable.
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

// Start ambient sound
playSound(sounds.ambient);

function animateBlip() {
    if (window.gsap) {
        // Animate blip
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
        blip.style.opacity = '1';
        setTimeout(() => {
            blip.style.opacity = '0';
        }, 1200);
    }
}

function randomDetection() {
    if (Math.random() < UFO_PROBABILITY) {
        isScanning = false;
        message.textContent = "UFO DETECTED!";
        playSound(sounds.detection);
        animateBlip();

        // Reset after detection
        setTimeout(() => {
            message.textContent = "Scanning for UFOs...";
            isScanning = true;
        }, 3000);
    }
}

// Start random detection loop
setInterval(() => {
    if (isScanning) {
        setTimeout(randomDetection, (SCAN_DURATION - DETECTION_WINDOW) * 1000);
    }
}, (SCAN_DURATION + DETECTION_WINDOW) * 1000);

// Initial console check
console.log("GSAP available:", window.gsap !== undefined);
console.log("Howler available:", window.Howl !== undefined);
