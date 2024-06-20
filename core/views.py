from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Sum, Count, Q
from efetivo.models import Apontamento, ApontamentoColaborador, Colaborador

from .views_mixins import SessionTimeoutMixin
from datetime import datetime,date
import calendar

class IndexView(SessionTimeoutMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        
        # Defina suas datas inicial e final conforme necessário
        data_atual = datetime.now().date()
        data_inicial = datetime.now().replace(day=1).date()
        ultimo_dia_mes = calendar.monthrange(date.today().year, date.today().month)[1]
        data_final = datetime.now().replace(day=ultimo_dia_mes).date()

        # QUERYS
        apontamentos_hoje = Apontamento.objects.filter(data=data_atual)
        lancamentos_do_dia = apontamentos_hoje.count()
        colaboradores_presentes_hoje = ApontamentoColaborador.objects.filter(apontamento__in=apontamentos_hoje,status='PRESENTE').count()
        colaboradores_faltas_hoje = ApontamentoColaborador.objects.filter(apontamento__in=apontamentos_hoje,status='FALTA').count()
        colaboradores_ferias_hoje = ApontamentoColaborador.objects.filter(apontamento__in=apontamentos_hoje,status='FERIAS').count()

        colaboradores_andaime = ApontamentoColaborador.objects.filter(apontamento__in=apontamentos_hoje,status='PRESENTE',
                                                                      apontamento__disciplina='AND').count()
        colaboradores_isolamento= ApontamentoColaborador.objects.filter(apontamento__in=apontamentos_hoje,status='PRESENTE',
                                                                      apontamento__disciplina='ISO').count()
        colaboradores_pintura = ApontamentoColaborador.objects.filter(apontamento__in=apontamentos_hoje,status='PRESENTE',
                                                                      apontamento__disciplina='PIN').count()

        context['data_atual'] = data_atual.strftime('%d/%m/%Y')

        context['quantidades_query'] = {
            'lancamentos_do_dia': 0 if not lancamentos_do_dia else lancamentos_do_dia,
            'colaboradores_presentes_hoje': 0 if not colaboradores_presentes_hoje else colaboradores_presentes_hoje,
            'colaboradores_faltas_hoje': 0 if not colaboradores_faltas_hoje else colaboradores_faltas_hoje,
            'colaboradores_ferias_hoje': 0 if not colaboradores_ferias_hoje else colaboradores_ferias_hoje,
            'colaboradores_andaime': 0 if not colaboradores_andaime else colaboradores_andaime,
            'colaboradores_isolamento': 0 if not colaboradores_isolamento else colaboradores_isolamento,
            'colaboradores_pintura': 0 if not colaboradores_pintura else colaboradores_pintura,
        }
        colaboradores_nao_apontados = Colaborador.objects.filter(
            ativo='1'  # Filtra apenas colaboradores ativos
        ).exclude(
            # Exclui colaboradores que foram apontados hoje
            Q(apontamentocolaborador__apontamento__data=data_atual)
        ).annotate(
            total_apontamentos=Count('apontamentocolaborador')
        )
        colaboradores_falta = Colaborador.objects.filter(
            apontamentocolaborador__status='1',  # Filtra colaboradores com status '1' (falta)
            apontamentocolaborador__apontamento__data=data_atual
        ).distinct()
        context['colaboradores_falta'] = colaboradores_falta
        context['colaboradores_nao_apontados'] = colaboradores_nao_apontados

        return context

def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
