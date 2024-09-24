from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('<h1>HOME</h1>')

def not_home(request):
    return HttpResponse('<h1>NOT HOME</h1>')