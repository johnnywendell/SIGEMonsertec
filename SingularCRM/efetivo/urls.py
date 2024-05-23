from django.urls import path
from . import views as v
from cadastro.views.import_csv import import_csv_colaboradores 

app_name = 'efetivo'

urlpatterns = [

    path(r'apontamento/adicionar/',
        v.AdicionarApontamentoView.as_view(), name='addapontamentoview'),
    path(r'apontamento/listaapontamentos/',
        v.ApontamentoListView.as_view(), name='listaapontamentoview'),
    path(r'apontamento/editarpontamento/<int:pk>/',
        v.EditarApontamentoView.as_view(), name='editarapontamentoview'),
    path(r'apontamento/copiarpontamento/<int:pk>/',
        v.GerarCopiaApontamentoView.as_view(), name='copiarapontamento'),

    # Colaborador
    path(r'colaborador/adicionarcolaborador/',
        v.AdicionarColaboradorView.as_view(), name='addcolaboradorview'),
    path(r'colaborador/listacolaborador/',
        v.ColaboradorListView.as_view(), name='listacolaboradoreview'),
    path(r'colaborador/editarcolaborador/<int:pk>/',
        v.EditarColaboradorView.as_view(), name='editarcolaboradorview'),
    path(r'colaborador/importarcolaborador/',
        import_csv_colaboradores, name='importar_csv_colaborador'),

]