import datetime
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User, Property, RentalAgreement, RentPayment
from .serializers import UserSerializer, PropertySerializer, RentalAgreementSerializer, RentPaymentSerializer
from .permissions import IsSuperUser, IsOwnerOrAdmin, IsTenantOrOwnerOrAdmin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_superuser and user.role == 'OWNER':
            serializer.save(role='TENANT')
        else:
            serializer.save()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()
        if user.is_superuser:
            return User.objects.all()
        if user.role == 'OWNER':
            tenant_ids = RentalAgreement.objects.filter(property__owner=user).values_list('tenant_id', flat=True)
            return User.objects.filter(Q(id=user.id) | Q(id__in=tenant_ids))
        return User.objects.filter(id=user.id)

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Property.objects.all()
        if user.role == 'OWNER':
            return Property.objects.filter(owner=user)
        return Property.objects.filter(agreements__tenant=user)

class RentalAgreementViewSet(viewsets.ModelViewSet):
    queryset = RentalAgreement.objects.all()
    serializer_class = RentalAgreementSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RentalAgreement.objects.all()
        if user.role == 'OWNER':
            return RentalAgreement.objects.filter(property__owner=user)
        return RentalAgreement.objects.filter(tenant=user)

@ensure_csrf_cookie
def index(request):
    return render(request, 'rentals/index.html')

class RentPaymentViewSet(viewsets.ModelViewSet):
    queryset = RentPayment.objects.all()
    serializer_class = RentPaymentSerializer

    def get_permissions(self):
        if self.action == 'approve':
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return RentPayment.objects.none()
        if user.is_superuser:
            return RentPayment.objects.all()
        if user.role == 'OWNER':
            return RentPayment.objects.filter(agreement__property__owner=user)
        return RentPayment.objects.filter(agreement__tenant=user)

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOrAdmin])
    def approve(self, request, pk=None):
        payment = self.get_object()
        payment.is_approved = True
        payment.is_paid = True
        if not payment.paid_date:
            payment.paid_date = datetime.date.today()
        payment.save()
        return Response({'status': 'payment approved and marked as paid'})

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        payment = self.get_object()
        if request.user != payment.agreement.tenant and not request.user.is_superuser:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        payment.is_submitted = True
        payment.payment_details = request.data.get('payment_details', '')
        payment.save()
        return Response({'status': 'payment details submitted for approval'})
