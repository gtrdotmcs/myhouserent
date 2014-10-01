from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from houseowner.models import HouseOwner
from Renter.models import RenterInfo
from myhouserent.cipherDiciphertext import encrypt_val, decrypt_val
#from django.contrib.auth.decorators import login_required

#@login_required(login_url='    /') 
def mainindex(request):
    return HttpResponseRedirect('/houseowner/')