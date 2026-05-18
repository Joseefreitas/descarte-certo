function toggleCard(btn) {
    const card = btn.closest('.rec-card');
    card.classList.toggle('active');
    btn.textContent = card.classList.contains('active') ? 'Fechar' : 'Saiba mais';
}