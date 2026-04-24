from rest_framework import serializers
from .models import User, Property, RentalAgreement, RentPayment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PropertySerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Property
        fields = ['id', 'owner', 'owner_username', 'title', 'address', 'description']
        read_only_fields = ['owner']

class RentalAgreementSerializer(serializers.ModelSerializer):
    property_title = serializers.ReadOnlyField(source='property.title')
    tenant_username = serializers.ReadOnlyField(source='tenant.username')

    class Meta:
        model = RentalAgreement
        fields = ['id', 'property', 'property_title', 'tenant', 'tenant_username', 'start_date', 'end_date', 'monthly_rent']

class RentPaymentSerializer(serializers.ModelSerializer):
    agreement_details = serializers.ReadOnlyField(source='agreement.__str__')

    class Meta:
        model = RentPayment
        fields = ['id', 'agreement', 'agreement_details', 'month', 'amount', 'is_paid', 'is_approved', 'paid_date']
        read_only_fields = ['is_approved']
