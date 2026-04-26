function toggleCard(btn) {
    const card = btn.closest(".rec-card");
    card.classList.toggle("active");

    if (card.classList.contains("active")) {
        btn.textContent = "Mostrar menos";
    } else {
        btn.textContent = "Saiba mais";
    }
}