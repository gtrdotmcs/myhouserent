# House Rent Management API

A Django-based REST API for managing house rentals with role-based access control.

## Setup Instructions

1.  **Install Dependencies**:
    Ensure you have Python installed, then run:
    ```bash
    pip install django djangorestframework django-filter
    ```

2.  **Apply Migrations**:
    Initialize the database:
    ```bash
    python manage.py migrate
    ```

3.  **Run Verification Script (Optional)**:
    To populate the database with sample data and verify visibility rules:
    ```bash
    python verify_api.py
    ```

4.  **Start the Server**:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

The API is accessible at `http://127.0.0.1:8000/api/`.

- `GET /api/users/`: List users (Admins see all, others see only themselves).
- `GET /api/properties/`: List properties (Owners see theirs, Tenants see the one they rent).
- `GET /api/agreements/`: List rental agreements.
- `GET /api/payments/`: List rent payments.
- `POST /api/payments/<id>/pay/`: Tenant marks a payment as paid.
- `POST /api/payments/<id>/approve/`: Owner approves a payment.

## Roles & Permissions

- **Superuser**: Manage all data, including creating House Owners.
- **House Owner**: Add/edit their own properties and agreements, and approve received rent.
- **Tenant**: View their own rental agreement and payment history. Can mark rent as paid.

## Visibility Rules

- Owners cannot see properties or tenants belonging to other owners.
- Tenants cannot see other flats or other tenants.
- Superusers have full visibility across the system.
