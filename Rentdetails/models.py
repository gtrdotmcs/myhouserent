from django.db import models
from houseowner.models import HouseOwner
from Renter.models import RenterInfo
from multiselectfield import MultiSelectField
#from django import forms

# Create your models here.
Months_year = ( ('Jan', 'January'),  
                ('Feb', 'February'),   
                ('Mar', 'March'),        
                ('Apr', 'April'),    
                ('May', 'May'),   
                ('Jun', 'June'),       
                ('Jul', 'July'),     
                ('Aug', 'August'),  
                ('Sep', 'September'),   
                ('Oct', 'October'),    
                ('Nov', 'November'), 
                ('Dec', 'December'))


class RentDetails(models.Model):
    HOID = models.ForeignKey(HouseOwner)
    RID = models.ForeignKey(RenterInfo)
    rent_amount  = models.IntegerField(default=0)
    rent_given_date = models.DateField('Date on Rent Given')
    pay_inadvance = models.BooleanField()
    Paid_for_mounths = MultiSelectField(choices=Months_year)
    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.rent_given_date)   
    