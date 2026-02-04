from rest_framework import serializers
from .models import Game, MoveExplanation


# Tradução em JSON da tabela MoveExplanation
class MoveExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoveExplanation
        fields = ['ply', 'move_number', 'color', 'content']

# Tradução em JSON da tabela Game
class GameSerializer(serializers.ModelSerializer):

    # Enviar as explicações dos lances quando enviar os dados do partida
    explanations = MoveExplanationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Game
        fields = ['id', 'variant_name', 'event', 'white_player', 'black_player', 'pgn', 'explanations']