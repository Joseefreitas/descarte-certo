import requests
from django.shortcuts import render

# Create your views here.
def buscar_agenda(request):
    query = request.GET.get('regiao') 
    resultados = []
    erro = None

    if query:
        try:
            url_pacote = "http://dados.recife.pe.gov.br/api/3/action/package_show?id=roteiro-de-coleta"
            
            resp_pacote = requests.get(url_pacote, timeout=10).json()
            recursos = resp_pacote['result']['resources']
            resource_id = None
            for rec in recursos:
                if rec['format'].upper() in ['CSV', 'JSON'] and 'dicionario' not in rec['name'].lower():
                    resource_id = rec['id']
                    break
            
            if resource_id:
                url_busca = f"http://dados.recife.pe.gov.br/api/3/action/datastore_search?resource_id={resource_id}&q={query}"
                resp_busca = requests.get(url_busca, timeout=10).json()
                
                registros = resp_busca['result']['records']
                
                if registros:
                    for reg in registros:
                        resultados.append({
                            'regiao': reg.get('bairro', reg.get('microrregiao', query)),
                            'dias_semana': reg.get('frequencia', reg.get('dias', 'Não informado')),
                            'horario': reg.get('turno', 'Não informado'),
                            'tipo_coleta': reg.get('tipo', 'Coleta Domiciliar')
                        })
                else:
                    erro = f"Nenhum horário encontrado para '{query}'. Tente usar apenas o nome do bairro."
            else:
                erro = "Base de dados da EMLURB indisponível."
                
        except Exception as e:
            erro = "Ocorreu um erro ao conectar com o serviço da Prefeitura. Tente novamente."

    contexto = {
        'resultados': resultados,
        'query': query,
        'erro': erro
    }
    return render(request, 'agenda.html', contexto)