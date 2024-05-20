from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
from .models import PlanoContasGrupo, PlanoContasSubgrupo, Saida, Entrada, STATUS_CONTA_ENTRADA_ESCOLHAS, STATUS_CONTA_SAIDA_ESCOLHAS



class PlanoContasGrupoForm(forms.ModelForm):
    class Meta:
        model = PlanoContasGrupo
        fields = ('tipo_grupo', 'descricao',)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_grupo': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao': _('Descrição'),
            'tipo_grupo': _('Tipo de lançamento'),
        }

class PlanoContasSubgrupoForm(forms.ModelForm):
    class Meta:
        model = PlanoContasSubgrupo
        fields = ('descricao',)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao': _('Descrição'),
        }
PlanoContasSubgrupoFormSet = inlineformset_factory(
    PlanoContasGrupo, PlanoContasSubgrupo, form=PlanoContasSubgrupoForm, fk_name='grupo', extra=1, can_delete=True)

class LancamentoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        
        super(LancamentoForm, self).__init__(*args, **kwargs)
        self.fields['valor_liquido'].localize = True

    class Meta:
        fields = ('descricao', 'grupo_plano', 'data_pagamento', 'data_vencimento',
                   'valor_liquido', 'movimentar_caixa',)
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'grupo_plano': forms.Select(attrs={'class': 'form-control'}),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'valor_liquido': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'movimentar_caixa': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao': _('Descrição'),
            'grupo_plano': _('Grupo (Plano de contas)'),
            'data_pagamento': _('Data do pagamento'),
            'data_vencimento': _('Data de vencimento'),
            'valor_liquido': _('Valor líquido'),
            'movimentar_caixa': _('Movimentar Caixa?'),
        }

class EntradaForm(LancamentoForm):
    def __init__(self, *args, **kwargs):
        super(EntradaForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = '0'

        if PlanoContasGrupo.objects.filter(tipo_grupo='0').count():
            self.fields['grupo_plano'].choices = ((grupo.id, str(grupo.codigo) + ' - ' + str(
                grupo.descricao)) for grupo in PlanoContasGrupo.objects.filter(tipo_grupo='0'))
        else:
            self.fields['grupo_plano'].choices = ((None, '----------'),)
    class Meta(LancamentoForm.Meta):
        model = Entrada
        fields = LancamentoForm.Meta.fields + ('status',)
        widgets = LancamentoForm.Meta.widgets
        widgets['status'] = forms.Select(
            attrs={'class': 'form-control', 'disabled': True})
        labels = LancamentoForm.Meta.labels
        labels['status'] = _('Status')

class SaidaForm(LancamentoForm):
    def __init__(self, *args, **kwargs):
        super(SaidaForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = '0'

        if PlanoContasGrupo.objects.filter(tipo_grupo='1').count():
            self.fields['grupo_plano'].choices = ((grupo.id, str(grupo.codigo) + ' - ' + str(
                grupo.descricao)) for grupo in PlanoContasGrupo.objects.filter(tipo_grupo='1'))
        else:
            self.fields['grupo_plano'].choices = ((None, '----------'),)

    class Meta(LancamentoForm.Meta):
        model = Saida
        fields = LancamentoForm.Meta.fields + ( 'status',)
        widgets = LancamentoForm.Meta.widgets
        widgets['status'] = forms.Select(
            attrs={'class': 'form-control', 'disabled': True})
        labels = LancamentoForm.Meta.labels
        labels['status'] = _('Status')

class ContaReceberForm(EntradaForm):

    def __init__(self, *args, **kwargs):
        super(ContaReceberForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = STATUS_CONTA_ENTRADA_ESCOLHAS
        self.fields['status'].initial = '1'
        self.fields['data_pagamento'].widget.attrs = {
            'class': 'form-control hidden', 'disabled': True, 'style': 'background-color:lightgrey;'}

class ContaPagarForm(SaidaForm):

    def __init__(self, *args, **kwargs):
        super(ContaPagarForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = STATUS_CONTA_SAIDA_ESCOLHAS
        self.fields['status'].initial = '1'
        self.fields['data_pagamento'].widget.attrs = {
            'class': 'form-control hidden', 'disabled': True, 'style': 'background-color:lightgrey;'}
