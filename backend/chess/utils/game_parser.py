import re
from chess.models import Game, MoveExplanation

class GameParser:
    # Parseia o conteúdo do arquivo e cria os objetos no banco de dados
    def parse_and_save(self, content):
        # Divide o conteúdo do arquivo em blocos, sendo cada bloco um jogo
        # Depois salva no banco de dados
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

            # Extrair os metadados
            metadata = self._extract_metadata(game_text)
            if not metadata:
                continue

            # Cria o objeto no banco de dados
            game = Game.objects.create(**metadata)
            total_games += 1

            # Processa as explicações
            total_explanations += self._process_explanations(game_text, game)

        return total_games, total_explanations

    def _extract_metadata(self, game_text):
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
                return None

            # Extrai os valores
            return {
                'variant_name': variant_match.group(1).strip(),
                'event': event_match.group(1).strip(),
                'white_player': white_match.group(1).strip(),
                'black_player': black_match.group(1).strip(),
                'pgn': pgn_match.group(1).strip()
            }   

    def _process_explanations(self, game_text, game):
            # Processa as explicações do jogo e salva no banco de dados
            if '---EXPLICAÇÕES---' not in game_text:
                return 0

            # Pega tudo após o marcador ---EXPLICAÇÕES---
            explanations_text = game_text.split('---EXPLICAÇÕES---')[1]

            # Divide o conteúdo por "PLY X:"
            ply_blocks = re.split(r'PLY\s+(\d+):', explanations_text)

            total = 0

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

                total += 1

            return total