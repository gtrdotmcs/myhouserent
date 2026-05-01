# Tasks

## Task List

- [ ] 1. Verify existing core functionality
  - [ ] 1.1 Run verify_api.py to confirm baseline visibility logic passes for all roles
  - [ ] 1.2 Review rentals/tests.py and add missing unit tests for authentication (session, basic auth, unauthenticated → 403)
  - [ ] 1.3 Add unit tests for user management: superuser creates user, non-superuser gets 403, password not exposed in response
  - [ ] 1.4 Add unit tests for pay action: correct tenant → 200 + response body; wrong user → 403
  - [ ] 1.5 Add unit tests for approve action: owner → 200 + response body; tenant → 403
  - [ ] 1.6 Add unit tests for cross-role isolation: owner A cannot access owner B's resources (404); tenant A cannot access tenant B's resources (404)

- [ ] 2. Property-based tests for core invariants
  - [ ] 2.1 Set up hypothesis and hypothesis-django in the project (add to requirements/dependencies)
  - [ ] 2.2 Write property test for P3: only superusers can create users (generate OWNER/TENANT users, assert POST /api/users/ → 403)
  - [ ] 2.3 Write property test for P5: non-superuser list returns only own record (generate N users, assert list length == 1 and id matches)
  - [ ] 2.4 Write property test for P8: role-scoped property visibility (generate owners with multiple properties, assert each owner only sees their own)
  - [ ] 2.5 Write property test for P10: role-scoped agreement visibility (generate owners/tenants with agreements, assert scoping holds)
  - [ ] 2.6 Write property test for P12: role-scoped payment visibility (generate payments across multiple owners/tenants, assert scoping holds)
  - [ ] 2.7 Write property test for P13: is_approved immutable via tenant PUT/PATCH (generate payments, tenant PATCH with is_approved=true, assert unchanged)
  - [ ] 2.8 Write property test for P14: pay action sets is_paid=True and paid_date=today (generate payments, call pay(), assert fields)
  - [ ] 2.9 Write property test for P19: cross-owner isolation returns 404 (generate two owners with separate resources, assert 404 on cross-access)
  - [ ] 2.10 Write property test for P20: cross-tenant isolation returns 404 (generate two tenants, assert 404 on cross-access)

- [ ] 3. Requirement 9: JWT Token Authentication
  - [ ] 3.1 Add djangorestframework-simplejwt to project dependencies
  - [ ] 3.2 Add JWTAuthentication to DEFAULT_AUTHENTICATION_CLASSES in settings.py
  - [ ] 3.3 Configure SIMPLE_JWT settings: ACCESS_TOKEN_LIFETIME=60min, REFRESH_TOKEN_LIFETIME=7days
  - [ ] 3.4 Add JWT token URLs to house_rent_project/urls.py (obtain and refresh endpoints)
  - [ ] 3.5 Write unit test: obtain tokens with valid credentials → returns access + refresh tokens
  - [ ] 3.6 Write unit test: refresh token → returns new access token
  - [ ] 3.7 Write unit test: decode access token and verify exp claim ≤ 60 minutes from issue
  - [ ] 3.8 Write property test for P21: valid JWT authenticates requests to protected endpoints
  - [ ] 3.9 Write property test for P22: invalid/expired JWT returns 401

- [ ] 4. Requirement 10: Payment Filtering
  - [ ] 4.1 Add django-filter to project dependencies and configure DEFAULT_FILTER_BACKENDS in settings.py
  - [ ] 4.2 Create RentPaymentFilter (FilterSet) with fields: agreement, month, is_paid, is_approved
  - [ ] 4.3 Set filterset_class = RentPaymentFilter on RentPaymentViewSet
  - [ ] 4.4 Write property test for P23: filter by agreement respects visibility scope
  - [ ] 4.5 Write property test for P24: filter by is_paid returns correct subset within visibility scope
  - [ ] 4.6 Write property test for P25: filter by month returns correct subset within visibility scope

- [ ] 5. Requirement 11: Property Search and Filtering
  - [ ] 5.1 Add SearchFilter and OrderingFilter to PropertyViewSet.filter_backends
  - [ ] 5.2 Set search_fields = ['title', 'address'] on PropertyViewSet
  - [ ] 5.3 Add filterset_fields = ['address'] for exact address filtering
  - [ ] 5.4 Write property test for P26: search is case-insensitive and visibility-scoped (generate properties with known titles, search with varied casing, assert results never exceed visibility scope)

- [ ] 6. Requirement 12: Late Payment Tracking
  - [ ] 6.1 Add is_overdue SerializerMethodField to RentPaymentSerializer
  - [ ] 6.2 Add ?overdue=true filter support in RentPaymentViewSet.get_queryset (month__lt=today, is_paid=False)
  - [ ] 6.3 Write property test for P27: is_overdue is correctly computed for all combinations of month and is_paid
  - [ ] 6.4 Write property test for P28: overdue filter returns only overdue payments scoped to owner's properties
  - [ ] 6.5 Run verify_api.py to confirm no regressions in visibility logic after all changes
