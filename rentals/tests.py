from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rentals.models import User, Property, RentalAgreement, RentPayment
from datetime import date

class RentalSystemTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create Superuser
        self.admin = User.objects.create_superuser(username='admin', password='adminpassword', email='admin@example.com', role='SUPERUSER')

        # Create Owners
        self.owner1 = User.objects.create_user(username='owner1', password='password123', role='OWNER')
        self.owner2 = User.objects.create_user(username='owner2', password='password123', role='OWNER')

        # Create Tenants
        self.tenant1 = User.objects.create_user(username='tenant1', password='password123', role='TENANT')
        self.tenant2 = User.objects.create_user(username='tenant2', password='password123', role='TENANT')

        # Create Properties
        self.prop1 = Property.objects.create(owner=self.owner1, title="Owner1's Flat", address="Street 1")
        self.prop2 = Property.objects.create(owner=self.owner2, title="Owner2's House", address="Street 2")

        # Create Agreement
        self.agreement1 = RentalAgreement.objects.create(
            property=self.prop1, tenant=self.tenant1,
            start_date=date(2023, 1, 1), end_date=date(2023, 12, 31),
            monthly_rent=1000.00
        )

        # Create Payment
        self.payment1 = RentPayment.objects.create(
            agreement=self.agreement1, month=date(2023, 5, 1), amount=1000.00
        )

    def test_property_visibility(self):
        # Owner1 should only see their property
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(reverse('property-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Owner1's Flat")

        # Tenant1 should see the property they rent
        self.client.force_authenticate(user=self.tenant1)
        response = self.client.get(reverse('property-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Owner1's Flat")

        # Tenant2 should see no properties
        self.client.force_authenticate(user=self.tenant2)
        response = self.client.get(reverse('property-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # Admin should see all properties
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('property-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_payment_actions(self):
        # Tenant1 pays rent
        self.client.force_authenticate(user=self.tenant1)
        response = self.client.post(reverse('rentpayment-pay', args=[self.payment1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment1.refresh_from_db()
        self.assertTrue(self.payment1.is_paid)

        # Owner1 approves rent
        self.client.force_authenticate(user=self.owner1)
        response = self.client.post(reverse('rentpayment-approve', args=[self.payment1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment1.refresh_from_db()
        self.assertTrue(self.payment1.is_approved)

    def test_unauthorized_approval(self):
        # Tenant1 tries to approve their own rent
        self.client.force_authenticate(user=self.tenant1)
        response = self.client.post(reverse('rentpayment-approve', args=[self.payment1.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.payment1.refresh_from_db()
        self.assertFalse(self.payment1.is_approved)

    def test_owner_visibility_of_payments(self):
        # Owner1 sees payment for their property
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(reverse('rentpayment-list'))
        self.assertEqual(len(response.data), 1)

        # Owner2 sees no payments
        self.client.force_authenticate(user=self.owner2)
        response = self.client.get(reverse('rentpayment-list'))
        self.assertEqual(len(response.data), 0)
