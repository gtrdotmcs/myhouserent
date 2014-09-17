from django.contrib import admin
from Renter.models import RenterInfo
# Register your models here.
class RenterAdmin(admin.ModelAdmin):
    fields = [ 'HOID', 'full_name', 'previous_address', 'rent_amount', 'deposit_by_renter','start_rent_date', 'end_rent_date' ]
    
admin.site.register(RenterInfo, RenterAdmin)