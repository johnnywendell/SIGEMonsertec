from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
from .models import RDO,AS, ItemMedicao, ProjetoCodigo, DISCIP

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = ProjetoCodigo
        fields = '__all__'
        widgets = {
                    'projeto_nome':forms.DateInput(attrs={'class': 'form-control'}), 
                    'contrato':forms.Select(attrs={'class': 'form-control'}),
                    }

class PlanejamentoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlanejamentoForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ('data','unidade','solicitante','contrato','escopo','local','tipo','doc',
                  'disciplina','obs','aprovado')
        widgets = {
                    'data':forms.DateInput(attrs={'class': 'form-control datepicker', 'autocomplete':'off'}), 
                    'unidade':forms.Select(attrs={'class': 'form-control'}),
                    'solicitante':forms.Select(attrs={'class': 'form-control'}),
                    'contrato':forms.Select(attrs={'class': 'form-control'}),
                    'escopo':forms.TextInput(attrs={'class': 'form-control'}), 
                    'local':forms.TextInput(attrs={'class': 'form-control'}), 
                    'tipo':forms.Select(attrs={'class': 'form-control'}),
                    'doc': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
                    'disciplina':forms.Select(attrs={'class': 'form-control'}),
                    'obs':forms.TextInput(attrs={'class': 'form-control'}), 
                    'aprovado':forms.CheckboxInput(attrs={'class': 'form-control'}),
                    }
        labels = {
            'data':_('Data'),
            'unidade':_('Àrea'),
            'solicitante':_('Solicitante'),
            'contrato':_('Contrato'),
            'escopo':_('Escopo'),
            'local':_('Local do Serviço'),
            'tipo':_('Tipo do Serviço'),
            'doc':_('Documento'),
            'disciplina':_('Disciplina'),
            'obs':_('Obs.'),
            'aprovado':_('Status'),
        }

class RDOForm(PlanejamentoForm):
    class Meta(PlanejamentoForm.Meta):
        model = RDO
        fields = PlanejamentoForm.Meta.fields + ('AS','encarregado','projeto_cod','clima','inicio','termino',
                                        'inicio_pt','termino_pt')

        widgets = {
            **PlanejamentoForm.Meta.widgets,
                    'AS':forms.Select(attrs={'class': 'form-control'}), 
                    'encarregado':forms.TextInput(attrs={'class': 'form-control'}), 
                    'projeto_cod':forms.Select(attrs={'class': 'form-control'}), 
                    'clima':forms.Select(attrs={'class': 'form-control'}), 
                    'inicio':forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}), 
                    'termino':forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}), 
                    'inicio_pt':forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}), 
                    'termino_pt':forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}), 
                }
        
        labels = {
            **PlanejamentoForm.Meta.labels,
            'AS':_('AS'),
            'encarregado':_('Encarregado'),
            'projeto_cod':_('Cód do Projeto'),
            'clima':_('Clima'),
            'inicio':_('Ínicio'),
            'termino':_('Término'),
            'inicio_pt':_('Ínicio PT'),
            'termino_pt':_('Término PT'),
        }
class ASForm(PlanejamentoForm):
    def __init__(self, *args, **kwargs):
        super(ASForm, self).__init__(*args, **kwargs)
   
    class Meta(PlanejamentoForm.Meta):
        model = AS
        fields = PlanejamentoForm.Meta.fields  
        widgets = PlanejamentoForm.Meta.widgets
        labels = PlanejamentoForm.Meta.labels

class ItemForm(forms.ModelForm):
    disciplina = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),label=_('Disciplina'),choices=DISCIP)
    cod_contrato = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label=_('Código item'),required=False)
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
  

    class Meta:
        model = ItemMedicao 

        fields = ('disciplina','cod_contrato','item_contrato','qtd','total','efetivo',
                  'qtd_t','qtd_e','qtd_pranchao','qtd_piso','montagem','placa')
        widgets = {
            'item_contrato':forms.Select(attrs={'class': 'form-control'}), 
            'qtd':forms.TextInput(attrs={'class': 'form-control'}), 
            'total':forms.TextInput(attrs={'class': 'form-control'}), 
            'efetivo':forms.TextInput(attrs={'class': 'form-control'}), 
            'qtd_t':forms.TextInput(attrs={'class': 'form-control'}), 
            'qtd_e':forms.TextInput(attrs={'class': 'form-control'}), 
            'qtd_pranchao':forms.TextInput(attrs={'class': 'form-control'}), 
            'qtd_piso':forms.TextInput(attrs={'class': 'form-control'}), 
            'montagem':forms.Select(attrs={'class': 'form-control'}), 
            'placa':forms.TextInput(attrs={'class': 'form-control'}), 
        }
        labels = {

            'item_contrato': _('Item Contrato'),
            'qtd': _('Quantidade'),
            'total': _('valor total'),
            'efetivo': _('Efetivo'),
            'qtd_t': _('Qtd Tubo'),
            'qtd_e': _('Qtd Encaixe'),
            'qtd_pranchao': _('Qtd Pranchão'),
            'qtd_piso': _('Qtd Piso'),
            'montagem': _('Montagem/Desmontagem'),
            'placa': _('Placa'),
        }
    
ItemFormSet = inlineformset_factory(
    RDO, ItemMedicao, form=ItemForm, extra=1, can_delete=True)