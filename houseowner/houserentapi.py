from tastypie.resources import ModelResource ,ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authorization import Authorization

from django.contrib.auth.models import User

from houseowner.models import HouseOwner
from tastypie.models import ApiKey
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['id',"username"]
        allowed_methods = ['get', 'post']
        resource_name = 'user'
        
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                user_apikey =  ApiKey.objects.get(user_id=user.pk)
                if user_apikey:
                    print user
                    return self.create_response(request, {
                        'success': True,
                        'userinfo': {'user_group': user.groups.all()[0].name,
                                     'first_name': user.first_name,
                                     'last_name':user.last_name,
                                     'username':user.username,
                                     'usermail_id': user.email,
                                     'UID': user.pk,
                                     'user_apikey': user_apikey.key,
                                     'active': user.is_active }
                    })
                else:
                    return self.create_response(request, {
                    'success': False,
                    'reason': 'user_apikey not present',
                    }, HttpForbidden )
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)
        
        # Add it here.
        #authentication = BasicAuthentication()
#     class Meta:
#         queryset = User.objects.all()
#         resource_name = 'user'
#     excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
    
class HouseownerResource(ModelResource):
    UID = fields.ForeignKey(UserResource, 'UID', full=True, null=True)
    class Meta:
        queryset = HouseOwner.objects.all()
        allowed_methods = ['get', 'post']
        include_resource_uri = True
        authorization = Authorization()
        resource_name = 'houseowner'
