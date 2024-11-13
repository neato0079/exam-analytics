# aka API handler i guess

from django.shortcuts import render
from django.http import HttpResponse
from my_project import test_serve_browser

# Create your views here.
def home(request):
    return render(request, 'index.html')
    # return HttpResponse('<h1>asdfasdfasdfasdf</h1>')

def help(request):
    return HttpResponse('<h1>TODO: Add helpful tips for user!</h1>')

def result_graph(request):
    graph = test_serve_browser() # this is a pd series.... now its a df

    # convert series to df
    df = graph.to_frame()

    # convert df to html
    html_table = df.to_html()
    return render(request, 'results.html', {'graph': html_table})