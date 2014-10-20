from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from houseowner.models import HouseOwner
from Renter.models import RenterInfo
from myhouserent.cipherDiciphertext import encrypt_val, decrypt_val
from django.contrib.auth.decorators import login_required

@login_required(login_url='/user/login/')    
def showdetails(request, renter_id):
    
    renterinfo = get_object_or_404(RenterInfo, pk=renter_id)
    listrneterdetails = renterinfo.rentdetails_set.all()
    if renterinfo:
        if request.method == 'GET' and 'frmmsg' in request.GET or 'delmsg' in request.GET:
            if 'frmmsg' in request.GET:
                message = decrypt_val(request.GET['frmmsg'].replace(' ', '+'))
                context = {'renterinfo': renterinfo,'success_message':message, 'listrneterdetails':listrneterdetails}
            elif 'delmsg' in request.GET:
                message = decrypt_val(request.GET['delmsg'].replace(' ', '+'))
                context = {'renterinfo': renterinfo,'error_message':message, 'listrneterdetails':listrneterdetails}       
            # not a perfect solution to replace the space with + but as url decode + as space we are doing for now in future it may hurt the code  
            return render(request, 'renterinfo/Renterdetails.html', context)
        else:    
            return render(request, 'renterinfo/Renterdetails.html', {'renterinfo': renterinfo, 'listrneterdetails':listrneterdetails})
    else:
        error_message = "hell ya it dose not exits dude!"     
        return render(request, 'renterinfo/Renterdetails.html', {'error_message': error_message})  

@login_required(login_url='/user/login/')
def addrenterinfo(request, houseowner_id):
    renterinfo = get_object_or_404(HouseOwner, pk=houseowner_id)
    print dir(renterinfo)
    if renterinfo:
        return render(request, 'renterinfo/Addrenterinfo.html', {'renterinfo': renterinfo} )
    else:
        error_message = "fuck nothing gotten what the hell"
        return render(request, 'renterinfo/Addrenterinfo.html', {'error_message': error_message} )
    #return render(request, 'houseowner/details.html', {'houseowner': houseowner})


@login_required(login_url='/user/login/')
def editrenterinfo(request, renter_id):
    renterinfo = get_object_or_404(RenterInfo, pk=renter_id)
    userobject = get_object_or_404(User, pk=renterinfo.UID_id)
    if renterinfo:
        return render(request, 'renterinfo/Editrenterinfo.html', {'renterinfo': renterinfo, 'userdetails':userobject} )
    else:
        error_message = "fuck nothing gotten what the hell"
        return render(request, 'renterinfo/Editrenterinfo.html', {'error_message': error_message} )

@login_required(login_url='/user/login/')
def deleterenterinfo(request, renter_id):
   try :
       renterinfodetails = get_object_or_404(RenterInfo, pk=renter_id)
       renterinfodetails.delete()
       deleted_message = encrypt_val("%s deleted successfully fully"%renterinfodetails)
       #return HttpResponseRedirect(reverse('renterinfo/Renterdetails.html',args=(renterinfo, error_message), kwargs={'renterinfo': renterinfo, 'error_message': error_message}))
       #return reverse('renterinfo/Renterdetails.html', args=(renterinfo, error_message))
       #return redirect('Renter.views.editdetails', {'renterinfo': renterinfo, 'error_message': error_message})
       return HttpResponseRedirect(reverse('houseowner:detail', args=(renterinfodetails.HOID_id,))+"?delmsg=%s"%deleted_message)
       #return render(request, 'renterinfo/Renterdetails.html', {'renterinfo': renterinfo, 'error_message': error_message})
   except (KeyError, RentDetails.DoesNotExist):
        # Redisplay the poll voting form.
        renterinfo = get_object_or_404(RenterInfo, pk=1)
        error_message = "what are you doing dude it dose not exist"
        return render(request, 'renterinfo/Renterdetails.html', {'renterinfo': renterinfo, 'error_message': error_message})
    
@login_required(login_url='/user/login/')
def showRentDetailsForyear(request, renter_id, rentfor_year):
    renterinfo = get_object_or_404(RenterInfo, pk=renter_id)
    listrneterdetails = renterinfo.rentdetails_set.filter(rent_given_date__icontains=rentfor_year)
    message = rentfor_year
    if int(rentfor_year) < 1998 :
        message = " %s ha ha Before this house was also not build are you was trying to to illegal construction here "%rentfor_year
    elif int(rentfor_year) > 2100:
        message = " %s ha ha Do you belive you be alive till this year "%rentfor_year   
    return render(request, 'renterinfo/Renterdetails.html', {'renterinfo': renterinfo, 'info_message':message, 'listrneterdetails':listrneterdetails})
    
@login_required(login_url='/user/login/')    
def submitrentinfo(request,flag):
    
     print request.POST['RenterName']
     print request.POST['RenterMonthrent']
     print request.POST['Start_Rent_Date']
     print request.POST['End_Rent_Date']
     try:
         if int(flag) == 0:
             renter_id = request.POST['renter_id']
             user_id = request.POST['userdetails_id']
             renterinfo = get_object_or_404(RenterInfo, pk=renter_id)
             userinfoedit = get_object_or_404(User, pk=user_id)
             if request.POST['RenterPassword'].strip() != "" and request.POST['RenterEmailid'].strip() != "" and request.POST['RenterPassword'].strip() != "":
               userinfoedit.username = request.POST['RenterUsername']
               userinfoedit.email = request.POST['RenterEmailid']
               userinfoedit.set_password(request.POST['RenterPassword']) 
               userinfoedit.save()
         elif int(flag) == 1:
             renterinfo = RenterInfo() # object of Renter
             #create new user with Renterinfo group
             user = User.objects.create_user(request.POST['RenterUsername'], request.POST['RenterEmailid'], request.POST['RenterPassword'])
             user.save()
             g = Group.objects.get(name='Renter_Group') 
             g.user_set.add(user)
             renterinfo.UID = user # assign it to the renter created.
             # add user under which house owner the user relies
             houseowner_id = request.POST['houseowner_id']
             renterinfodetails = get_object_or_404(HouseOwner, pk=houseowner_id)
             renterinfo.HOID = renterinfodetails
         
     except (KeyError, RenterInfo.DoesNotExist):
         # Redisplay the poll voting form.
         return render(request, 'renterinfo/Editrenterinfo.html', {
             'renterinfo': renterinfo,
             'error_message': "You didn't correctly edited.",
         })
     else:
         renterinfo.full_name = request.POST['RenterName']
         renterinfo.previous_address = request.POST['RenterPreviousAdd']
         renterinfo.deposit_by_renter = request.POST['RenterDeposit']
         renterinfo.rent_amount = request.POST['RenterMonthrent']
         renterinfo.start_rent_date = request.POST['Start_Rent_Date']
         renterinfo.end_rent_date = request.POST['End_Rent_Date']
         renterinfo.save()
         renter_id = renterinfo.id
         # Always return an HttpResponseRedirect after successfully dealing
         # with POST data. This prevents data from being posted twice if a
         # user hits the Back button.
         houseowner = get_object_or_404(HouseOwner, pk=renterinfo.HOID_id)
         success_message = encrypt_val("yo bro you rock!")
         
         #return render(request, 'houseowner/details.html', {'houseowner': houseowner,'success_message': success_message} )
         return HttpResponseRedirect(reverse('houseowner:detail', args=(renterinfo.HOID_id,))+"?frmmsg=%s&renter_id=%s"%(success_message,str(renter_id)))