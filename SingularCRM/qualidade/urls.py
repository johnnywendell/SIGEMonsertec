from django.urls import path
from . import views as v

app_name = 'qualidade'

urlpatterns = [

    # Relatorio Area
    # cadastro/empresa/adicionar/
    path(r'relatorioarea/adicionar/',
        v.AdicionarRelatorioAreaView.as_view(), name='addrelatorioareaview'),
    # cadastro/empresa/listaempresas
    path(r'relatorioarea/listaromaneios/',
        v.RelatorioAreaListView.as_view(), name='listarelatorioareaview'),
    # cadastro/empresa/editar/
    path(r'relatorioarea/editar/<int:pk>/',
        v.EditarRelatorioAreaView.as_view(), name='editarrelatorioareaview'),
    #path('romaneio/pdf/<int:pk>/', v.render_pdf_view, name='romaneio_pdf'), 

    # Relatorio Area
    # cadastro/empresa/adicionar/
    path(r'relatoriojato/adicionar/',
        v.AdicionarRelatorioJatoView.as_view(), name='addrelatoriojatoview'),
    # cadastro/empresa/listaempresas
    path(r'relatoriojato/listaromaneios/',
        v.RelatorioJatoListView.as_view(), name='listarelatoriojatoview'),
    # cadastro/empresa/editar/
    path(r'relatoriojato/editar/<int:pk>/',
        v.EditarRelatorioJatoView.as_view(), name='editarrelatoriojatoview'),
    #path('romaneio/pdf/<int:pk>/', v.render_pdf_view, name='romaneio_pdf'), 

    path(r'relatorio/photoarea/<int:pk>/',
        v.PhotoCreateViewArea.as_view(), name='photorelatorioarea'),
    path(r'relatorio/photojato/<int:pk>/',
        v.PhotoCreateViewJato.as_view(), name='photorelatoriojato'),
    path(r'relatorio/photo/deletearea/<int:pk>/',
        v.delete_photoarea, name='photorelatorioareadelete'),
    path(r'relatorio/photo/deletejato/<int:pk>/',
        v.delete_photojato, name='photorelatoriojatodelete'),
        #path('romaneio/pdf/<int:pk>/', v.render_pdf_view, name='romaneio_pdf'), 

    path('relatorio/pdf/<int:pk>/', v.render_pdf_view, name='render_pdf_view'),
    path('relatorio/pdfsimple/<int:pk>/', v.render_pdf_view_simple, name='render_pdf_view_simple'),
    path('relatorio/atualizar-materiais/', v.atualizar_materiais_selecionados, name='atualizar_materiais'),
]