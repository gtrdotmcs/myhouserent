from django.contrib import admin
from Rentdetails.models import RentDetails 
# Register your models here.

class RentDetailsAdmin(admin.ModelAdmin):
    fields = ['HOID', 'RID', 'rent_amount', 'rent_given_date', 'pay_inadvance','Paid_for_mounths']
    
admin.site.register(RentDetails, RentDetailsAdmin)
