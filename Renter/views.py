from django.shortcuts import render, get_object_or_404

# Create your views here.


# Create your views here.
from django.http import HttpResponse
from houseowner.models import HouseOwner
from Renter.models import RenterInfo
    
def showdetails(request, renter_id):
    
    renterinfo = get_object_or_404(RenterInfo, pk=renter_id)
    return render(request, 'renterinfo/Renterdetails.html', {'renterinfo': renterinfo})