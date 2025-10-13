from django import forms
from .models import Aluno
import re
from datetime import date, timedelta

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

    def clean_nome_completo(self):
        nome = self.cleaned_data.get('nome_completo')
        if nome and not re.match(r"^[a-zA-Z\sáéíóúâêôãõçÁÉÍÓÚÂÊÔÃÕÇ'.]+$", nome):
            raise forms.ValidationError("O nome deve conter apenas letras, espaços e acentos válidos.")
        return nome

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        
        if not data_nascimento:
            return data_nascimento

        hoje = date.today()
        
        if data_nascimento > hoje:
            raise forms.ValidationError("A data de nascimento não pode ser no futuro.")

        idade_minima = hoje - timedelta(days=365.25 * 90)
        idade_maxima = hoje - timedelta(days=365.25 * 2)

        if not (idade_minima <= data_nascimento <= idade_maxima):
            raise forms.ValidationError("O aluno deve ter entre 2 e 90 anos de idade.")
            
        return data_nascimento

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