from django.db import models

# Tabela dos jogos
class Game(models.Model):

    # ID da tabela
    id = models.AutoField(primary_key=True)

    # Titulo da variante
    variant_name = models.CharField(max_length=100)

    # Nome do evento
    event = models.CharField(max_length=100)

    # Nome do jogador branco
    white_player = models.CharField(max_length=100)

    # Nome do jogador preto
    black_player = models.CharField(max_length=100)

    # PGN do jogo
    pgn = models.TextField()

    # Data da criação (Última modificação)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Como o objeto aparece no painel admin
    def __str__(self):
        return f"{self.variant_name} ({self.white_player} vs {self.black_player})"

# Tabela das explicações de movimentos
class MoveExplanation(models.Model):

    # ID da tabela
    id = models.AutoField(primary_key=True)

    # ID do jogo
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='explanations')

    # O endereço de cada lance no jogo
    ply = models.IntegerField()

    # A numeração visual do lance
    move_number = models.IntegerField()

    # Identificação de qual jogador fez o lance (True = branco, False = preto)
    color = models.BooleanField(default=True)

    # A explicação do lance
    content = models.TextField()

    # Não haver duas explicações para o mesmo lance no jogo
    class Meta:
        unique_together = ('game_id', 'ply')

    def __str__(self):
        # Tenta pegar o nome da variante, se não conseguir, pega somente o ply
        try:
            return f"Explicação Ply {self.ply} - {self.game.variant_name}"
        except AttributeError:
            return f"Explicação Ply {self.ply}"