
from django.urls import path
from . import views

from settings import DEBUG

app_name = 'base'
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
]

if DEBUG:
    urlpatterns += [
        path(r'404/', views.handler404),
        path(r'500/', views.handler500),
    ]
