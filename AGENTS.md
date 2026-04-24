# AGENTS.md - Technical Guide for House Rent API

## Project Overview
This repository contains a Django-based API for a House Rental system. It uses Django REST Framework (DRF) to provide endpoints for managing users, properties, rental agreements, and payments.

## Core Architecture

### Models (`rentals/models.py`)
- **User**: Custom user model with `role` choices: `SUPERUSER`, `OWNER`, `TENANT`.
- **Property**: Represents a house or flat, owned by a `User` (Owner).
- **RentalAgreement**: Links a `Property` to a `User` (Tenant) with start/end dates and rent amount.
- **RentPayment**: Tracks monthly rent payments. Includes `is_paid` (set by tenant) and `is_approved` (set by owner).

### Visibility & Security (`rentals/views.py`)
Visibility rules are enforced in the `get_queryset` methods of the ViewSets:
- **Owners**: Can only see properties they own, agreements for their properties, and payments related to those agreements.
- **Tenants**: Can only see the property they are renting, their own agreements, and their own payments.
- **Admins**: Can see everything.

### Actions
- `RentPaymentViewSet.pay()`: Allows a tenant to mark a payment as paid.
- `RentPaymentViewSet.approve()`: Allows an owner (or admin) to approve a payment. This field is read-only in the main serializer to prevent tenants from approving their own payments via standard PUT/PATCH requests.

## Development & Verification

### Verification Script
The `verify_api.py` script is the primary tool for verifying role-based visibility. It:
1. Clears the database.
2. Creates a Superuser, two Owners, and two Tenants.
3. Creates properties and agreements.
4. Verifies that `get_queryset` returns the correct number of objects for each user role.

### Coding Standards
- Keep business logic in `views.py` or separate service layers if they grow complex.
- Ensure all new endpoints respect the visibility rules implemented in `get_queryset`.
- Use the custom permissions defined in `rentals/permissions.py`.

## Programmatic Checks
When making changes to the models or views, you **MUST** run the verification script to ensure no regressions in the visibility logic:
```bash
python verify_api.py
```
If the script outputs "Expected" counts that do not match the actual counts, the visibility logic is broken.
