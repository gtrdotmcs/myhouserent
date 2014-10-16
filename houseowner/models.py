#Should validate
import datetime
from django.utils import timezone

#
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class HouseOwner(models.Model):
    #Username = models.CharField(max_length=25)
    UID = models.ForeignKey(User)
    Full_Name = models.CharField(max_length=200)
    Address_of_houseowner = models.CharField(max_length=200)
    No_of_renters  = models.IntegerField(default=0)
    Houseownerjoinedthesite = models.DateTimeField('House owner join site')
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.Houseownerjoinedthesite <= now
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.Full_Name