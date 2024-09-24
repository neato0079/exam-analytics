from django.urls import path
from . import views

urlpatterns = [
    path('not_home/', views.not_home, name='nothome'),
    path('', views.home, name='thehome')
]