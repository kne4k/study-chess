from django import forms

# Formulário para upload de arquivo de jogos
class ImportGamesForm(forms.Form):
    file = forms.FileField(
        label='Arquivo de texto formatado (.txt)',
        help_text='<span> As instruções da formatação do arquivo estão abaixo</span>',
        widget=forms.FileInput(attrs={'accept': '.txt'})
    )