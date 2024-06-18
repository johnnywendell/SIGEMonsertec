from django.db import models
from cadastro.models.geral import Area, Solicitante, ItemBm
from cadastro.models.base import TimeStampedModel

class Romaneio(TimeStampedModel):
    entrada = models.DateField(verbose_name='Data de Entrada')
    nf = models.CharField('NF',max_length=15, blank=True, null=True)
    documento = models.CharField('documento referência', max_length=20, blank=True, null=True)
    obs = models.CharField('Obs',blank=True, null=True, max_length=40)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL,blank=True, null=True)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.SET_NULL, blank=True, null=True)
    concluido =  models.BooleanField(default=False)
    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return '{}/{}'.format(str(self.pk).zfill(4),self.entrada.strftime('%Y'))
    def get_entrada(self):
        return self.entrada.strftime('%d/%m/%Y')
    def nf_formated(self):
        return str(self.nf).zfill(8)

MATERIAIS = (
    ('perfil_I','perfil_I'),
    ('perfil_H','perfil_H'),
    ('perfil_U','perfil_U'),
    ('perfil_L','perfil_L'),
    ('barra_chata','barra_chata'),
    ('tubulacao','tubulacao'),
    ('acess_T','acess_T'),
    ('acess_FLG','acess_FLG'),
    ('acess_RED','acess_RED'),
    ('acess_CV90','acess_CV90'),
    ('acess_CV45','acess_CV45'),
    ('acess_VV','acess_VV'),
    ('acess_VVC','acess_VVC'),
    ('acess_CAP','acess_CAP'),
    ('boleado','boleado'),
    ('carretel','carretel'),
    ('cubo','cubo'),
    ('cone','cone'),
    ('janela','janela'),
)   
class Material(models.Model):
    n_romaneio = models.ForeignKey(Romaneio, on_delete=models.CASCADE, related_name='romaneios')
    jato = models.ForeignKey(ItemBm, on_delete=models.SET_NULL, blank=True, null=True, related_name='itemjato')
    tf = models.ForeignKey(ItemBm, on_delete=models.SET_NULL, blank=True, null=True, related_name='itemtf')
    ti = models.ForeignKey(ItemBm, on_delete=models.SET_NULL, blank=True, null=True, related_name='itemti')
    ta = models.ForeignKey(ItemBm, on_delete=models.SET_NULL, blank=True, null=True, related_name='itemta')
    cor = models.CharField(max_length=15, blank=True, null=True)
    material = models.CharField(max_length=15, choices=MATERIAIS)
    descricao = models.CharField('Descrição',max_length=30, blank=True, null=True)
    polegada = models.CharField('Pol', max_length=4, blank=True, null=True)
    m_quantidade = models.DecimalField('M/QTD', max_digits=7, decimal_places=2, blank=True, null=True)
    m2 = models.DecimalField('M²', max_digits=7, decimal_places=3)

    raio = models.DecimalField('raio', max_digits=7, decimal_places=2, blank=True, null=True)
    largura = models.DecimalField('largura', max_digits=7, decimal_places=2, blank=True, null=True)
    altura = models.DecimalField('altura', max_digits=7, decimal_places=2, blank=True, null=True)
    comprimento = models.DecimalField('comprimento/lados', max_digits=7, decimal_places=2, blank=True, null=True)
    lados = models.DecimalField('QTD', max_digits=7, decimal_places=2, blank=True, null=True)
    relatorio = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return str(self.pk)
