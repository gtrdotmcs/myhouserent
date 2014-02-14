from django.contrib import admin
from houseowner.models import HouseOwner
from Renter.models import RenterInfo
# Register your models here.

class RenterInline(admin.StackedInline):
    model = RenterInfo
    
class HouseOwnerAdmin(admin.ModelAdmin):
    fields = ['Full_Name', 'No_of_renters', 'Houseownerjoinedthesite']
    inlines = [RenterInline]
admin.site.register(HouseOwner, HouseOwnerAdmin)