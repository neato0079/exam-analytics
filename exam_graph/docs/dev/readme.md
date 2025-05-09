Notes
-----
path to this readme: `exam_graph/docs/dev/readme.md`

Run server with python `manage.py runserver`
- Make sure you are in the correct python environment. You can check this by running the command `which python` in the terminal

TESTS
-----
code snippett:
```
from django.urls import path, include
from . import views

urlpatterns = [
    path('help/', views.help, name='help'),
    path('', views.home, name='home'),
    path('result/', views.filter_submission_handler, name='test'),
    path('form/', views.form_page, name='formyayay'),
    path('upload/', views.upload_csv, name='mock'),
    path('load_data/', views.load_data, name='load_data'),
    path('login/', views.login_page, name='login_page'),
    path('app_login/', views.app_login, name='login'),    
    path('logout/', views.logout, name='logout'),
    path('wholog/', views.wholog, name='wholog'),
    path("user/", include("django.contrib.auth.urls")),
    path("docs/<path:doc_path>/", views.documentation, name='documentation')
]
```