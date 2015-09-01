from tastypie.resources import ModelResource
from Rentdetails.models import RentDetails 


class RentDetailsResource(ModelResource):
    class Meta:
        queryset = RentDetails.objects.all()
        resource_name = 'rentdetails'
        
        