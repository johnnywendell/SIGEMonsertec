from django.urls import path
from .views import empresa, base, geral, import_csv

app_name = 'cadastro'

urlpatterns = [
    # Empresa
    path(r'empresa/adicionar/',
        empresa.AdicionarEmpresaView.as_view(), name='addempresaview'),
    path(r'empresa/listaempresas/',
        empresa.EmpresasListView.as_view(), name='listaempresasview'),
    path(r'empresa/editar/<int:pk>/',
        empresa.EditarEmpresaView.as_view(), name='editarempresaview'),

    # Outros
    # COntratos
    path(r'outros/adicionarcontrato/',
        geral.AdicionarContratoView.as_view(), name='addcontratoview'),
    path(r'outros/listacontratos/',
        geral.ContratosListView.as_view(), name='listacontratosview'),
    path(r'outros/editarcontrato/<int:pk>/',
        geral.EditarContratoView.as_view(), name='editarcontratoview'),

    # Area
    path(r'outros/adicionararea/',
        geral.AdicionarAreaView.as_view(), name='addareaview'),
    path(r'outros/listaareas/',
        geral.AreasListView.as_view(), name='listaareasview'),
    path(r'outros/editararea/<int:pk>/',
        geral.EditarAreaView.as_view(), name='editarareaview'),
    

    # Solicitante
    path(r'outros/adicionarsolicitante/',
        geral.AdicionarSolicitanteView.as_view(), name='addsolicitanteview'),
    path(r'outros/listasolicitantes/',
        geral.SolicitantesListView.as_view(), name='listasolicitantesview'),
    path(r'outros/editarsolicitante/<int:pk>/',
        geral.EditarSolicitanteView.as_view(), name='editarsolicitanteview'),

    # Aprovador
    path(r'outros/adicionaraprovador/',
        geral.AdicionarAprovadorView.as_view(), name='addaprovadorview'),
    path(r'outros/listaaprovadors/',
        geral.AprovadorListView.as_view(), name='listaaprovadorview'),
    path(r'outros/editaraprovador/<int:pk>/',
        geral.EditarAprovadorView.as_view(), name='editaraprovadorview'),

     # ItemBM
    path(r'outros/adicionaritemmed/',
        geral.AdicionarItemBmView.as_view(), name='additemmedview'),
    path(r'outros/listaitensmed/',
        geral.ItemBmListView.as_view(), name='listaitensmedview'),
    path(r'outros/editaritemmed/<int:pk>/',
        geral.EditarItemBmView.as_view(), name='editaritemmedview'),
    path(r'outros/importaritembm/',
        import_csv.import_csv_itembm, name='importar_csv_itembm'),
]