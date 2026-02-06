from django.contrib import admin
from django.urls import path
from chess.models import Game
from .inlines import MoveExplanationInLine
from .views import ImportGamesMixin

@admin.register(Game)
class GameAdmin(ImportGamesMixin, admin.ModelAdmin):
    # Configuração do Admin para o modelo Game

    # Colunas mostradas na lista
    list_display = ('variant_name', 'white_player', 'black_player','event')
    
    # Campos de busca
    search_fields = ('variant_name', 'white_player', 'black_player','event')

    # Filtros laterais
    list_filter = ('white_player', 'black_player','event', 'created_at')

    # Conecta com a tabela criada acima
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