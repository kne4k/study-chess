from django.contrib import admin
from .models import MoveExplanation
from .admin.game_admin import GameAdmin
# GameAdmin já está registrado no arquivo chess/admin/game_admin.py

# Registra MoveExplanation, para poder editar diretamente
@admin.register(MoveExplanation)
class MoveExplanationAdmin(admin.ModelAdmin):
    """Admin para editar explicações diretamente"""
    list_display = ('game_id', 'ply', 'move_number', 'color')
    list_filter = ('color', 'move_number')
    search_fields = ('content',)