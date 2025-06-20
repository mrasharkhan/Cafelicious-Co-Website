const carousel = document.getElementById("carouselItems");
const images = carousel.querySelectorAll("img");


const total = images.length;
const angleStep = 360 / total;
let currentAngle = 0;
const radius = 500;
let intervalId;

function updateImages() {
  images.forEach((img, i) => {
    const angle = (angleStep * i + currentAngle) % 360;
    const rad = angle * (Math.PI / 180);
    const x = Math.sin(rad) * radius;
    const z = Math.cos(rad) * radius;
    const y = Math.cos(rad) * -100;

    img.style.transform = `translate(-50%, -80%) translateX(${x}px) translateZ(${z}px) translateY(${-y}px)`;
    img.style.opacity = z > 0 ? 1 : 0.2;
  });
}

function rotateToIndex(index) {
  const targetAngle = -angleStep * index;
  currentAngle = targetAngle;
  updateImages();
}

function startAutoRotate() {
  intervalId = setInterval(() => {
    currentAngle += angleStep;
    updateImages();
  }, 3000);
}

function stopAutoRotate() {
  clearInterval(intervalId);
}

images.forEach((img, i) => {
  img.addEventListener("click", () => {
    stopAutoRotate();
    rotateToIndex(i);
  });
});

updateImages();
startAutoRotate();