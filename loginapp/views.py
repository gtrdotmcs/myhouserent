from django.shortcuts import render

# Create your views here.
from django.template import RequestContext
#from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in! %s"%username
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render(request, 'logged_in.html', {'state':state, 'username': username})

def logout_view(request):
    logout(request)
    state = "logout success if you want you can log in below..."
    username = password = ''
    return render(request, 'logged_in.html',{'state':state, 'username': username})
    # Redirect to a success page.