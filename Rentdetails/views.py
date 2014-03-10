from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from Renter.models import RenterInfo
from Rentdetails.models import RentDetails
    
def editrentdetails(request, rentdetail_id):
    renter = RenterInfo.objects.get(id=rentdetail_id)
    rentername = renter.full_name
    rentdetails = get_object_or_404(RentDetails, pk=rentdetail_id)
    context = {'rentdetails': rentdetails, 'rentername': rentername}
    return render(request, 'rentdetails/Rentdetail.html', context )