from django.db import models
from houseowner.models import HouseOwner
# Create your models here.
class RenterInfo(models.Model):
    HOID = models.ForeignKey(HouseOwner)
    full_name = models.CharField(max_length=200)
    rent_amount  = models.IntegerField(default=0)
    start_rent_date = models.DateField('Agreement started')
    end_rent_date = models.DateField('Agreement Ended')
