from tastypie.resources import ModelResource
from tastypie import fields
from Renter.models import RenterInfo
from houseowner.houserentapi import HouseownerResource


class RenterResource(ModelResource):
    HOID = fields.ForeignKey(HouseownerResource, 'HOID_id')
    class Meta:
        queryset = RenterInfo.objects.all()
        resource_name = 'renter'