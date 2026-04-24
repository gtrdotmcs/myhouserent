from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERUSER = 'SUPERUSER', 'Superuser'
        OWNER = 'OWNER', 'House Owner'
        TENANT = 'TENANT', 'Tenant'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TENANT)

    def is_owner(self):
        return self.role == self.Role.OWNER or self.is_superuser

    def is_tenant(self):
        return self.role == self.Role.TENANT

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class RentalAgreement(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='agreements')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.property.title} - {self.tenant.username}"

class RentPayment(models.Model):
    agreement = models.ForeignKey(RentalAgreement, on_delete=models.CASCADE, related_name='payments')
    month = models.DateField(help_text="First day of the month for which rent is being paid")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False, help_text="Approved by owner")
    paid_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.agreement} - {self.month.strftime('%B %Y')}"
