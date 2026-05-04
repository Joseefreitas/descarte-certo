import os
import requests
from django.core.management.base import BaseCommand
from mapa.models import PontoColeta


class Command(BaseCommand):
    help = 'Importa pontos de coleta da API da Prefeitura do Recife'

    def handle(self, *args, **options):
        resource_id = os.environ.get('RESOURCE_ID_PONTOS', '24adb60a-9fb2-4f55-b1d5-808729f5f28e')
        url = 'https://dados.recife.pe.gov.br/api/action/datastore_search'

        criados = 0
        atualizados = 0
        erros = 0
        offset = 0
        limit = 100  # busca 100 por vez

        self.stdout.write('🔄 Buscando pontos da API da Prefeitura do Recife...')

        while True:
            try:
                response = requests.get(url, params={
                    'resource_id': resource_id,
                    'limit': limit,
                    'offset': offset,
                })
                response.raise_for_status()
                data = response.json()

                records = data['result']['records']
                if not records:
                    break  # acabaram os registros

                for row in records:
                    try:
                        observacao = row.get('observacao', '').strip()
                        bairro = row.get('bairro', '').strip()
                        endereco = row.get('endereco', '').strip()
                        complemento = row.get('complemento', '').strip()
                        tipo = row.get('tiporesiduo', '').strip()
                        lat = float(str(row.get('latitude', 0)).replace(',', '.'))
                        lng = float(str(row.get('longitude', 0)).replace(',', '.'))

                        if not lat or not lng:
                            continue

                        # Monta o nome
                        if observacao and bairro and observacao != bairro:
                            nome = f'{observacao} - {bairro}'
                        elif observacao:
                            nome = observacao
                        else:
                            nome = bairro

                        # Monta o endereço completo
                        endereco_completo = endereco
                        if complemento and complemento.lower() != 's/n':
                            endereco_completo += f', {complemento}'
                        endereco_completo += f' - {bairro}, Recife'

                        # Cria ou atualiza
                        ponto, created = PontoColeta.objects.update_or_create(
                            latitude=lat,
                            longitude=lng,
                            defaults={
                                'nome': nome[:100],
                                'endereco': endereco_completo[:255],
                                'tipo_residuo': tipo[:255],
                            }
                        )

                        if created:
                            criados += 1
                            self.stdout.write(f'✅ Criado: {nome}')
                        else:
                            atualizados += 1

                    except Exception as e:
                        erros += 1
                        self.stderr.write(f'❌ Erro: {e}')

                offset += limit

            except requests.RequestException as e:
                self.stderr.write(f'❌ Erro na API: {e}')
                break

        self.stdout.write(f'\nTotal criados: {criados} | Atualizados: {atualizados} | Erros: {erros}')