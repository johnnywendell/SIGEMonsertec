from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory

from .models import Romaneio, Material
from cadastro.models.geral import ItemBm


class RomaneioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RomaneioForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Romaneio
        fields = ('entrada','nf','documento','obs','area','solicitante','concluido','bm')
        widgets = {
            'concluido': forms.CheckboxInput(attrs={'class': 'exclude-from-hide'}),
            'entrada': forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete':'off'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'solicitante': forms.Select(attrs={'class': 'form-control'}),
            'nf': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'obs': forms.TextInput(attrs={'class': 'form-control'}),
            'bm': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'concluido': _('Concluido'), 
            'entrada': _('Data de Entrada'),
            'area': _('Area'),
            'solicitante': _('Solicitante/fiscal'),
            'nf': _('Nota Fiscal'),
            'documento': _('DOC/REC/REF'),
            'obs': _('Observações'),
            'bm': _('Boletim de medição'),
        }
   
    
class MaterialForm(forms.ModelForm):
    pol_inicial = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','disabled': True}),label=_('Fator'),required=False)
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['jato'].queryset = ItemBm.objects.filter(disciplina='PINTURA',und="M2")
        self.fields['ti'].queryset = ItemBm.objects.filter(disciplina='PINTURA',und="M2")
        self.fields['ta'].queryset = ItemBm.objects.filter(disciplina='PINTURA',und="M2")
        self.fields['tf'].queryset = ItemBm.objects.filter(disciplina='PINTURA',und="M2")

    class Meta:
        model = Material 

        fields = ('jato','tf','ti','ta','cor','material','descricao','polegada','m_quantidade',
                   'm2','raio','largura','altura','comprimento','lados','relatorio')
        widgets = {
            'jato': forms.Select(attrs={'class': 'form-control'}),
            'tf': forms.Select(attrs={'class': 'form-control'}),
            'ti': forms.Select(attrs={'class': 'form-control'}),
            'ta': forms.Select(attrs={'class': 'form-control'}),  
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-control clMaterial'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'polegada': forms.TextInput(attrs={'class': 'form-control clPolegada' }),
            'm_quantidade': forms.TextInput(attrs={'class': 'form-control  clQuantidade'}),
            'm2': forms.TextInput(attrs={'class': 'form-control '}),
            'raio': forms.TextInput(attrs={'class': 'form-control '}),
            'largura': forms.TextInput(attrs={'class': 'form-control '}),
            'altura': forms.TextInput(attrs={'class': 'form-control '}),
            'comprimento': forms.TextInput(attrs={'class': 'form-control '}),
            'lados': forms.TextInput(attrs={'class': 'form-control  clLados'}),
            'relatorio': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            
            'jato': _('jato'), 
            'ti': _('ti'), 
            'ta': _('ta'), 
            'tf': _('tf'), 
            'cor': _('cor'), 
            'material': _('material'), 
            'descricao': _('descricao'),
            'polegada': _('polegada'),
            'm_quantidade': _('m_quantidade'), 
            'm2': _('m2'), 
            'raio': _('raio'), 
            'largura': _('largura'), 
            'altura': _('altura'),
            'comprimento': _('comprimento/lados'),
            'lados': _('Qtd.'), 
            'relatorio': _('Relatorio'), 
        }
    
MaterialFormSet = inlineformset_factory(
    Romaneio, Material, form=MaterialForm, extra=1, can_delete=True)
