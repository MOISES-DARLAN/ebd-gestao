from django import forms
from .models import Aluno

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome_completo', 'data_nascimento', 'nome_responsavel', 'telefone_contato']
        widgets = {
            'data_nascimento': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

class ChamadaGeralForm(forms.Form):
    oferta_do_dia = forms.DecimalField(
        label="Oferta do Dia (R$)",
        max_digits=10,
        decimal_places=2,
        min_value=0,
        max_value=2000,
        required=False,
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    visitantes = forms.IntegerField(
        label="Nº de Visitantes",
        min_value=0,
        max_value=2000,
        required=False
    )