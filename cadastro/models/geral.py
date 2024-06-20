from django.db import models


TIPO_APROV = (  ('BMF','BMF'),
                ('DMS','DMS'),              
)

class Contrato(models.Model):
    contrato = models.CharField(max_length=50, unique=True)
    class Meta:
        ordering = ('contrato',)
    def __str__(self):
        return self.contrato

class Area(models.Model):
    area = models.CharField(max_length=30, unique=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    class Meta:
        ordering = ('area',)
    def __str__(self):
        return self.area

class Solicitante(models.Model):
    solicitante = models.CharField(max_length=30, unique=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    class Meta:
        ordering = ('solicitante',)
    def __str__(self):
        return self.solicitante
    
class Aprovador(models.Model):
    aprovador = models.CharField(max_length=255, unique=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    class Meta:
        ordering = ('aprovador',)
    def __str__(self):
        return self.aprovador
class EtapaAprovacao(models.Model):
    aprovador = models.ForeignKey(
        Aprovador, related_name="etapa_aprovacao", on_delete=models.CASCADE)
    etapa = models.CharField(max_length=255)
    
DISCIP = (
    ('ANDAIME','ANDAIME'),
    ('PINTURA','PINTURA'),
    ('ISOLAMENTO','ISOLAMENTO'),
    ('GERAL','GERAL'),
)
UND = (
    ('M','M'),
    ('M2','M2'),
    ('M3','M3'),
    ('UN','UN'),
    ('VAL','VAL'),
    ('H','H'),
)
class ItemBm(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    item_ref = models.CharField(max_length=10,unique=True)
    disciplina = models.CharField(max_length=20,choices=DISCIP)
    descricao = models.CharField(max_length=200)
    und = models.CharField(max_length=3, choices=UND)
    preco_item = models.DecimalField('Preço', max_digits=11, decimal_places=3)
    obs = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return self.descricao
