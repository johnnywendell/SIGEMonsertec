
from django.urls import path
from . import views


app_name = 'financeiro'
urlpatterns = [
    # Plano de contas
    # financeiro/planodecontas
    path(r'planodecontas/', views.PlanoContasView.as_view(), name='planocontasview'),
    # financeiro/planodecontas/adicionargrupo/
    path(r'planodecontas/adicionargrupo/',views.AdicionarGrupoPlanoContasView.as_view(), name='addgrupoview'),
    # financeiro/planodecontas/editargrupo/
    path(r'planodecontas/editargrupo/<int:pk>/',views.EditarGrupoPlanoContasView.as_view(), name='editargrupoview'),

    # Fluxo de caixa
    # financeiro/fluxodecaixa
    path(r'fluxodecaixa/', views.FluxoCaixaView.as_view(), name='fluxodecaixaview'),

    # Pagamentos
    # financeiro/pagamento/adicionar/
    path(r'pagamento/adicionar/',
        views.AdicionarSaidaView.as_view(), name='addpagamentoview'),
    # financeiro/pagamento/listacontapagar
    path(r'pagamento/listapagamento/',
        views.SaidaListView.as_view(), name='listapagamentosview'),
    # financeiro/pagamento/editar/
    path(r'pagamento/editar/<int:pk>/',
        views.EditarSaidaView.as_view(), name='editarpagamentoview'),

    # Recebimentos
    # financeiro/recebimento/adicionar/
    path(r'recebimento/adicionar/',
        views.AdicionarEntradaView.as_view(), name='addrecebimentoview'),
    # financeiro/recebimento/listarecebimento
    path(r'recebimento/listarecebimento/',
        views.EntradaListView.as_view(), name='listarecebimentosview'),
    # financeiro/recebimento/editar/
    path(r'recebimento/editar/<int:pk>/',
        views.EditarEntradaView.as_view(), name='editarrecebimentoview'),

     # Contas a pagar
    # financeiro/contapagar/adicionar/
    path(r'contapagar/adicionar/',
        views.AdicionarContaPagarView.as_view(), name='addcontapagarview'),
    # financeiro/contapagar/listacontapagar
    path(r'contapagar/listacontapagar/',
        views.ContaPagarListView.as_view(), name='listacontapagarview'),
    # financeiro/contapagar/editar/
    path(r'contapagar/editar/<int:pk>/',
        views.EditarContaPagarView.as_view(), name='editarcontapagarview'),
    # financeiro/contapagar/listacontapagar/atrasadas/
    path(r'contapagar/listacontapagar/atrasadas/',
        views.ContaPagarAtrasadasListView.as_view(), name='listacontapagaratrasadasview'),
    # financeiro/contapagar/listacontapagar/hoje/
    path(r'contapagar/listacontapagar/hoje/',
        views.ContaPagarHojeListView.as_view(), name='listacontapagarhojeview'),

    # Contas a receber
    # financeiro/contareceber/adicionar/
    path(r'contareceber/adicionar/',
        views.AdicionarContaReceberView.as_view(), name='addcontareceberview'),
    # financeiro/contareceber/listacontapagar
    path(r'contareceber/listacontareceber/',
        views.ContaReceberListView.as_view(), name='listacontareceberview'),
    # financeiro/contareceber/editar/
    path(r'contareceber/editar/<int:pk>/',
        views.EditarContaReceberView.as_view(), name='editarcontareceberview'),
    # financeiro/contareceber/listacontapagar/atrasadas/
    path(r'contareceber/listacontareceber/atrasadas/',
        views.ContaReceberAtrasadasListView.as_view(), name='listacontareceberatrasadasview'),
    # financeiro/contareceber/listacontapagar/hoje/
    path(r'contareceber/listacontareceber/hoje/',
        views.ContaReceberHojeListView.as_view(), name='listacontareceberhojeview'),

    # Lancamentos
    # Gerar lancamento
    path(r'gerarlancamento/', views.GerarLancamentoView.as_view(),
        name='gerarlancamento'),
    # Lista todos lancamentos
    path(r'lancamentos/', views.LancamentoListView.as_view(),
        name='listalancamentoview'),
]


