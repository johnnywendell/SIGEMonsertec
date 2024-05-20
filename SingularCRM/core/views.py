from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Sum
from financeiro.models import MovimentoCaixa, Entrada, Saida

from datetime import datetime,date
import calendar

import matplotlib.pyplot as plt
import os
import io
import base64
import numpy as np
import tempfile 

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        
        # Defina suas datas inicial e final conforme necessário
        data_atual = datetime.now().date()
        data_inicial = datetime.now().replace(day=1).date()
        ultimo_dia_mes = calendar.monthrange(date.today().year, date.today().month)[1]
        data_final = datetime.now().replace(day=ultimo_dia_mes).date()

        # Filtra objetos entre as datas inicial e final
        movimentos = MovimentoCaixa.objects.filter(data_movimento__range=(data_inicial, data_final))

        # Obtém a soma dos valores de entrada e saída dos objetos filtrados
        soma_entradas = movimentos.aggregate(soma_entradas=Sum('entradas'))['soma_entradas']
        soma_saidas = movimentos.aggregate(soma_saidas=Sum('saidas'))['soma_saidas']

        context['data_atual'] = data_atual.strftime('%d/%m/%Y')

        context['quantidade_cadastro'] = {
            'entradas': 0.00 if not soma_entradas else "{:.2f}".format(soma_entradas),
            'saidas': 0.00 if not soma_saidas else"{:.2f}".format(soma_saidas),
        }

        # Contas atrasadas
        alertas = {
            'contas_receber_atrasadas': Entrada.objects.filter(data_vencimento__lte=data_atual, status__in=['1', '2']).count(),
            'contas_pagar_atrasadas': Saida.objects.filter(data_vencimento__lte=data_atual, status__in=['1', '2']).count()
        }
        context['alertas'] = alertas
        
        # Tenta encontrar o movimento do dia
        try:
            context['movimento_dia'] = MovimentoCaixa.objects.get(data_movimento=data_atual)
        except (MovimentoCaixa.DoesNotExist, ObjectDoesNotExist):
            ultimo_mvmt = MovimentoCaixa.objects.filter(data_movimento__lt=data_atual)
            context['saldo'] = ultimo_mvmt.latest('data_movimento').saldo_final if ultimo_mvmt else '0,00'

        # Gráfico
        movimentos = MovimentoCaixa.objects.filter(data_movimento__range=(data_inicial, data_final))

        # Agrupa os movimentos por data e calcula a soma das saídas e entradas por dia
        movimentos_diarios = movimentos.values('data_movimento').annotate(
            soma_entradas=Sum('entradas'), soma_saidas=Sum('saidas')
        )

        datas = [movimento['data_movimento'].strftime('%d/%m/%Y') for movimento in movimentos_diarios]
        entradas_diarias = [movimento['soma_entradas'] for movimento in movimentos_diarios]
        saidas_diarias = [movimento['soma_saidas'] for movimento in movimentos_diarios]

        # Configura a largura das barras
        largura_barra = 0.35
        indice = np.arange(len(datas))

        # Cria o gráfico de barras
        fig, ax = plt.subplots()
        ax.bar(indice - largura_barra/2, entradas_diarias, largura_barra, color='green', label='Entradas')
        ax.bar(indice + largura_barra/2, saidas_diarias, largura_barra, color='red', label='Saídas')
        ax.set_xlabel('Data')
        ax.set_ylabel('Valor')
        ax.set_title('Entradas e Saídas Dia a Dia')
        ax.set_xticks(indice)
        ax.set_xticklabels(datas, rotation=45, ha='right')
        ax.legend()

        # Adiciona legendas aos valores das barras
        for i in range(len(datas)):
            ax.text(indice[i] - largura_barra/2, entradas_diarias[i], "{:.2f}".format(entradas_diarias[i]), ha='center', va='bottom')
            ax.text(indice[i] + largura_barra/2, saidas_diarias[i], "{:.2f}".format(saidas_diarias[i]), ha='center', va='bottom')

        plt.tight_layout()
        # Salva o gráfico como um arquivo temporário
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_filename = temp_file.name
            plt.savefig(temp_filename, format='png')

        # Lê o arquivo temporário e converte em base64
        with open(temp_filename, 'rb') as img_file:
            graph_img = base64.b64encode(img_file.read()).decode()

        # Remove o arquivo temporário
        os.unlink(temp_filename)

        # Adiciona a imagem do gráfico ao contexto
        context['graph_img'] = 'data:image/png;base64,' + graph_img

        return context

def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
