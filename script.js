const UFO_PROBABILITY = 0.3; // 30% chance every 5 seconds
const SCAN_DURATION = 2;
const DETECTION_WINDOW = 1.5;

const message = document.getElementById('message');
const blip = document.getElementById('blip');
let isScanning = true;

// Configure sound effects
const sounds = {
    detection: new window.Howl({
        src: ['https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3'],
        volume: 0.5
    }),
    ambient: new window.Howl({
        src: ['https://assets.mixkit.co/active_storage/sfx/2401/2401-preview.mp3'],
        loop: true,
        volume: 0.2
    })
};

// Start ambient sound
sounds.ambient.play();

function randomDetection() {
    if (Math.random() < UFO_PROBABILITY) {
        isScanning = false;
        message.textContent = "UFO DETECTED!";
        sounds.detection.play();
        
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