from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page

def index(request):

    '''
    > Query the database for a list of ALL categories curently stored
    > Order the caegories by the number of likes in descnding order
    > Retrieve the top 5 only -- or all if less than 5
    > Place the list in our context_dict dictionary (with boldmessage)
    > this will be passed to the template engine
    '''
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # Render response and send back
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context = context_dict)

def show_category(request, category_name_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

def show_page(request, page_name_slug):
    
    context_dict ={}

    try:
        page = Page.objects.get(slug=page_name_slug)
        context_dict['page'] = page

    except Page.DoesNotExist:
        context_dict['page'] = None

    return render(request, 'rango/page.html', context=context_dict)


