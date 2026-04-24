# Project Brief: Mobile-Friendly Tenant & Rent Portal
**Prepared for:** Jules
**Status:** Implementation Plan – Frontend Focus
**Approach:** API-First / Mobile-Responsive

## 1. Project Objective
To design and implement a mobile-optimized web interface that allows property owners to manage tenants and view rent history. All data operations will be performed via asynchronous JavaScript calls to existing Django REST Framework (DRF) APIs.

## 2. Core Requirements
* **Mobile-First Design:** Implementation of responsive CSS (Flexbox/Grid) to ensure full usability on mobile devices.
* **Decoupled Frontend:** Direct reliance on existing API endpoints. No server-side rendering (SSR) will be utilized for UI logic.
* **Minimal Backend Interaction:** Backend modifications will be restricted strictly to creating missing endpoints required for the frontend functionality.

## 3. Execution Roadmap

| Phase | Task Description |
| :--- | :--- |
| **I. Frontend Layout** | Development of responsive shell, mobile-nav, and adaptive data tables/cards for tenant lists. |
| **II. API Integration** | Implementation of `fetch()` logic to handle `GET`, `POST`, and `DELETE` requests. |
| **III. Dynamic UI** | DOM-injection logic to display rent history and update tenant lists without page refreshes. |
| **IV. Backend Gap-Fill** | (Conditional) Development of supplemental DRF views only where API gaps are identified. |

## 4. Technical Constraints
* **API Protocol:** All requests must be handled via standard RESTful patterns.
* **Auth Handling:** Authentication state will be managed via the client-side session or token headers as currently established in the project.
* **Scope Limitation:** Development is strictly limited to the necessary interactions between the browser and the API.
