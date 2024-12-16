from django.urls import path
from . import views

urlpatterns = [
    path('help/', views.help, name='help'),
    path('', views.home, name='thehome'),
    path('test/', views.result_graph, name='test'),
    path('result/<str:modality>/', views.upload_csv, name='result')
]