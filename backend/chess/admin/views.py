from django.shortcuts import render, redirect
from django.contrib import messages
from chess.forms.import_forms import ImportGamesForm
from chess.utils.game_parser import GameParser

class ImportGamesMixin:
# Mixin para adicionar a funcionalidade de importar jogos e explicações

    def import_games_view(self, request):
        if request.method == "POST":
            form = ImportGamesForm(request.POST, request.FILES)

            if form.is_valid():
                arquivo = request.FILES['file']

                try:
                    content = arquivo.read().decode('utf-8')
                except UnicodeDecodeError:
                    messages.error(
                        request,
                        'Erro: arquivo não está em UTF-8 e não pode ser lido',
                        level='error'
                    )
                    return redirect('..')
                
                # Processar os dados da importação
                try:
                    parser = GameParser()
                    total_games, total_explanations = parser.parse_and_save(content)

                    messages.success(
                        request,
                        f'{total_games} jogos e {total_explanations} explicações foram importados!',
                        level='success'
                    )
                except Exception as e:
                    messages.error(
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