
// Inicializa o mapa como uma variável GLOBAL (para o HTML poder usar depois)
var map = L.map('mapa-container').setView([-8.0477, -34.877], 13);

// Adiciona o fundo do mapa (CARTO)
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    maxZoom: 19,
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>'
}).addTo(map);

// Geolocalização
map.locate({setView: true, maxZoom: 16});

function aoAcharLocalizacao(e) {
    var raio = e.accuracy / 2;
    L.marker(e.latlng).addTo(map)
        .bindPopup("Você está por aqui! (Margem de " + Math.round(raio) + " metros)").openPopup();
    L.circle(e.latlng, raio).addTo(map);
}

function aoDarErroLocalizacao(e) {
    alert("Não conseguimos acessar sua localização. Navegue pelo mapa manualmente.");
}

map.on('locationfound', aoAcharLocalizacao);
map.on('locationerror', aoDarErroLocalizacao);