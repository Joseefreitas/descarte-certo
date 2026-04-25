const mapaAdicionar = L.map('mapa-adicionar').setView([-8.0476, -34.8770], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(mapaAdicionar);

let marcadorSelecionado = null;

mapaAdicionar.on('click', function(e) {
    const lat = e.latlng.lat.toFixed(6);
    const lng = e.latlng.lng.toFixed(6);

    document.getElementById('id_latitude').value = lat;
    document.getElementById('id_longitude').value = lng;

    document.getElementById('instrucao-mapa').textContent =
        `📍 Localização selecionada: ${lat}, ${lng}`;

    if (marcadorSelecionado) {
        mapaAdicionar.removeLayer(marcadorSelecionado);
    }
    marcadorSelecionado = L.marker([lat, lng]).addTo(mapaAdicionar);

    document.getElementById('mapa-adicionar').classList.add('selecionado');
});