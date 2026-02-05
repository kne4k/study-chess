from django import forms
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from .models import Game, MoveExplanation
import re

class ImportGamesForm(forms.Form):
    file = forms.FileField(
        label='Arquivo de texto formatado (.txt)',
        help_text='''
            <span> As instruções da formatação do arquivo estão abaixo
            </span>
        ''',
        widget=forms.FileInput(attrs={'accept': '.txt'})
    )

# Permite editar as explicações dentro da tela da partida
class MoveExplanationInLine(admin.TabularInline):
    model = MoveExplanation

    # Mostra uma linha extra para adicionar mais explicações
    extra = 1

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('variant_name', 'white_player', 'black_player','event')

    # Conecta a tabela criada acima
    inlines = [MoveExplanationInLine]

    # Template customizado para adicionar botão de importar jogos
    change_list_template = 'admin/chess/game_changelist.html'

    # Adiciona URL customizada para importação
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import/', self.import_games_view, name='import_games')
        ]
        return custom_urls + urls
    
    # View que processa upload e importação dos jogos
    def import_games_view(self, request):
        if request.method == "POST":
            form = ImportGamesForm(request.POST, request.FILES)

            if form.is_valid():
                arquivo = request.FILES['file']

                try:
                    content = arquivo.read().decode('utf-8')
                except UnicodeDecodeError:
                    self.message_user(
                        request,
                        'Erro: arquivo não está em UTF-8 e não pode ser lido',
                        level='error'
                    )
                    return redirect('..')
                
                # Processar os dados da importação
                try:
                    total_games, total_explanations = self.process_import(content)

                    self.message_user(
                        request,
                        f'{total_games} jogos e {total_explanations} explicações foram importados!',
                        level='success'
                    )
                except Exception as e:
                    self.message_user(
                        request,
                        f'Erro ao processar o arquivo: {str(e)}',
                        level='error'
                    )
                
                return redirect('..')
        else:
            form = ImportGamesForm()
        context = {
            'form': form,
            'site_header': 'Importação de Jogos',
        }
        return render(request, 'admin/chess/import_games.html', context)
        
    # Processa conteúdo do arquivo e cria os objetos no banco de dados
    def process_import(self, content):
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

        return total_games, total_explanations