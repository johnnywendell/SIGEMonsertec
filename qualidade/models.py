import os
from django.db import models
from cadastro.models.geral import Solicitante, Area
from cadastro.models.base import TimeStampedModel


CORROS = (
    ('N/A','N/A'),
    ('C1','C1'),
    ('C2','C2'),
    ('C3','C3'),
    ('C4','C4'),
    ('C5','C5'),
    ('C6','C6'),
)   
TIPOS = (
    ('PARADA','PARADA'),
    ('PROJETO','PROJETO'),
    ('NOTA','NOTA'),
    ('PLANO DE PINTURA','PLANO DE PINTURA'),
    ('INTEGRIDADE','INTEGRIDADE'),
    ('MANUTENCAO','MANUTENÇÃO'),
)
AMB =(
    ('INTERNO','INTERNO'),
    ('EXTERNO','EXTERNO')
)
CHECK =(
    ('0','APROVADO'),
    ('1','REPROVADO')
)
class Relatorio(TimeStampedModel):
    cliente = models.CharField('Cliente',max_length=15, blank=True, null=True)
    data = models.DateField(verbose_name='Data serviço')
    rec = models.CharField(max_length=50, blank=True, null=True)
    nota = models.CharField('Nota',max_length=50, blank=True, null=True)
    tag = models.CharField('Tag',max_length=50, blank=True, null=True)
    tipo_serv = models.CharField('Tipo serviço',max_length=20, choices=TIPOS)
    unidade = models.ForeignKey(Area, on_delete=models.SET_NULL, related_name='areaa', blank=True, null=True)
    setor = models.CharField('Setor',max_length=50, blank=True, null=True)
    corrosividade = models.CharField(max_length=15, choices=CORROS)
    fiscal = models.CharField('Fiscal',max_length=50, blank=True, null=True)
    inspetor = models.CharField('inspetor',max_length=50, blank=True, null=True)

    inicio = models.DateTimeField(verbose_name='Inicio', blank=True, null=True)
    termino = models.DateTimeField(verbose_name='Fim', blank=True, null=True)
    tratamento = models.CharField('Tratamento',max_length=50, blank=True, null=True)
    tipo_subs = models.CharField('Tipo do substrato',max_length=50, blank=True, null=True)
    
    temp_ambiente = models.CharField('Temperatura ambiente', blank=True, null=True,max_length=20)
    ura = models.CharField('Úmidade relativa', blank=True, null=True,max_length=20)
    po = models.CharField('Ponto de Orvalho', blank=True, null=True,max_length=20)
    temp_super = models.CharField('Temperatura da superfície', blank=True, null=True,max_length=20)
    intemperismo = models.CharField('Grau de intemperismo',max_length=2, blank=True, null=True)
    descontaminacao = models.CharField('Descontaminação',max_length=20, blank=True, null=True)
    poeira_tam = models.CharField('Teste de poeira tamanho',max_length=10, blank=True, null=True)
    poeira_quant = models.CharField('Teste de poeira quantidade',max_length=10, blank=True, null=True)
    teor_sais = models.CharField('Teor sais soluveis na superfície',max_length=10, blank=True, null=True)
    ambiente_pintura = models.CharField('Ambiente pintura',max_length=30, blank=True, null=True,choices=AMB)
    rugosidade = models.CharField('Rugosidade', blank=True, null=True,max_length=20)
    laudo = models.BooleanField(default=True)

    rnc_n = models.BooleanField('RNC?',default=False)
    obs_inst = models.TextField('Instrumentos de medição',blank=True, null=True)
    obs_final = models.TextField('Observações finais', blank=True, null=True)
    aprovado = models.BooleanField(default=True)

    class Meta:
        ordering = ('pk',)
    def get_data(self):
        return self.data.strftime('%d/%m/%Y')
    def get_inicio(self):
        return self.inicio.strftime('%d/%m/%Y')
    def get_termino(self):
        return self.termino.strftime('%d/%m/%Y')
    def __str__(self):
        return super().__str__()
    
   
    
class EtapaPintura(models.Model):
    rip_n = models.ForeignKey(Relatorio, on_delete=models.CASCADE, related_name='relatorios')
    tinta = models.CharField(max_length=20, blank=True, null=True)
    lote_a = models.CharField(max_length=20, blank=True, null=True)
    val_a = models.DateField(verbose_name='Validade lote A', blank=True, null=True)
    lote_b = models.CharField(max_length=20, blank=True, null=True)
    val_b = models.DateField(verbose_name='Validade lote B', blank=True, null=True)
    lote_c = models.CharField(max_length=20, blank=True, null=True)
    val_c = models.DateField(verbose_name='Validade lote C', blank=True, null=True)
    cor_munsell = models.CharField(max_length=20, blank=True, null=True)
    temp_amb = models.CharField('Temp. ambiente', blank=True, null=True,max_length=20)
    ura = models.CharField('Úmidade relativa', blank=True, null=True,max_length=20)
    po = models.CharField('Ponto de Orvalho', blank=True, null=True,max_length=20)
    temp_substrato = models.CharField('Temperatura da substrato', blank=True, null=True,max_length=20)
    diluente = models.CharField(max_length=20, blank=True, null=True)
    met_aplic = models.CharField(max_length=20, blank=True, null=True)
    inicio = models.DateTimeField(verbose_name='Inicio', blank=True, null=True)
    termino = models.DateTimeField(verbose_name='Fim', blank=True, null=True)
    inter_repintura = models.CharField(max_length=20, blank=True, null=True)
    epe = models.CharField('Espessura especificada', blank=True, null=True,max_length=20)
    eps = models.CharField('Espessura seca', blank=True, null=True,max_length=20)
    insp_visual = models.CharField(default=True,choices=CHECK,max_length=20, blank=True, null=True)
    aderencia = models.CharField(max_length=20, blank=True, null=True)
    holiday = models.CharField(max_length=20, blank=True, null=True)
    laudo = models.CharField(default=True,choices=CHECK,max_length=20)
    data_insp = models.DateField(verbose_name='Data inspeção', blank=True, null=True)
    pintor = models.CharField("Matrícula Executante",max_length=30, blank=True, null=True)

    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return str(self.tinta)
    def get_data_insp(self):
        return self.data_insp.strftime('%d/%m/%Y')
    def get_inicio(self):
        return self.inicio.strftime('%d/%m/%Y')
    def get_termino(self):
        return self.termino.strftime('%d/%m/%Y')
    def get_val_a(self):
        return self.val_a.strftime('%d/%m/%Y')
    def get_val_b(self):
        return self.val_b.strftime('%d/%m/%Y')
    def get_val_c(self):
        return self.val_c.strftime('%d/%m/%Y')

def logo_directory_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return 'imagens/relatorio/registro_{0}_{1}{2}'.format(instance.rip_numero, instance.id, extension)   

class Photo(models.Model):
    rip_numero = models.ForeignKey(Relatorio, on_delete=models.CASCADE, verbose_name='RIP',related_name='relatorio')
    photo = models.ImageField('foto',upload_to=logo_directory_path, default='imagens/logo.png', blank=True, null=True)
    class Meta:
        ordering =('pk',)
        verbose_name = 'foto'
        verbose_name_plural = 'fotos'

    def __unicode__(self):
        return u'%s' % self.photo

    def __str__(self):
        return u'%s' % self.photo
    
    def delete(self, using=None, keep_parents=False):
        os.remove(self.photo.path)
        return super().delete(using, keep_parents)



CHOICE = (
    ('N/A','N/A'),
    ('SIM','SIM'),
    ('NÃO','NÃO'),
)

class RelatorioArea(Relatorio):
    m2 = models.DecimalField('Metro quadrado', max_digits=6, decimal_places=2, blank=True, null=True)
    calha_utec = models.CharField("Todos pontos de contato foram instalados calha tipo Utec?",max_length=5, choices=CHOICE)
    guia_pc = models.CharField("Foram pintados os guias e os pontos de contatos da tubulação?",max_length=5, choices=CHOICE)
    fita_protec = models.CharField("Aplicado fita de proteção nos pontos com grampos de fixação?",max_length=5, choices=CHOICE)    
    trecho_rec = models.CharField("Foi pintado todos trechos recomendados da REC?",max_length=5, choices=CHOICE)
    elastomero = models.CharField("Foi Aplicado elastômero nos acessórios?",max_length=5, choices=CHOICE)  
    volante_caps = models.CharField("Foram pintados todos os volantes e caps?",max_length=5, choices=CHOICE)
    def __str__(self):
        return '{}/{}'.format(str(self.id).zfill(4),self.data.strftime('%Y'))

class RelatorioJato(Relatorio):
    def __str__(self):
        return 'J{}/{}'.format(str(self.id).zfill(4),self.data.strftime('%Y'))

    
