import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'house_rent_project.settings')
django.setup()

from rentals.models import User, Property, RentalAgreement, RentPayment
from datetime import date

def verify():
    # Clear existing data
    User.objects.all().delete()

    # 1. Super user manage all of the Things it can create the A House owner.
    admin = User.objects.create_superuser(username='admin', password='adminpassword', email='admin@example.com')
    admin.role = 'SUPERUSER'
    admin.save()
    print("Created superuser")

    owner1 = User.objects.create_user(username='owner1', password='password123', role='OWNER')
    owner2 = User.objects.create_user(username='owner2', password='password123', role='OWNER')
    print("Created owners")

    tenant1 = User.objects.create_user(username='tenant1', password='password123', role='TENANT')
    tenant2 = User.objects.create_user(username='tenant2', password='password123', role='TENANT')
    print("Created tenants")

    # 2. House owner has right to add flat or home on rent
    prop1 = Property.objects.create(owner=owner1, title="Owner1's Flat", address="Street 1")
    prop2 = Property.objects.create(owner=owner2, title="Owner2's House", address="Street 2")
    print("Created properties")

    # Owner will add details and all information from Agreement Date from start to end date.
    agreement1 = RentalAgreement.objects.create(
        property=prop1, tenant=tenant1, 
        start_date=date(2023, 1, 1), end_date=date(2023, 12, 31), 
        monthly_rent=1000.00
    )
    print("Created agreement")

    # and how much rent per month received approve means rent is received by Owner.
    payment1 = RentPayment.objects.create(
        agreement=agreement1, month=date(2023, 5, 1), amount=1000.00
    )
    print("Created payment")

    # Verification of visibility rules
    print("\nVerifying Visibility:")
    
    # Owner1 should see prop1 but not prop2
    from django.test import RequestFactory
    from rentals.views import PropertyViewSet
    
    factory = RequestFactory()
    
    def get_queryset_count(view_class, user):
        request = factory.get('/')
        request.user = user
        view = view_class()
        view.request = request
        return view.get_queryset().count()

    print(f"Owner1 sees {get_queryset_count(PropertyViewSet, owner1)} properties (Expected: 1)")
    print(f"Owner2 sees {get_queryset_count(PropertyViewSet, owner2)} properties (Expected: 1)")
    print(f"Admin sees {get_queryset_count(PropertyViewSet, admin)} properties (Expected: 2)")
    print(f"Tenant1 sees {get_queryset_count(PropertyViewSet, tenant1)} properties (Expected: 1)")
    print(f"Tenant2 sees {get_queryset_count(PropertyViewSet, tenant2)} properties (Expected: 0)")

    # Test payment pay and approve
    print("\nVerifying Actions:")
    payment1.is_paid = True
    payment1.paid_date = date.today()
    payment1.save()
    print(f"Tenant1 paid rent. Payment paid status: {payment1.is_paid}")
    
    payment1.is_approved = True
    payment1.save()
    print(f"Owner approved rent. Payment approved status: {payment1.is_approved}")

if __name__ == "__main__":
    verify()
