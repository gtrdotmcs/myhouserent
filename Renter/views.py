from django.shortcuts import render, get_object_or_404

# Create your views here.


# Create your views here.
from django.http import HttpResponse
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