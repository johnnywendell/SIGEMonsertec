from django import forms
from django.utils.translation import gettext_lazy as _
from cadastro.models.geral import Contrato,Area,Aprovador,Solicitante,ItemBm, EtapaAprovacao


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ('contrato',)
        widgets = {
            'contrato': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'contrato': _('Contrato'),
        }
        
class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ('area','contrato')
        widgets = {
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'contrato': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'area': _('Area'),
            'contrato': _('Contrato'),
        }

class AprovadorForm(forms.ModelForm):
    class Meta:
        model = Aprovador
        fields = ('aprovador','contrato')
        widgets = {
            'aprovador': forms.TextInput(attrs={'class': 'form-control'}),
            'contrato': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'aprovador': _('Aprovador'),
            'contrato': _('Contrato'),
        }
class SolicitanteForm(forms.ModelForm):
    class Meta:
        model = Solicitante
        fields = ('solicitante','contrato')
        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control'}),
            'contrato': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'solicitante': _('Solicitante'),
            'contrato': _('Contrato'),
        }

class ItemBmForm(forms.ModelForm):
    class Meta:
        model = ItemBm
        fields = ('contrato','item_ref','disciplina','descricao','und','preco_item','obs')
        widgets = {
            'contrato': forms.Select(attrs={'class': 'form-control'}),
            'item_ref': forms.TextInput(attrs={'class': 'form-control'}),
            'disciplina': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'und': forms.TextInput(attrs={'class': 'form-control'}),
            'preco_item': forms.TextInput(attrs={'class': 'form-control'}),
            'obs': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'contrato': _('Contrato'),
            'item_ref': _('Item/Código'),
            'disciplina': _('Disciplina'),
            'descricao': _('Descrição'),
            'und': _('Unidade'),
            'preco_item': _('Preço'),
            'obs': _('Obs.'),
        }
