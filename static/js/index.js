const slides = document.querySelectorAll('.slide');
let current = 0;

function goTo(index) {
    slides.forEach(slide => {
        slide.style.transform = `translateX(-${index * 100}%)`;
    });
    current = index;
}

setInterval(() => {
    const next = (current + 1) % slides.length;
    goTo(next);
}, 4000);