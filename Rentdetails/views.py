from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from Rentdetails.models import RentDetails
from Renter.models import RenterInfo
from myhouserent.cipherDiciphertext import encrypt_val, decrypt_val
#from django.core.context_processors import request
from django.contrib.auth.decorators import login_required, permission_required

@login_required(login_url='/user/login/') 
def inforentdetails(request, rentdetail_id):
    rentdetails = get_object_or_404(RentDetails, pk=rentdetail_id)
    return render(request, 'rentdetails/Rentdetail.html', {'rentdetails': rentdetails} )

@login_required(login_url='/user/login/') 
def editrentdetails(request, rentdetail_id):
    rentdetails = get_object_or_404(RentDetails, pk=rentdetail_id)
    print dir(rentdetails)
    if rentdetails:
        return render(request, 'rentdetails/editrentdetails.html', {'rentdetails': rentdetails} )
    else:
        error_message ="fuck nothing gotten what the hell"
        return render(request, 'rentdetails/editrentdetails.html', {'error_message': error_message} )

@login_required(login_url='/user/login/') 
def addrentdetails(request, renterinfo_id):
    renterdetails = get_object_or_404(RenterInfo, pk=renterinfo_id)
    print dir(renterdetails)
    if renterdetails:
        return render(request, 'rentdetails/addrenterdetails.html', {'renterdetails': renterdetails} )
    else:
        error_message = "fuck nothing gotten what the hell"
        return render(request, 'rentdetails/addrenterdetails.html', {'error_message': error_message} )

@login_required(login_url='/user/login/') 
def delete_rent_detail(request, rentdetail_id):
   try :
       rentdetails = get_object_or_404(RentDetails, pk=rentdetail_id)
       rentdetails.delete()
       deleted_message = encrypt_val("%s  deleted successfully fully"%rentdetails)
       return HttpResponseRedirect(reverse('Renter:showdetails', args=(rentdetails.RID_id,))+"?delmsg=%s"%deleted_message)
       #return render(request, 'renterinfo/Renterdetails.html', {'renterinfo': renterinfo, 'error_message': error_message})
   except (KeyError, RentDetails.DoesNotExist):
        # Redisplay the poll voting form.
        renterinfo = get_object_or_404(RenterInfo, pk=1)
        error_message = "what are you doing dude it dose not exist"
        return render(request, 'renterinfo/Renterdetails.html', {'renterinfo': renterinfo, 'error_message': error_message}) 

@login_required(login_url='/user/login/') 
def submitrentdetails(request,flag):
    
    try:
        if int(flag) == 0:
            rentdetail_id = request.POST['rentdetails_id']
            rentdetails = get_object_or_404(RentDetails, pk=rentdetail_id)
        elif int(flag) == 1:
            rentdetail_id = request.POST['renterdetails_id']
            rentdetails = RentDetails()
            renterinfodetails = get_object_or_404(RenterInfo, pk=rentdetail_id)
            rentdetails.HOID = renterinfodetails.HOID
            rentdetails.RID = renterinfodetails
        
    except (KeyError, RentDetails.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'rentdetails/editrentdetails.html', {
            'rentdetails': rentdetails_id,
            'error_message': "You didn't correctly edited.",
        })
    else:
        print request.POST['months']
        print request.POST['Dategiven']
        print request.POST.get('pyeeadv', False)
        print request.POST['Amount']
        
        rentdetails.Paid_for_mounths = request.POST['months']
        rentdetails.rent_given_date = request.POST['Dategiven']
        rentdetails.pay_inadvance = request.POST.get('pyeeadv', False) #request.POST['pyeeadv']
        rentdetails.rent_amount = request.POST['Amount']
        rentdetails.save()
        
        success_message = encrypt_val("Successfully Done Kudos!")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('Renter:showdetails', args=(rentdetails.RID_id,))+"?frmmsg=%s"%success_message)
        #return HttpResponseRedirect(reverse('Rentdetails:inforentdetails', args=(rentdetails.id,)))
