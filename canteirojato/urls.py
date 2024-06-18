from django.urls import path
from . import views as v

app_name = 'canteirojato'

urlpatterns = [

    # Romaneios
    # cadastro/empresa/adicionar/
    path(r'romaneio/adicionar/',
        v.AdicionarRomaneioView.as_view(), name='addromaneioview'),
    # cadastro/empresa/listaempresas
    path(r'romaneio/listaromaneios/',
        v.RomaneioListView.as_view(), name='listaromaneioview'),
    # cadastro/empresa/editar/
    path(r'romaneio/editar/<int:pk>/',
        v.EditarRomaneioView.as_view(), name='editarromaneioview'),
    path('romaneios/json/', v.json_fatores, name='json_fatores'),
    path('romaneio/qrcode/<int:pk>/', v.render_pdf_view_tag, name='romaneio_qrcode'),
    path('romaneio/pdf/<int:pk>/', v.render_pdf_view, name='romaneio_pdf'), 


]