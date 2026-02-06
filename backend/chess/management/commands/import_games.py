# Importações
from django.core.management.base import BaseCommand
from chess.utils.game_parser import GameParser

# Classe do comando
class Command(BaseCommand):

    # Descrição do comando
    help = 'Importa jogos e explicações de um arquivo de texto formatado'

    # Argumentos do comando
    def add_arguments(self, parser):
        parser.add_argument(
            'filepath',
            type=str,
            help='Caminho do arquivo de texto com os dados'
        )

    # Lógica do comando
    def handle(self, *args, **options):

        # Pegar o caminho do arquivo
        filepath = options['filepath']

        # Mensagem inicial
        self.stdout.write(self.style.SUCCESS(f'Lendo arquivo: {filepath}'))

        try:
            # Leitura do arquivo
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            # Usa a classe GameParser para processar e salvar os dados
            parser = GameParser()
            total_games, total_explanations = parser.parse_and_save(content)


            # Mensagem de sucesso
            self.stdout.write(self.style.SUCCESS(
                f'\nImportação concluída!\n'
                f'Jogos criados: {total_games}\n'
                f'Explicações criadas: {total_explanations}'))

        # Tratar erro de arquivo não encontrado
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {filepath}'))

        # Tratar outros erros
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro: {str(e)}'))