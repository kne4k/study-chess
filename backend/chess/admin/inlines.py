from django.contrib import admin
from chess.models import MoveExplanation

# Permite editar as explicações dentro da tela da partida
class MoveExplanationInLine(admin.TabularInline):
    model = MoveExplanation

    # Mostra uma linha extra para adicionar mais explicações
    extra = 1
    fields = ('ply', 'move_number', 'color', 'content')
    # Impede edição do índice do lance
    readonly_fields = ('ply',)