from rest_framework import viewsets
from .models import Game
from .serializers import GameSerializer

class GameViewSet(viewsets.ModelViewSet):

    # Pegar todos os jogos
    queryset = Game.objects.all()
    
    # Utilizar o serializer como tradutor para JSON
    serializer_class = GameSerializer