# Local Services Booking Platform — V1 Specification

## 1. Project Overview

**Local Services Booking Platform** is a Flask web application that allows customers to book local services from providers.

The application serves both:

* Backend logic using Flask routes and Python modules.
* Frontend pages using Jinja templates, HTML, CSS, and JavaScript.

The first version will focus on a simple, complete booking cycle.

## 2. Main Goal

Build a simple platform where:

* A customer can register and log in.
* A customer can browse available services.
* A customer can create a booking request.
* A provider can accept, reject, start, or complete bookings.
* A customer can review a completed booking.
* An admin can view the main system data.

## 3. User Roles

### Customer

A customer can:

* Register.
* Log in.
* View services.
* View service details.
* Create booking requests.
* View their own bookings.
* Cancel pending bookings.
* Add a review after booking completion.

### Provider

A provider can:

* Log in.
* View booking requests.
* Accept booking requests.
* Reject booking requests.
* Mark accepted bookings as in progress.
* Mark in-progress bookings as completed.

### Admin

An admin can:

* View users.
* View services.
* View bookings.
* View reviews.

For V1, admin actions can be simple read-only pages.

## 4. Booking Lifecycle

The booking status cycle will be:

```text
PENDING
ACCEPTED
REJECTED
IN_PROGRESS
COMPLETED
CANCELLED
```

### Status Rules

* A new booking starts as `PENDING`.
* A provider can change `PENDING` to `ACCEPTED`.
* A provider can change `PENDING` to `REJECTED`.
* A provider can change `ACCEPTED` to `IN_PROGRESS`.
* A provider can change `IN_PROGRESS` to `COMPLETED`.
* A customer can change `PENDING` to `CANCELLED`.
* A customer can review only `COMPLETED` bookings.

## 5. V1 Features

### Authentication

* Register.
* Log in.
* Log out.
* Store logged-in user data in the Flask session.
* Support the following roles:

  * `CUSTOMER`
  * `PROVIDER`
  * `ADMIN`

### Services

* List all services.
* View service details.
* Store services in a JSON file for V1.

### Bookings

* A customer can create a booking.
* A customer can view their bookings.
* A provider can view booking requests.
* A provider can update booking statuses.

### Reviews

* A customer can add a review for a completed booking.
* Service and provider pages can display reviews later.

### Admin

* Provide a simple admin dashboard.
* Show basic counts:

  * Users count.
  * Services count.
  * Bookings count.
  * Reviews count.

## 6. Storage

For V1, data will be stored in JSON files:

```text
data/users.json
data/services.json
data/bookings.json
data/reviews.json
```

## 7. Architecture

The project will use a clean modular structure:

```text
module/
├── domain/
├── application/
├── infrastructure/
└── api/
```

### Domain Layer

Contains core entities, value objects, and enums.

Examples:

```text
User
Role
Booking
BookingStatus
```

The domain layer must not depend on:

* Flask.
* Templates.
* JSON files.
* Database code.
* Infrastructure code.

### Application Layer

Contains application use cases and business workflows.

Examples:

* Register a user.
* Log in a user.
* Create a booking.
* Accept a booking.
* Complete a booking.

### Infrastructure Layer

Contains technical implementation details.

For V1, repositories will read from and write to JSON files.

### API Layer

Contains Flask routes.

Routes are responsible for:

1. Receiving form data.
2. Validating request data.
3. Calling application services.
4. Returning templates or redirects.

Business logic should not be implemented directly inside Flask routes.

## 8. Validation Rules

### Registration

* Name is required.
* Email is required.
* Email must have a valid format.
* Password is required.
* Password must contain at least six characters.
* Confirm password must match the password.
* Email must be unique.

### Login

* Email is required.
* Password is required.
* Email and password must be correct.

### Booking

* Service is required.
* Date is required.
* Time is required.
* Address is required.
* Problem description is optional but recommended.

## 9. Pages for V1

### Public Pages

* Home page.
* Registration page.
* Login page.
* Services page.
* Service details page.

### Customer Pages

* Customer dashboard.
* My bookings page.
* Create booking page.
* Booking details page.

### Provider Pages

* Provider dashboard.
* Booking requests page.
* Booking details page.

### Admin Pages

* Admin dashboard.

## 10. Out of Scope for V1

The following features will not be implemented in the first version:

* Online payments.
* Real-time chat.
* Notifications.
* Email sending.
* Google Maps integration.
* Provider availability calendar.
* Advanced admin analytics.
* REST API for mobile applications.
* PostgreSQL database.
* Docker deployment.

## 11. Development Workflow

The project will follow a feature-branch workflow:

```text
main
  ↓
feature/name
  ↓
pull request
  ↓
merge into main
```

Example branches:

```text
feature/user-auth
feature/services
feature/bookings
feature/reviews
docs/project-spec
```

Each feature should be committed separately with a clear commit message.
