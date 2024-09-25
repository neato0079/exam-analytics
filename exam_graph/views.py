from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')
    # return HttpResponse('<h1>asdfasdfasdfasdf</h1>')

def not_home(request):
    return HttpResponse('<h1>NOT HOME</h1>')