from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from houseowner.models import HouseOwner 

def index(request):
    #latest_houseowner_list = HouseOwner.objects.order_by()
    #output = ', '.join([p.Full_Name for p in latest_houseowner_list])
    #return HttpResponse(output)
    Houseowner_list = HouseOwner.objects.all()
    context = {'Houseowner_list': Houseowner_list}
    return render(request, 'houseowner/houseownerdetails.html', context)

def detail(request, houseowner_id):
    houseowner = get_object_or_404(HouseOwner, pk=houseowner_id)
    return render(request, 'houseowner/details.html', {'houseowner': houseowner})
    #return HttpResponse("You're looking at poll %s." % houseowner_id)
    