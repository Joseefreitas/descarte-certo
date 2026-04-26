const tips = [
    "Lave embalagens antes de reciclar para evitar contaminação.",
    "Pilhas e eletrônicos devem ser levados a pontos específicos de coleta.",
    "Separar o lixo orgânico ajuda na compostagem e reduz resíduos.",
    "Caixas de papelão devem estar secas antes da reciclagem.",
    "Vidros quebrados devem ser embalados com cuidado antes do descarte."
];

function setRandomTip() {
    const el = document.getElementById("tip-text");

    if (!el) return;

    const random = Math.floor(Math.random() * tips.length);
    el.textContent = tips[random];
}

document.addEventListener("DOMContentLoaded", () => {
    setRandomTip();

    setInterval(setRandomTip, 10000); // troca a cada 10s
});