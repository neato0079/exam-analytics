from django.urls import path, include
from . import views

urlpatterns = [
    path('help/', views.help, name='help'),
    path('', views.home, name='home'),
    path('result/', views.filter_submission_handler, name='test'),
    path('form/', views.form_page, name='formyayay'),
    path('mock_data/', views.display_mock_csv, name='mock'),
    path('upload/', views.upload_csv, name='mock'),
    path('load_data/', views.load_data, name='load_data'),
    path('login/', views.login_page, name='login_page'),
    path('app_login/', views.app_login, name='login'),    
    path('logout/', views.logout, name='logout'),
    path('wholog/', views.wholog, name='wholog'),
    path("user/", include("django.contrib.auth.urls")),
]
# what this includes: include("django.contrib.auth.urls")
# user/login/ [name='login']
# user/logout/ [name='logout']
# user/password_change/ [name='password_change']
# user/password_change/done/ [name='password_change_done']
# user/password_reset/ [name='password_reset']
# user/password_reset/done/ [name='password_reset_done']
# user/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# user/reset/done/ [name='password_reset_complete']