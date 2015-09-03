from tastypie.resources import ModelResource
from tastypie import fields
from Rentdetails.models import RentDetails 
from houseowner.houserentapi import HouseownerResource
from Renter.renterapi import RenterResource

class RentDetailsResource(ModelResource):
    HOID = fields.ForeignKey(HouseownerResource, 'HOID', full=True)
    RID = fields.ForeignKey(RenterResource, 'RID', full=True)
    class Meta:
        queryset = RentDetails.objects.all()
        resource_name = 'rentdetails'
        
        