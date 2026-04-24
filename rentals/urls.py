from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PropertyViewSet, RentalAgreementViewSet, RentPaymentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'agreements', RentalAgreementViewSet)
router.register(r'payments', RentPaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
