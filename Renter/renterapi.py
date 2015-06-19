from tastypie.resources import ModelResource
from Renter.models import RenterInfo


class RenterResource(ModelResource):
    class Meta:
        queryset = RenterInfo.objects.all()
        resource_name = 'renter'