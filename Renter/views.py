from django.shortcuts import render, get_object_or_404

# Create your views here.


# Create your views here.
from django.http import HttpResponse
from houseowner.models import HouseOwner 
    
def editdetails(request, houseowner_id):
    
    houseowner = get_object_or_404(HouseOwner, pk=houseowner_id)
    return render(request, 'renterinfo/Renterdetails.html', {'houseowner': houseowner})