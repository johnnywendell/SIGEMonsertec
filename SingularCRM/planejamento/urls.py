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
    #path('rdos/json/', v.json_fatores, name='json_fatores'),
    #path('rdo/qrcode/<int:pk>/', v.render_pdf_view_tag, name='rdo_qrcode'),
    #path('rdo/pdf/<int:pk>/', v.render_pdf_view, name='rdo_pdf'), 


]