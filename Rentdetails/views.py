from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from Rentdetails.models import RentDetails
    
def inforentdetails(request, rentdetail_id):
    rentdetails = get_object_or_404(RentDetails, pk=rentdetail_id)
    return render(request, 'rentdetails/Rentdetail.html', {'rentdetails': rentdetails} )

def editrentdetails(request, rentdetail_id):
    rentdetails = get_object_or_404(RentDetails, pk=rentdetail_id)
    return render(request, 'rentdetails/editrentdetails.html', {'rentdetails': rentdetails} )

def submitrentdetails(request, rentdetail_id):
    
    try:
        rentdetails = get_object_or_404(RentDetails, pk=rentdetail_id)
        
    except (KeyError, RentDetails.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'rentdetails/editrentdetails.html', {
            'rentdetails': rentdetails_id,
            'error_message': "You didn't correctly edited.",
        })
    else:
        print request.POST['months']
        print request.POST['Dategiven']
        print request.POST['pyeeadv']
        print request.POST['Amount']
        
        rentdetails.Paid_for_mounths = request.POST['months']
        rentdetails.rent_given_date = request.POST['Dategiven']
        rentdetails.pay_inadvance = request.POST['pyeeadv']
        rentdetails.rent_amount = request.POST['Amount']
        rentdetails.save()
       
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('Rentdetails:inforentdetails', args=(u'1',)))