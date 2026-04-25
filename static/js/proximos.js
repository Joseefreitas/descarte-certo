const markers = {};

function inicializarPins(pontos) {
    pontos.forEach((ponto, i) => {
        if (isNaN(ponto.lat) || isNaN(ponto.lng) || ponto.lat === 0) return;
        const marker = L.marker([ponto.lat, ponto.lng]).addTo(map);
        const popup = `<b>${ponto.nome}</b><br>
            Aceita: ${ponto.tipo}<br>
            📍 ${ponto.endereco}<br><br>
            <a href='https://www.google.com/maps/dir/?api=1&destination=${ponto.lat},${ponto.lng}'
               target='_blank'
               style='display:block;background:#008000;color:white;text-align:center;
                      padding:8px;border-radius:5px;text-decoration:none;font-weight:bold;'>
               Traçar Rota 🚗
            </a>`;
        marker.bindPopup(popup);
        markers[i] = marker;
    });
}

function haversine(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) ** 2 +
              Math.cos(lat1 * Math.PI / 180) *
              Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) ** 2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function mostrarProximos(userLat, userLng, pontos) {
    L.marker([userLat, userLng], {
        icon: L.divIcon({
            className: '',
            html: '<div style="background:#2196f3;width:14px;height:14px;border-radius:50%;border:2px solid white;box-shadow:0 0 4px rgba(0,0,0,0.4)"></div>'
        })
    }).addTo(map).bindPopup("📍 Você está aqui").openPopup();

    map.setView([userLat, userLng], 14);

    const comDistancia = pontos
        .map((p, i) => ({ ...p, i, dist: haversine(userLat, userLng, p.lat, p.lng) }))
        .filter(p => !isNaN(p.lat) && p.lat !== 0)
        .sort((a, b) => a.dist - b.dist);

    const container = document.getElementById('cards-container');
    container.innerHTML = '';

    const LIMITE = 5;
    const visiveis = comDistancia.slice(0, LIMITE);
    const restantes = comDistancia.slice(LIMITE);

    visiveis.forEach(p => renderizarCard(p, container));

    if (restantes.length > 0) {
        const btnVerMais = document.createElement('button');
        btnVerMais.textContent = `Ver mais ${restantes.length} pontos`;
        btnVerMais.style = 'width:100%;padding:8px;margin-top:4px;background:white;border:1px solid #4caf50;color:#4caf50;border-radius:6px;cursor:pointer;font-size:13px;';
        btnVerMais.addEventListener('click', () => {
            restantes.forEach(p => renderizarCard(p, container));
            btnVerMais.remove();
        });
        container.appendChild(btnVerMais);
    }

    document.getElementById('status-localizacao').textContent =
        `${comDistancia.length} pontos encontrados, ordenados por distância.`;
}

function renderizarCard(p, container) {
    const card = document.createElement('div');
    card.className = 'ponto-card';
    card.innerHTML = `
        <div class="nome">${p.nome}</div>
        <div class="distancia">🚶 ${p.dist.toFixed(2)} km de distância</div>
        <div class="tipo">♻️ ${p.tipo}</div>
        <div style="font-size:11px;color:#999;margin-top:4px">${p.endereco}</div>
    `;
    card.addEventListener('click', () => {
        map.flyTo([p.lat, p.lng], 16);
        markers[p.i]?.openPopup();
    });
    container.appendChild(card);
}

function configurarBotao(pontos) {
    document.getElementById('btn-localizar').addEventListener('click', () => {
        const status = document.getElementById('status-localizacao');
        status.textContent = 'Buscando sua localização...';

        if (!navigator.geolocation) {
            status.textContent = 'Geolocalização não suportada pelo seu navegador.';
            return;
        }

        navigator.geolocation.getCurrentPosition(
            pos => mostrarProximos(pos.coords.latitude, pos.coords.longitude, pontos),
            () => { status.textContent = 'Não foi possível obter sua localização.'; }
        );
    });
}
