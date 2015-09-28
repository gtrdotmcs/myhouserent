from tastypie.resources import ModelResource
from tastypie import fields
from Renter.models import RenterInfo
from houseowner.houserentapi import HouseownerResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization

class RenterResource(ModelResource):
    HOID = fields.ForeignKey(HouseownerResource, 'HOID', full=True)
    class Meta:
        queryset = RenterInfo.objects.all()
        resource_name = 'renter'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()