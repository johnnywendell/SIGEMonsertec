from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
from .models import Colaborador, Apontamento, ApontamentoColaborador

class ColaboradorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ColaboradorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Colaborador
        fields = ('nome', 'matricula', 'funcao', 'ativo')
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'funcao': forms.TextInput(attrs={'class': 'form-control'}),
            'ativo': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': _('Nome'),
            'matricula': _('Matrícula'),
            'funcao': _('Função'),
            'ativo': _('Ativo?'),
        }

class ApontamentoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApontamentoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Apontamento
        fields = ('data', 'area', 'projeto_cod', 'disciplina')
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'projeto_cod': forms.Select(attrs={'class': 'form-control'}),
            'disciplina': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'data': _('Data'),
            'area': _('Área'),
            'projeto_cod': _('Código do Projeto'),
            'disciplina': _('Disciplina'),
        }


class ApontamentoColaboradorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApontamentoColaboradorForm, self).__init__(*args, **kwargs)
        self.fields['colaborador'].queryset = Colaborador.objects.filter(ativo='1')

    class Meta:
        model = ApontamentoColaborador
        fields = ('colaborador', 'status', 'lider')
        widgets = {
            'colaborador': forms.Select(attrs={'class': 'form-control s3lect2'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'lider': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'colaborador': _('Colaborador'),
            'status': _('Status'),
            'lider': _('Líder'),
        }
        
ApontamentoColaboradorFormSet = inlineformset_factory(
    Apontamento, ApontamentoColaborador, form=ApontamentoColaboradorForm, extra=1, can_delete=True
)