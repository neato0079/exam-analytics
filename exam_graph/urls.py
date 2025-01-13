from django.urls import path
from . import views

urlpatterns = [
    path('help/', views.help, name='help'),
    path('', views.home, name='thehome'),
    path('result/', views.filter_submission_handler, name='test'),
    path('form/', views.form_page, name='formyayay'),
    path('mock_data/', views.display_mock_csv, name='mock'),
    path('test/', views.upload_csv, name='mock'),
]