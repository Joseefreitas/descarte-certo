import csv
import os
from django.core.management.base import BaseCommand
from mapa.models import PontoColeta


class Command(BaseCommand):
    help = 'Importa pontos de coleta de um arquivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Caminho para o arquivo CSV')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        if not os.path.exists(csv_file):
            self.stderr.write(f'Arquivo não encontrado: {csv_file}')
            return

        criados = 0
        erros = 0

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    observacao = row.get('observacao', '').strip()
                    bairro = row.get('bairro', '').strip()
                    endereco = row.get('endereco', '').strip()
                    complemento = row.get('complemento', '').strip()
                    tipo = row.get('tiporesiduo', '').strip()
                    lat = float(row.get('latitude', 0))
                    lng = float(row.get('longitude', 0))

                    # Monta o nome: "Ecoestação Arruda" ou "Cooperativa - São José"
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

                    # Evita duplicatas
                    if PontoColeta.objects.filter(latitude=lat, longitude=lng).exists():
                        self.stdout.write(f'Já existe: {nome}')
                        continue

                    PontoColeta.objects.create(
                        nome=nome,
                        endereco=endereco_completo,
                        tipo_residuo=tipo,
                        latitude=lat,
                        longitude=lng,
                    )
                    criados += 1
                    self.stdout.write(f'✅ Criado: {nome}')

                except Exception as e:
                    erros += 1
                    self.stderr.write(f'❌ Erro na linha {row}: {e}')

        self.stdout.write(f'\nTotal criados: {criados} | Erros: {erros}')