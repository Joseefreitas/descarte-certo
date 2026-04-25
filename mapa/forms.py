from django import forms
from .models import PontoColeta

class PontoColetaForm(forms.ModelForm):
    class Meta:
        model = PontoColeta
        fields = ['nome', 'endereco', 'latitude', 'longitude', 'tipo_residuo']
        labels = {
            'nome': 'Nome do local',
            'endereco': 'Endereço',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'tipo_residuo': 'Tipo de resíduo aceito',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Cooperativa Verde Vida'}),
            'endereco': forms.TextInput(attrs={'placeholder': 'Ex: Rua das Flores, 123 - Boa Viagem'}),
            'tipo_residuo': forms.TextInput(attrs={'placeholder': 'Ex: Eletrônicos, Plástico, Papel'}),
        }