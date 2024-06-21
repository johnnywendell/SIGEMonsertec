from django.db import models
from cadastro.models.geral import Area
from cadastro.models.base import TimeStampedModel
from planejamento.models import ProjetoCodigo

DISCIP = (
    ('AND', 'ANDAIME'),
    ('PIN', 'PINTURA'),
    ('ISO', 'ISOLAMENTO'),
)

STATUS = (
    ('PRESENTE', 'PRESENTE'),
    ('FALTA', 'FALTA'),
    ('TRANSFERIDO', 'TRANSFERIDO'),
    ('FÉRIAS', 'FÉRIAS'),
    ('EXAMES', 'EXAMES'),
    ('TREINAMENTO', 'TREINAMENTO'),
)
LIDER = (
    ('0', 'NÃO'),
    ('1', 'SIM'),
)

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=6, unique=True)
    funcao = models.CharField(max_length=100)
    ativo = models.CharField(max_length=2, choices=LIDER, default='1')

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return '{} - {}'.format(self.matricula, self.nome)

class Apontamento(TimeStampedModel):
    data = models.DateField(verbose_name='Período')
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    projeto_cod = models.ForeignKey(ProjetoCodigo, on_delete=models.CASCADE, verbose_name='Cód. Projetos')
    disciplina = models.CharField(max_length=20, choices=DISCIP)
    obs = models.CharField(max_length=255,null=True,blank=True)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return str(self.pk)
    
    def get_data(self):
        return self.data.strftime('%d/%m/%Y')
    
    
class ApontamentoColaborador(models.Model):
    apontamento = models.ForeignKey(Apontamento, related_name="apontamentos", on_delete=models.CASCADE)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS)
    lider = models.CharField(max_length=20, choices=LIDER, default='0')

    class Meta:
        unique_together = ('apontamento', 'colaborador')

    def __str__(self):
         return f'{self.apontamento} - {self.colaborador} - {self.get_status_display()} - {"Líder" if self.lider else ""}'
