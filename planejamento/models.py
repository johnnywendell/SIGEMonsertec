from django.db import models
from cadastro.models.geral import Contrato, Area, Solicitante, ItemBm, Aprovador
from cadastro.models.base import TimeStampedModel
from django.db.models.signals import pre_save, post_save
from django.utils import timezone

class ProjetoCodigo(models.Model):
    projeto_nome = models.CharField(max_length=30, unique=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return '{} --- {}'.format(self.pk,self.projeto_nome)

TIPO = (
    ('PARADA','PARADA'),
    ('PACOTE','PACOTE'),
    ('ROTINA','ROTINA'),
    ('PROJETO','PROJETO'),
)
DISCIP = (
    ('ANDAIME','ANDAIME'),
    ('PINTURA','PINTURA'),
    ('ISOLAMENTO','ISOLAMENTO'),
    ('GERAL','GERAL'),
)
CLIMA = (
    ('BOM','BOM'),
    ('NUBLADO','NUBLADO'),
    ('CHUVOSO','CHUVOSO'),
)

BM_STATUS = (  ('APROVADO','APROVADO'),
                ('AGUARDANDO OM','AGUARDANDO OM'),
                ('EM LANÇAMENTO','EM LANÇAMENTO'),
                ('NÃO APROVADO','NÃO APROVADO'),
                ('REPROVADO','REPROVADO'),
) 
PGT_STATUS = (  ('EMITIR NF','EMITIR NF'),
                ('ABAT REAJUSTE','ABAT REAJUSTE'),
) 
MED_STATUS = (  ('NORMAL','NORMAL'),
                ('ANTECIPAÇÃO','ANTECIPAÇÃO'),
                ('PROJEÇÃO','PROJEÇÃO'),
                ('PREST DE CONTAS','PRESTAÇÃO DE CONTAS'),
) 
class BoletimMedicao(TimeStampedModel):
    unidade = models.ForeignKey(Area, on_delete=models.CASCADE)
    periodo_inicio = models.DateField(verbose_name='Período início')
    periodo_fim = models.DateField(verbose_name='Período fim')
    status_pgt = models.CharField(max_length=20,choices=PGT_STATUS, blank=True, null=True)
    status_med = models.CharField(max_length=20,choices=MED_STATUS, blank=True, null=True)

    d_numero = models.CharField('DMS',max_length=40, blank=True, null=True)
    d_data = models.DateField(verbose_name='DMS data', blank=True, null=True)
    d_aprovador = models.ForeignKey(Aprovador, on_delete=models.SET_NULL, blank=True, null=True,related_name='aprovadordms')
    d_status = models.CharField('Status DMS',max_length=20,choices=BM_STATUS, blank=True, null=True)
    b_numero = models.CharField('BMS',max_length=40, blank=True, null=True)
    b_data = models.DateField(verbose_name='BMS data ', blank=True, null=True)
    b_aprovador = models.ForeignKey(Aprovador, on_delete=models.SET_NULL, blank=True, null=True,related_name='aprovadorbms')
    b_status = models.CharField('Status BMS',max_length=20,choices=BM_STATUS, blank=True, null=True)
    
    descricao = models.CharField('Descricao do serviço',max_length=120)
    #frs = models.ForeignKey(FRS, on_delete=models.CASCADE, blank=True, null=True, related_name='frs')
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=3, blank=True, null=True)
    follow_up = models.TextField('Obs/followup', blank=True, null=True)
    rev = models.IntegerField('Revisão',default=0, blank=True, null=True)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return 'BM Nº{}'.format(str(self.pk).zfill(5))
    def get_inicio(self):
        return self.periodo_inicio.strftime('%d/%m/%Y')
    def get_fim(self):
        return self.periodo_fim.strftime('%d/%m/%Y')

class PlanejamentoModel(TimeStampedModel):
    data = models.DateField(verbose_name='Período')
    unidade = models.ForeignKey(Area, on_delete=models.SET_NULL, blank=True, null=True)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.SET_NULL, blank=True, null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    escopo = models.CharField('Escopo do serviço',max_length=200)
    local = models.CharField('Local do serviço',max_length=200)
    tipo = models.CharField('Tipo Serviço',max_length=20,choices=TIPO)
    doc = models.FileField('documento',upload_to='planejamento/', max_length=100, blank=True, null=True)
    slug = models.SlugField(default="", null=False)
    disciplina = models.CharField(max_length=20,choices=DISCIP)
    obs = models.TextField('Obs', blank=True, null=True)
    aprovado = models.BooleanField(default=False)

    def get_data(self):
        return self.data.strftime('%d/%m/%Y')
    class Meta:
        abstract = True

class AS(PlanejamentoModel):
    class Meta:
        ordering = ('-pk',)
    def __str__(self):
        return 'AS Nº{}/{}'.format(str(self.pk).zfill(5),self.data.strftime('%Y'))
    
class RDO(PlanejamentoModel):
    AS = models.ForeignKey(AS, on_delete=models.SET_NULL, blank=True, null=True, related_name='ass',verbose_name='AS')
    encarregado = models.CharField('Encarregado',max_length=100, blank=True, null=True)
    projeto_cod = models.ForeignKey(ProjetoCodigo, on_delete=models.SET_NULL, blank=True, null=True,verbose_name='Cód. Projetos')
    clima = models.CharField('Clima',max_length=20,choices=CLIMA)
    inicio = models.TimeField(verbose_name='Inicio',blank=True, null=True)
    termino = models.TimeField(verbose_name='Fim',blank=True, null=True)
    inicio_pt = models.TimeField(verbose_name='Inicio PT',blank=True, null=True)
    termino_pt = models.TimeField(verbose_name='Término PT',blank=True, null=True)
    class Meta:
        ordering = ('-pk',)
    def __str__(self):
        return 'RDO Nº{}/{}'.format(str(self.pk).zfill(5),self.data.strftime('%Y'))


MONTAGEM = (
    ('MONTAGEM','MONTAGEM'),
    ('DESMONTAGEM','DESMONTAGEM'),
)

class ItemMedicao(models.Model):
    doc_origem = models.ForeignKey(RDO, on_delete=models.CASCADE, related_name='rdos')
    item_contrato = models.ForeignKey(ItemBm, on_delete=models.CASCADE, blank=True, null=True)
    qtd = models.DecimalField('qtd', max_digits=12, decimal_places=3)
    total = models.DecimalField('total', max_digits=12, decimal_places=3)

    efetivo = models.DecimalField('Efetivo', max_digits=12, decimal_places=3, blank=True, null=True)
    qtd_t = models.DecimalField('Tubo', max_digits=12, decimal_places=3, blank=True, null=True)
    qtd_e = models.DecimalField('Encaixe', max_digits=12, decimal_places=3, blank=True, null=True)
    qtd_pranchao = models.DecimalField('Pranchão', max_digits=12, decimal_places=3, blank=True, null=True)
    qtd_piso = models.DecimalField('Piso', max_digits=12, decimal_places=3, blank=True, null=True)
    montagem = models.CharField('Tipo',max_length=20,choices=MONTAGEM, blank=True, null=True)
    placa = models.CharField('Placa',max_length=30, blank=True, null=True)

##############################################################################################
import string, random
from django.utils.text import slugify 
  
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size)) 
  
def unique_slug_generator(instance, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.escopo) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 6)) 
        return unique_slug_generator(instance, new_slug = new_slug) 
    return slug 

def pre_save_receiver(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_slug_generator(instance) 
  
pre_save.connect(pre_save_receiver, sender = RDO)

pre_save.connect(pre_save_receiver, sender = AS)
