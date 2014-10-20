from django.shortcuts import render, get_object_or_404

# Create your views here.


from django.http import HttpResponse
from houseowner.models import HouseOwner
from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import CountryForm
from django.core.context_processors import request
from myhouserent.cipherDiciphertext import encrypt_val, decrypt_val
from django.contrib.auth.decorators import login_required, permission_required

@login_required(login_url='/user/login/')
@permission_required('houseowner.add_houseowner')
def index(request):
    #latest_houseowner_list = HouseOwner.objects.order_by()
    #output = ', '.join([p.Full_Name for p in latest_houseowner_list])
    #return HttpResponse(output)
    Houseowner_list = HouseOwner.objects.all()
    context = {'Houseowner_list': Houseowner_list}
    return render(request, 'houseowner/houseownerdetails.html', context)

@login_required(login_url='/user/login/')
def detail(request, houseowner_id):
    houseowner = get_object_or_404(HouseOwner, pk=houseowner_id)
    print request
    if houseowner:
        if request.method == 'GET' and 'frmmsg' in request.GET or 'delmsg' in request.GET:
            if 'frmmsg' in request.GET:
                message = decrypt_val(request.GET['frmmsg'].replace(' ', '+'))
                context = {'houseowner': houseowner,'success_message':message}
            elif 'delmsg' in request.GET:
                message = decrypt_val(request.GET['delmsg'].replace(' ', '+'))
                context = {'houseowner': houseowner,'error_message':message}       
            # not a perfect solution to replace the space with + but as url decode + as space we are doing for now in future it may hurt the code  
            return render(request, 'houseowner/details.html', context)
        else:    
            return render(request, 'houseowner/details.html', {'houseowner': houseowner})
    else:
        error_message ="fuck nothing gotten what the hell"
        return render(request, 'houseowner/details.html', {'error_message': error_message})
    #return HttpResponse("You're looking at poll %s." % houseowner_id)
'''
def my_view(request):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
''' 

def countries_view(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            countries = form.cleaned_data.get('countries')
            print countries,""
            # do something with your results
    else:
        form = CountryForm
    return render_to_response('forms.html', {'form':form },
        context_instance=RequestContext(request))