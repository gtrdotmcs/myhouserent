from tastypie.resources import ModelResource
from houseowner.models import HouseOwner


class HouseownerResource(ModelResource):
    class Meta:
        queryset = HouseOwner.objects.all()
        resource_name = 'houseowner'