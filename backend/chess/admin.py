from django.contrib import admin
from .models import Game, MoveExplanation

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