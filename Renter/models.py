from django.db import models
from houseowner.models import HouseOwner
# Create your models here.
class RenterInfo(models.Model):
    HOID = models.ForeignKey(HouseOwner)
    full_name = models.CharField(max_length=200)
    previous_address = models.CharField(max_length=200)
#    photo_of_renter = models.CharField(max_length=200)#we can use cloudnary to save path of images of any photo upload.
    rent_amount  = models.IntegerField(default=0)
    start_rent_date = models.DateField('Agreement started')
    end_rent_date = models.DateField('Agreement Ended')
    deposit_by_renter = models.IntegerField(default=0)
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
    def __unicode__(self):  # Python 3: def __str__(self):
         return self.full_name