# Requirements Document

## Introduction

The House Rent API is a Django REST Framework backend for managing residential property rentals. It supports three user roles — Superuser, Owner, and Tenant — and provides endpoints for property listings, rental agreements, and rent payment tracking. This document captures the requirements for the current system and defines acceptance criteria that guide both verification of existing behaviour and future enhancements.

---

## Glossary

- **API**: The Django REST Framework HTTP service exposed at `/api/`.
- **System**: The House Rent API as a whole.
- **Auth_Service**: The component responsible for authenticating requests (currently session + basic auth).
- **User_Manager**: The component responsible for user account lifecycle (UserViewSet + UserSerializer).
- **Property_Manager**: The component responsible for property CRUD (PropertyViewSet + PropertySerializer).
- **Agreement_Manager**: The component responsible for rental agreement CRUD (RentalAgreementViewSet + RentalAgreementSerializer).
- **Payment_Manager**: The component responsible for rent payment tracking (RentPaymentViewSet + RentPaymentSerializer).
- **Superuser**: A user with `is_superuser=True`; has unrestricted access to all resources.
- **Owner**: A user with `role=OWNER`; manages their own properties and agreements.
- **Tenant**: A user with `role=TENANT`; rents properties and submits payments.
- **Property**: A rentable unit with a title, address, and optional description, owned by an Owner.
- **RentalAgreement**: A contract linking a Property to a Tenant with start date, end date, and monthly rent amount.
- **RentPayment**: A record of a monthly rent payment for a RentalAgreement, with paid and approval states.
- **Visibility Rule**: The data-scoping logic applied per role in `get_queryset` to ensure users only see records they are authorised to access.

---

## Requirements

### Requirement 1: User Authentication

**User Story:** As any user, I want to authenticate with the API, so that I can access protected endpoints securely.

#### Acceptance Criteria

1. WHEN a request is made to any `/api/` endpoint without valid credentials, THE Auth_Service SHALL return HTTP 403.
2. WHEN a request includes valid session credentials, THE Auth_Service SHALL authenticate the user and allow the request to proceed.
3. WHEN a request includes valid HTTP Basic Auth credentials, THE Auth_Service SHALL authenticate the user and allow the request to proceed.
4. IF a request includes invalid credentials, THEN THE Auth_Service SHALL return HTTP 403 without exposing internal error details.

---

### Requirement 2: User Management

**User Story:** As a Superuser, I want to create and manage user accounts, so that Owners and Tenants can access the system.

#### Acceptance Criteria

1. THE User_Manager SHALL enforce that only Superusers can create new user accounts via `POST /api/users/`.
2. WHEN a Superuser creates a user, THE User_Manager SHALL accept `username`, `email`, `role`, and `password` fields and store the password as a secure hash.
3. WHEN an authenticated non-Superuser requests `GET /api/users/`, THE User_Manager SHALL return only the requesting user's own record.
4. WHEN a Superuser requests `GET /api/users/`, THE User_Manager SHALL return all user records.
5. IF a non-Superuser attempts to create a user account, THEN THE User_Manager SHALL return HTTP 403.
6. THE User_Manager SHALL expose `id`, `username`, `email`, and `role` in read responses and SHALL NOT expose the password hash.

---

### Requirement 3: Property Management

**User Story:** As an Owner, I want to list and manage my rental properties, so that Tenants can be assigned to them.

#### Acceptance Criteria

1. WHEN an Owner or Superuser submits `POST /api/properties/`, THE Property_Manager SHALL create a Property and automatically assign the authenticated Owner as the owner.
2. WHEN an Owner requests `GET /api/properties/`, THE Property_Manager SHALL return only Properties owned by that Owner.
3. WHEN a Tenant requests `GET /api/properties/`, THE Property_Manager SHALL return only Properties for which the Tenant has an active RentalAgreement.
4. WHEN a Superuser requests `GET /api/properties/`, THE Property_Manager SHALL return all Properties.
5. IF a Tenant attempts to create, update, or delete a Property, THEN THE Property_Manager SHALL return HTTP 403.
6. THE Property_Manager SHALL expose `id`, `owner` (read-only id), `owner_username`, `title`, `address`, and `description` in responses.

---

### Requirement 4: Rental Agreement Management

**User Story:** As an Owner, I want to create and manage rental agreements, so that Tenants are formally linked to my properties.

#### Acceptance Criteria

1. WHEN an Owner or Superuser submits `POST /api/agreements/`, THE Agreement_Manager SHALL create a RentalAgreement linking a Property to a Tenant with `start_date`, `end_date`, and `monthly_rent`.
2. WHEN an Owner requests `GET /api/agreements/`, THE Agreement_Manager SHALL return only RentalAgreements for Properties owned by that Owner.
3. WHEN a Tenant requests `GET /api/agreements/`, THE Agreement_Manager SHALL return only RentalAgreements where the Tenant is the named tenant.
4. WHEN a Superuser requests `GET /api/agreements/`, THE Agreement_Manager SHALL return all RentalAgreements.
5. IF a Tenant attempts to create, update, or delete a RentalAgreement, THEN THE Agreement_Manager SHALL return HTTP 403.
6. THE Agreement_Manager SHALL expose `id`, `property`, `property_title`, `tenant`, `tenant_username`, `start_date`, `end_date`, and `monthly_rent` in responses.

---

### Requirement 5: Rent Payment Tracking

**User Story:** As a Tenant, I want to record my monthly rent payments, so that Owners can verify and approve them.

#### Acceptance Criteria

1. THE Payment_Manager SHALL allow any authenticated user to read RentPayment records scoped to their role.
2. WHEN an Owner requests `GET /api/payments/`, THE Payment_Manager SHALL return only RentPayments linked to agreements for Properties owned by that Owner.
3. WHEN a Tenant requests `GET /api/payments/`, THE Payment_Manager SHALL return only RentPayments linked to that Tenant's agreements.
4. WHEN a Superuser requests `GET /api/payments/`, THE Payment_Manager SHALL return all RentPayments.
5. THE Payment_Manager SHALL expose `id`, `agreement`, `agreement_details`, `month`, `amount`, `is_paid`, `is_approved` (read-only), and `paid_date` in responses.
6. THE Payment_Manager SHALL prevent Tenants from setting `is_approved` directly via PUT or PATCH requests.

---

### Requirement 6: Tenant Pay Action

**User Story:** As a Tenant, I want to mark a payment as paid, so that my Owner knows I have submitted rent.

#### Acceptance Criteria

1. WHEN a Tenant submits `POST /api/payments/{id}/pay/`, THE Payment_Manager SHALL set `is_paid=True` and `paid_date` to the current date for that RentPayment.
2. WHEN the pay action succeeds, THE Payment_Manager SHALL return HTTP 200 with `{"status": "payment sent for approval"}`.
3. IF a user who is not the agreement's Tenant and not a Superuser submits the pay action, THEN THE Payment_Manager SHALL return HTTP 403.
4. WHILE a RentPayment has `is_paid=True`, THE Payment_Manager SHALL retain the original `paid_date` and SHALL NOT reset it on subsequent read requests.

---

### Requirement 7: Owner Approve Action

**User Story:** As an Owner, I want to approve a tenant's payment, so that the payment record reflects confirmed receipt of rent.

#### Acceptance Criteria

1. WHEN an Owner or Superuser submits `POST /api/payments/{id}/approve/`, THE Payment_Manager SHALL set `is_approved=True` for that RentPayment.
2. WHEN the approve action succeeds, THE Payment_Manager SHALL return HTTP 200 with `{"status": "payment approved"}`.
3. IF a Tenant attempts to call the approve action, THEN THE Payment_Manager SHALL return HTTP 403.

---

### Requirement 8: Role-Based Visibility Isolation

**User Story:** As a system administrator, I want strict data isolation between roles, so that users cannot access records belonging to other users.

#### Acceptance Criteria

1. THE System SHALL ensure that an Owner cannot read, update, or delete Properties, RentalAgreements, or RentPayments belonging to another Owner.
2. THE System SHALL ensure that a Tenant cannot read RentalAgreements or RentPayments belonging to another Tenant.
3. THE System SHALL ensure that a Tenant cannot read Properties for which the Tenant has no RentalAgreement.
4. WHEN a user requests a specific resource by ID that is outside their visibility scope, THE System SHALL return HTTP 404.

---

### Requirement 9: Token-Based Authentication (Future Enhancement)

**User Story:** As a developer integrating with the API, I want to authenticate using JWT tokens, so that I can build stateless client applications without relying on session cookies.

#### Acceptance Criteria

1. WHEN a client submits valid credentials to `POST /api/auth/token/`, THE Auth_Service SHALL return a signed JWT access token and a refresh token.
2. WHEN a client submits a valid JWT access token in the `Authorization: Bearer` header, THE Auth_Service SHALL authenticate the request.
3. WHEN a client submits a valid refresh token to `POST /api/auth/token/refresh/`, THE Auth_Service SHALL return a new access token.
4. IF a client submits an expired or invalid JWT token, THEN THE Auth_Service SHALL return HTTP 401.
5. THE Auth_Service SHALL set access token expiry to no more than 60 minutes and refresh token expiry to no more than 7 days.

---

### Requirement 10: Payment History and Reporting (Future Enhancement)

**User Story:** As an Owner or Tenant, I want to view payment history summaries, so that I can track rent compliance over time.

#### Acceptance Criteria

1. WHEN an Owner requests `GET /api/payments/?agreement={id}`, THE Payment_Manager SHALL return all RentPayments for that agreement scoped to the Owner's visibility.
2. WHEN an Owner requests `GET /api/payments/?is_paid=false`, THE Payment_Manager SHALL return all unpaid RentPayments for the Owner's properties.
3. WHEN a Tenant requests `GET /api/payments/?month={YYYY-MM}`, THE Payment_Manager SHALL return RentPayments for that month scoped to the Tenant's agreements.
4. THE Payment_Manager SHALL support filtering by `agreement`, `month`, `is_paid`, and `is_approved` query parameters.

---

### Requirement 11: Property Search and Filtering (Future Enhancement)

**User Story:** As a Tenant or Owner, I want to search and filter properties, so that I can quickly find relevant listings.

#### Acceptance Criteria

1. WHEN a user requests `GET /api/properties/?search={term}`, THE Property_Manager SHALL return Properties where `title` or `address` contains the search term (case-insensitive), scoped to the user's visibility.
2. WHEN a user requests `GET /api/properties/?address={value}`, THE Property_Manager SHALL return Properties with an address matching the filter value, scoped to the user's visibility.
3. THE Property_Manager SHALL apply Visibility Rules before applying search or filter parameters.

---

### Requirement 12: Late Payment Tracking (Future Enhancement)

**User Story:** As an Owner, I want to identify overdue payments, so that I can follow up with tenants who have not paid on time.

#### Acceptance Criteria

1. WHEN the current date is past the first day of a payment's `month` and `is_paid=False`, THE System SHALL consider that RentPayment overdue.
2. WHEN an Owner requests `GET /api/payments/?overdue=true`, THE Payment_Manager SHALL return all overdue RentPayments for the Owner's properties.
3. THE Payment_Manager SHALL include an `is_overdue` computed field in RentPayment responses indicating whether the payment is overdue.
