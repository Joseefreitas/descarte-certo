const mapaAdicionar = L.map('mapa-adicionar').setView([-8.0476, -34.8770], 13);

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap contributors © CARTO'
}).addTo(mapaAdicionar);

let marcadorSelecionado = null;

function atualizarMarcador(lat, lng) {
    if (marcadorSelecionado) {
        mapaAdicionar.removeLayer(marcadorSelecionado);
    }
    marcadorSelecionado = L.marker([lat, lng]).addTo(mapaAdicionar);
    mapaAdicionar.setView([lat, lng], 16);

    document.getElementById('id_latitude').value = parseFloat(lat).toFixed(6);
    document.getElementById('id_longitude').value = parseFloat(lng).toFixed(6);
    document.getElementById('instrucao-mapa').textContent =
        `📍 Localização selecionada: ${parseFloat(lat).toFixed(6)}, ${parseFloat(lng).toFixed(6)}`;
    document.getElementById('mapa-adicionar').classList.add('selecionado');
}

// Busca por endereço via Nominatim
document.getElementById('btn-buscar-endereco').addEventListener('click', () => {
    const endereco = document.getElementById('endereco').value.trim();
    if (!endereco) {
        alert('Digite um endereço primeiro.');
        return;
    }

    const status = document.getElementById('instrucao-mapa');
    status.textContent = '🔍 Buscando endereço...';

    fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(endereco)}&format=json&limit=1`)
        .then(res => res.json())
        .then(data => {
            if (data.length === 0) {
                status.textContent = '❌ Endereço não encontrado. Tente ser mais específico.';
                return;
            }
            atualizarMarcador(data[0].lat, data[0].lon);
        })
        .catch(() => {
            status.textContent = '❌ Erro ao buscar endereço.';
        });
});

// Clique manual no mapa como alternativa
mapaAdicionar.on('click', function(e) {
    atualizarMarcador(e.latlng.lat, e.latlng.lng);
});