from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from houseowner.models import HouseOwner 

def index(request):
    latest_houseowner_list = HouseOwner.objects.order_by()
    output = ', '.join([p.Full_Name for p in latest_houseowner_list])
    return HttpResponse(output)

def detail(request, houseowner_id):
    return HttpResponse("You're looking at poll %s." % houseowner_id)