from django.urls import path
from . import views as v

app_name = 'planejamento'

urlpatterns = [

    # RDO's
    # cadastro/empresa/adicionar/
    path(r'rdo/adicionar/',
        v.AdicionarRDOView.as_view(), name='addrdoview'),
    # cadastro/empresa/listaempresas
    path(r'rdo/listardos/',
        v.RDOListView.as_view(), name='listardoview'),
    # cadastro/empresa/editar/
    path(r'rdo/editar/<int:pk>/',
        v.EditarRDOView.as_view(), name='editarrdoview'),
    
    # BOLETIM DE MEDIÇÃO
    path(r'boletimmedicao/adicionar/',
        v.AdicionarBoletimMedicaoRDOView.as_view(), name='addbmview'),
    path(r'boletimmedicao/listabms/',
        v.BoletimMedicaoListView.as_view(), name='listabmview'),
    path(r'boletimmedicao/editar/<int:pk>/',
        v.EditarBoletimMedicaoView.as_view(), name='editarbmview'),
    path(r'boletimmedicao/atualizar-materiais/', v.atualizar_romaneios_selecionados, name='atualizar_romaneios'),
    path(r'boletimmedicao/pdf/<int:pk>/', v.render_pdf_view, name='render_pdf_view'),

    # CÓDIGO DE PROJETOS
    path(r'projeto/adicionar/',
        v.AdicionarProjetoView.as_view(), name='addprojetoview'),
    # cadastro/empresa/listaempresas
    path(r'projeto/listaprojetos/',
        v.ProjetoListView.as_view(), name='listaprojetoview'),
    # cadastro/empresa/editar/
    path(r'projeto/editar/<int:pk>/',
        v.EditarProjetoView.as_view(), name='editarprojetoview'),


]