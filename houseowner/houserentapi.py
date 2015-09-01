from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization

from django.contrib.auth.models import User

from houseowner.models import HouseOwner


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
    excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
    
class HouseownerResource(ModelResource):
    UID = fields.ForeignKey('self', 'UID')
    class Meta:
        queryset = HouseOwner.objects.all()
        resource_name = 'houseowner'