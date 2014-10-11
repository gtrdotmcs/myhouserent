from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import RequestContext
from django.http import HttpResponseRedirect
#from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from houseowner.models import HouseOwner
from Renter.models import RenterInfo

def login_user(request):
    username = password = ''
#    state = "well o"
    print request   
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
#        state = "hell o"
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print user.get_all_permissions()
                Groupperm = user.groups.all()[0]
                if Groupperm.name == 'HouseownerGroup':
                    houseownerid =  get_object_or_404(HouseOwner, UID=user.id)
                    return HttpResponseRedirect('/houseowner/HOspcf/%s/details'%(houseownerid.id))
                elif Groupperm.name == 'Renter_Group':
                    renterid =  get_object_or_404(RenterInfo, UID=user.id)
                    return HttpResponseRedirect('/renterinfo/%s/details'%renterid.id)
#                 state = "You're successfully logged in! %s"%username
#             else:
#                 state = "Your account is not active, please contact the site admin."
#         else:
#             state = "Your username and/or password were incorrect."

    return render(request, 'logged_in.html', {'username': username})

def logout_view(request):
    logout(request)
#    state = "logout success if you want you can log in below..."
    username = password = ''
    print username,password,"herelogout"
    return render(request, 'logged_in.html',{'username': username})
    # Redirect to a success page.
