# -*- coding: utf-8 -*-

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from cadastro.models.base import Pessoa, Telefone, Email
from cadastro.models.geral import EtapaAprovacao, Aprovador

class TelefoneForm(forms.ModelForm):

    class Meta:
        model = Telefone
        fields = ('tipo_telefone', 'telefone',)
        labels = {
            'tipo_telefone': _("Telefone"),
            'telefone': _(''),
        }
        widgets = {
            'tipo_telefone': forms.Select(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmailForm(forms.ModelForm):

    class Meta:
        model = Email
        fields = ('email',)
        labels = {
            'email': _('Email')
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class EtapaAprovacaoForm(forms.ModelForm):
    class Meta:
        model = EtapaAprovacao
        fields = ('etapa',)
        labels = {
            'etapa': _('DOC/Etapa')
        }
        widgets = {
            'etapa': forms.TextInput(attrs={'class': 'form-control'}),
        }

EtapaAprovacaoFormSet = inlineformset_factory(
    Aprovador, EtapaAprovacao, form=EtapaAprovacaoForm, extra=1, can_delete=True)
TelefoneFormSet = inlineformset_factory(
    Pessoa, Telefone, form=TelefoneForm, extra=1, can_delete=True)
EmailFormSet = inlineformset_factory(
    Pessoa, Email, form=EmailForm, extra=1, can_delete=True)

