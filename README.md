# Local Services Booking Platform

A Flask web application that allows customers to book local services from providers.

The project is built as a simple but complete V1 platform with authentication, services, bookings, reviews, admin dashboard, tests, and GitHub Actions.

---

## Features

### Authentication

- Register
- Login
- Logout
- Session-based authentication
- Role-based access control

### User Roles

- Customer
- Provider
- Admin

### Customer Features

- Browse available services
- View service details
- Create booking requests
- View own bookings
- Cancel pending bookings
- Review completed bookings
- View submitted reviews

### Provider Features

- Create services
- View own services
- View booking requests
- Accept booking requests
- Reject booking requests
- Start accepted bookings
- Complete in-progress bookings

### Admin Features

- View dashboard statistics
- View users
- View services
- View bookings
- View reviews

---

## Booking Status Flow

```text
PENDING
  ↓
ACCEPTED
  ↓
IN_PROGRESS
  ↓
COMPLETED