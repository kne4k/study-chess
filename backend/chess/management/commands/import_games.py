# Importações
from django.core.management.base import BaseCommand
from chess.models import Game, MoveExplanation
import re

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

            # Processar os dados
            # Divide o conteúdo do arquivo em blocos, cada bloco é um jogo
            games_raw = content.split('===JOGO===')[1:] # Remove o primeiro elemento vazio antes de ===JOGO=== 
            
            total_games = 0
            total_explanations = 0

            for game_text in games_raw:

                # Verifica se o conteúdo possui ===FIM===
                if '===FIM===' not in game_text:
                    continue # Se não tiver, pula para o próximo jogo

                # Remove tudo após ===FIM===
                game_text = game_text.split('===FIM===')[0]
                # Desse modo, game_text agora contém apenas as informações de um jogo


                # Extrai os metadados do jogo
                # Busca por "VARIANT: XXX"
                variant_match = re.search(r'VARIANT:\s*(.+)', game_text)
                # Busca por "EVENT: XXX"
                event_match = re.search(r'EVENT:\s*(.+)', game_text)
                # Busca por "WHITE: XXX"
                white_match = re.search(r'WHITE:\s*(.+)', game_text)
                # Busca por "BLACK: XXX"
                black_match = re.search(r'BLACK:\s*(.+)', game_text)
                # Busca por "PGN: XXX"
                pgn_match = re.search(r'PGN:\s*(.+)', game_text)

                # Verifica se encontrou todos os metadados
                if not all([variant_match, event_match, white_match, black_match, pgn_match]):
                    self.stdout.write(self.style.WARNING(f'Jogo incompleto encontrado, este jogo não será adicionado, buscando próximo jogo no arquivo...'))
                    continue

                # Extrai os valores
                variant_name = variant_match.group(1).strip()
                event = event_match.group(1).strip()
                white_player = white_match.group(1).strip()
                black_player = black_match.group(1).strip()
                pgn = pgn_match.group(1).strip()

                # Criar o objeto game no banco de dados
                game = Game.objects.create(
                    variant_name=variant_name,
                    event=event,
                    white_player=white_player,
                    black_player=black_player,
                    pgn=pgn
                )

                total_games += 1
                self.stdout.write(self.style.SUCCESS(f'Adicionado o jogo que contém a variante: {variant_name}'))

                # Verifica se o jogo possui explicações
                if '---EXPLICAÇÕES---' in game_text:
                    # Pega tudo após o marcador ---EXPLICAÇÕES---
                    explanations_text = game_text.split('---EXPLICAÇÕES---')[1]

                    # Divide o conteúdo por "PLY X:"
                    ply_blocks = re.split(r'PLY\s+(\d+):', explanations_text)

                    # Processamento do conteúdo de cada ply
                    # Loop de 2 em 2: índice ímpar = ply, índice par = explicação da ply
                    for i in range(1, len(ply_blocks), 2):

                        # Pega o número da ply
                        ply_number = int(ply_blocks[i])

                        # Pega o conteúdo da explicação
                        content = ply_blocks[i + 1].strip()

                        # Pula se o conteúdo estiver vazio
                        if not content:
                            continue
                
                        # Calcula o número do lance
                        move_number = (ply_number // 2) + 1

                        # Calcula a cor do jogador que executou o lance (True=brancas, False=pretas)
                        color = (ply_number % 2 == 1)

                        MoveExplanation.objects.create(
                            game_id=game,
                            ply=ply_number,
                            move_number=move_number,
                            color=color,
                            content=content
                        )

                        total_explanations += 1
                        self.stdout.write(f'Explicação para o lance {move_number} das {color} adicionada')


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