from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Contstruct a dictionary to pass to the template engine as its context
    # 'boldmessage' matches the variable {{boldmessage}} in template
    context_dict = {'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!'}

    # returns a rendered response ro sedn to the client
    # make sure of the shortcut funtion (? what is this)
    # first param is template we wish to use
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context = context_dict)