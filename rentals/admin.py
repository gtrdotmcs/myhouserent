from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Property, RentalAgreement, RentPayment


# Custom User Admin Configuration
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


# Property Admin Configuration
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'address')
    list_filter = ('owner',)
    search_fields = ('title', 'address', 'description')
    raw_id_fields = ('owner',)  # Better for performance with many users


# Rental Agreement Admin Configuration
@admin.register(RentalAgreement)
class RentalAgreementAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'start_date', 'end_date', 'monthly_rent')
    list_filter = ('property__owner', 'tenant')
    search_fields = ('property__title', 'tenant__username', 'tenant__email')
    raw_id_fields = ('property', 'tenant')
    date_hierarchy = 'start_date'


# Rent Payment Admin Configuration
@admin.register(RentPayment)
class RentPaymentAdmin(admin.ModelAdmin):
    list_display = ('agreement', 'month', 'amount', 'is_paid', 'is_approved', 'paid_date')
    list_filter = ('is_paid', 'is_approved', 'month')
    search_fields = ('agreement__property__title', 'agreement__tenant__username')
    raw_id_fields = ('agreement',)
    date_hierarchy = 'month'
    list_editable = ('is_paid', 'is_approved')  # Allows quick editing from list view
