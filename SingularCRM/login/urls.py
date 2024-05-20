from django.urls import path
from . import views as v

app_name = 'login'
urlpatterns = [
    # login/
    path(r'', v.UserFormView.as_view(), name='loginview'),

    # login/registrar/
    path(r'registrar/', v.UserRegistrationFormView.as_view(),
        name='registrarview'),

    # login/esqueceu/:
    path(r'esqueceu/', v.ForgotPasswordView.as_view(), name='esqueceuview'),

    # login/trocarsenha/:
    path(r'trocarsenha/<str:uidb64>-<str:token>/',
        v.PasswordResetConfirmView.as_view(), name='trocarsenhaview'),

    # logout
    path(r'logout/', v.UserLogoutView.as_view(), name='logoutview'),

    # login/perfil/
    path(r'perfil/', v.MeuPerfilView.as_view(), name='perfilview'),

    # login/editarperfil/
    path(r'editarperfil/', v.EditarPerfilView.as_view(), name='editarperfilview'),

    # login/usuarios/
    path(r'usuarios/', v.UsuariosListView.as_view(), name='usuariosview'),

    # login/usuarios/(id_usuario)
    path(r'usuarios/<int:pk>/',
        v.UsuarioDetailView.as_view(), name='usuariodetailview'),

    # deletar usuario
    path(r'deletaruser/<int:pk>/',
        v.DeletarUsuarioView.as_view(), name='deletarusuarioview'),

    # permissoes usuario
    path(r'permissoesusuario/<int:pk>/',
        v.EditarPermissoesUsuarioView.as_view(), name='permissoesusuarioview'),

    # selecionar empresa
    path(r'selecionarempresa/', v.SelecionarMinhaEmpresaView.as_view(),
        name='selecionarempresaview'),
]
