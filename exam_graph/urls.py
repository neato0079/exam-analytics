from django.urls import path
from . import views

urlpatterns = [
    path('help/', views.help, name='help'),
    path('', views.home, name='thehome'),
    path('test/', views.filter_submission_handler, name='test'),
    path('result/<str:modality>/', views.upload_csv, name='result')
]