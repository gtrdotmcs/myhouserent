from django.contrib import admin
from houseowner.models import HouseOwner
# Register your models here.


class HouseOwnerAdmin(admin.ModelAdmin):
    fields = ['Full_Name', 'No_of_renters', 'Houseownerjoinedthesite']
    
admin.site.register(HouseOwner, HouseOwnerAdmin)