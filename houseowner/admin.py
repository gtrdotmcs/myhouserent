from django.contrib import admin
from houseowner.models import HouseOwner
from Renter.models import RenterInfo
# Register your models here.

class RenterInline(admin.TabularInline):
    model = RenterInfo
    
class HouseOwnerAdmin(admin.ModelAdmin):
    fields = ['Full_Name', 'No_of_renters', 'Address_of_houseowner','Houseownerjoinedthesite']
    inlines = [RenterInline]
    
admin.site.register(HouseOwner, HouseOwnerAdmin)