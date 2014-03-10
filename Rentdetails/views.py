from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from Rentdetails.models import RentDetails
    
def editrentdetails(request, rentdetail_id):
    
    rentdetails = get_object_or_404(RentDetails, pk=rentdetail_id)
    return render(request, 'rentdetails/Rentdetail.html', {'rentdetails': rentdetails})