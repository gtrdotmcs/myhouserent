from django.shortcuts import render, get_object_or_404

# Create your views here.


# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from houseowner.models import HouseOwner
from Renter.models import RenterInfo
    
def showdetails(request, renter_id):
    
    renterinfo = get_object_or_404(RenterInfo, pk=renter_id)
    return render(request, 'renterinfo/Renterdetails.html', {'renterinfo': renterinfo})


def addrenterinfo(request, houseowner_id):
    renterinfo = get_object_or_404(HouseOwner, pk=houseowner_id)
    print dir(renterinfo)
    if renterinfo:
        return render(request, 'renterinfo/Addrenterinfo.html', {'renterinfo': renterinfo} )
    else:
        error_message = "fuck nothing gotten what the hell"
        return render(request, 'renterinfo/Addrenterinfo.html', {'error_message': error_message} )
    #return render(request, 'houseowner/details.html', {'houseowner': houseowner})



def editrenterinfo(request, renter_id):
    renterinfo = get_object_or_404(RenterInfo, pk=renter_id)
    print dir(renterinfo)
    if renterinfo:
        return render(request, 'renterinfo/Editrenterinfo.html', {'renterinfo': renterinfo} )
    else:
        error_message = "fuck nothing gotten what the hell"
        return render(request, 'renterinfo/Editrenterinfo.html', {'error_message': error_message} )
    
def submitrentinfo(request,flag):
    
     print request.POST['RenterName']
     print request.POST['RenterMonthrent']
     print request.POST['Start_Rent_Date']
     print request.POST['End_Rent_Date']
     try:
         if int(flag) == 0:
             renter_id = request.POST['renter_id']
             renterinfo = get_object_or_404(RenterInfo, pk=renter_id)
         elif int(flag) == 1:
             rentdetail_id = request.POST['renterdetails_id']
             rentdetails = RentDetails()
             renterinfodetails = get_object_or_404(RenterInfo, pk=rentdetail_id)
             rentdetails.HOID = renterinfodetails.HOID
             rentdetails.RID = renterinfodetails
         
     except (KeyError, RentDetails.DoesNotExist):
         # Redisplay the poll voting form.
         return render(request, 'renterinfo/Editrenterinfo.html', {
             'renterinfo': renter_id,
             'error_message': "You didn't correctly edited.",
         })
     else:
               
         renterinfo.full_name = request.POST['RenterName']
         renterinfo.rent_amount = request.POST['RenterMonthrent']
         renterinfo.start_rent_date = request.POST['Start_Rent_Date']
         renterinfo.end_rent_date = request.POST['End_Rent_Date']
         renterinfo.save()
         # Always return an HttpResponseRedirect after successfully dealing
         # with POST data. This prevents data from being posted twice if a
         # user hits the Back button.
         success_message ="yo bro you rock!"
         return HttpResponseRedirect(reverse('houseowner:detail', args=(renterinfo.HOID_id)))