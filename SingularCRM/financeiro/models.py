from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.urls import reverse_lazy
from django.template.defaultfilters import date

import locale
locale.setlocale(locale.LC_ALL, '')

STATUS_CONTA_SAIDA_ESCOLHAS = (
    (u'0', u'Paga'),
    (u'1', u'A pagar'),
    (u'2', u'Atrasada'),
)

STATUS_CONTA_ENTRADA_ESCOLHAS = (
    (u'0', u'Recebida'),
    (u'1', u'A receber'),
    (u'2', u'Atrasada'),
)

TIPO_GRUPO_ESCOLHAS = (
    (u'0', u'Entrada'),
    (u'1', u'Saída'),
)
class PlanoContasGrupo(models.Model):
    codigo = models.CharField(max_length=6)
    tipo_grupo = models.CharField(max_length=1, choices=TIPO_GRUPO_ESCOLHAS)
    descricao = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Grupo do Plano de Contas"
    def __unicode__(self):
        s = u'%s' % (self.descricao)
        return s
    def __str__(self):
        s = u'%s' % (self.descricao)
        return s

class PlanoContasSubgrupo(PlanoContasGrupo):
    grupo = models.ForeignKey('financeiro.PlanoContasGrupo',related_name="subgrupos", on_delete=models.CASCADE)

class Lancamento(models.Model):
    data_vencimento = models.DateField(null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    descricao = models.CharField(max_length=255)
    valor_liquido = models.DecimalField(max_digits=13, decimal_places=2, validators=[
                                        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    movimentar_caixa = models.BooleanField(default=True)
    movimento_caixa = models.ForeignKey(
        'financeiro.MovimentoCaixa', related_name="movimento_caixa_lancamento", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Lançamento"
    def format_valor_liquido(self):
        return locale.format(u'%.2f', self.valor_liquido, 1)
    @property
    def format_data_vencimento(self):
        return '%s' % date(self.data_vencimento, "d/m/Y")
    @property
    def format_data_pagamento(self):
        return '%s' % date(self.data_pagamento, "d/m/Y")
    
class Entrada(Lancamento):
    status = models.CharField(
        max_length=1, choices=STATUS_CONTA_ENTRADA_ESCOLHAS, default='1')
    grupo_plano = models.ForeignKey(
        'financeiro.PlanoContasGrupo', related_name="grupo_plano_recebimento", on_delete=models.SET_NULL, null=True, blank=True)

    def get_edit_url(self):
        if self.status == '0':
            return reverse_lazy('financeiro:editarrecebimentoview', kwargs={'pk': self.id})
        else:
            return reverse_lazy('financeiro:editarcontareceberview', kwargs={'pk': self.id})
    def get_tipo(self):
        return 'Entrada'

class Saida(Lancamento):
    status = models.CharField(
        max_length=1, choices=STATUS_CONTA_SAIDA_ESCOLHAS, default='1')
    grupo_plano = models.ForeignKey(
        'financeiro.PlanoContasGrupo', related_name="grupo_plano_pagamento", on_delete=models.SET_NULL, null=True, blank=True)

    def get_edit_url(self):
        if self.status == '0':
            return reverse_lazy('financeiro:editarpagamentoview', kwargs={'pk': self.id})
        else:
            return reverse_lazy('financeiro:editarcontapagarview', kwargs={'pk': self.id})
    def get_tipo(self):
        return 'Saida'
    
class MovimentoCaixa(models.Model):
    data_movimento = models.DateField(null=True, blank=True)
    saldo_inicial = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0.00'))
    saldo_final = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0.00'))
    entradas = models.DecimalField(max_digits=13, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    saidas = models.DecimalField(max_digits=13, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    class Meta:
        verbose_name = "Movimento de Caixa"
        permissions = (
            ("acesso_fluxodecaixa", "Pode acessar o Fluxo de Caixa"),
        )
    @property
    def format_data_movimento(self):
        return '%s' % date(self.data_movimento, "d/m/Y")
    @property
    def valor_lucro_prejuizo(self):
        return self.saldo_final - self.saldo_inicial
    def __unicode__(self):
        s = u'Movimento dia %s' % (self.data_movimento)
        return s
    def __str__(self):
        s = u'Movimento dia %s' % (self.data_movimento)
        return s