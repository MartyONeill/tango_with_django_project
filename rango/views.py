from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect
from django.urls import reverse

from rango.models import Category, Page
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required

from datetime import datetime

def index(request):

    'request.session.set_test_cookie()'

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


    visitor_cookie_handler(request)
    #context_dict['visits'] = request.session['visits']
    
    # Render response and send back
    response = render(request, 'rango/index.html', context = context_dict)
    return response

def about(request):

    '''
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    '''

    context_dict = {}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

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

@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST ?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # have we been provided with a valid form
        if form.is_valid():

            #save the new category to the database
            form.save(commit=True)

            #now that the category is saved, we confirm this
            #for now, just redirect the user bakc to index view
            return redirect('/rango/')
        
        else:
            #if the form isnt valid, show errors
            print(form.errors)

    #will handle the bad form, new form, or no form supplied cases
    # render the form with error message
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):

    try:
        category = Category.objects.get(slug=category_name_slug)

    except Category.DoesNotExist:
        category = None

    #cant aDD a page to a category that doesnt exist
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', 
                                        kwargs={'category_name_slug': 
                                            category_name_slug}))

        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):

    # boolean telling the template if the registreation was succ
    # inital false, when registred turn to true
    registered = False

    #if itsa post we're intrested in processing form data
    if request.method == 'POST':

        # attempt to grab info from form
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            # hash the password with set_password method
            # once hashed update the user object
            user.set_password(user.password)
            user.save()

            # we dont save to begin with as we need to add user, 
            # do this later
            profile = profile_form.save(commit=False)
            profile.user = user

            # if the user provided a pic save it
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # now we save the user profile
            profile.save()

            # update vairable to show suer registered
            registered = True

        else:

            print(user_form.errors, profile_form.errors)

    else:

        #theyre not a user yet so we render the forms as blank
        user_form = UserForm()
        profile_form = UserProfileForm()

    # render the form depending on the context
    return render(request, 'rango/register.html', 
                    context = {'user_form':user_form, 
                    'profile_form':profile_form,
                    'registered':registered})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:

            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

            # The request is not a HTTP POST, so display the login form.
            # This scenario would most likely be a HTTP GET.

    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

#use login requered so only people already logged in can see it
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

""" 
HELPER FUNCTIONS
""" 

def visitor_cookie_handler(request):

    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.

    visits = int(get_server_side_cookie(request, 'visits', 1))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:

        visits = visits + 1

        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())

    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
             
