import requests
from django.shortcuts import render

# Create your views here.
def buscar_agenda(request):
    query = request.GET.get('regiao', '').strip() 
    resultados = []
    erro = None

    if query:
        try:
            url_pacote = "http://dados.recife.pe.gov.br/api/3/action/package_show?id=roteiro-de-coleta"
            
            resp_pacote = requests.get(url_pacote, timeout=10)
            resp_pacote.raise_for_status()
            
            dados_pacote = resp_pacote.json()
            recursos = dados_pacote['result']['resources']
            resource_id = None
            
            for rec in recursos:
                if rec['format'].upper() in ['CSV', 'JSON'] and 'dicionario' not in rec['name'].lower():
                    resource_id = rec['id']
                    break
            
            if resource_id:
                url_busca = f"http://dados.recife.pe.gov.br/api/3/action/datastore_search?resource_id={resource_id}&q={query}"
                resp_busca = requests.get(url_busca, timeout=10)
                resp_busca.raise_for_status()
                
                dados_busca = resp_busca.json()
                registros = dados_busca['result']['records']
                
                if registros:
                    for reg in registros:
                        resultados.append({
                            'regiao': reg.get('bairro') or reg.get('microrregiao') or query,
                            'dias_semana': reg.get('frequencia') or reg.get('dias') or 'Não informado',
                            'horario': reg.get('turno') or 'Não informado',
                            'tipo_coleta': reg.get('tipo') or 'Coleta Domiciliar'
                        })
                else:
                    erro = f"Nenhum horário encontrado para '{query}'. Dica: Tente usar apenas o nome principal do bairro (ex: 'Várzea')."
            else:
                erro = "Sistema da Prefeitura em manutenção. Tente mais tarde."
                
        except requests.exceptions.RequestException:
            erro = "Não foi possível conectar aos dados da Prefeitura. Verifique sua internet."
        except Exception as e:
            erro = "Ocorreu um erro inesperado no processamento da agenda."

    contexto = {
        'resultados': resultados,
        'query': query,
        'erro': erro
    }
    return render(request, 'agenda.html', contexto)