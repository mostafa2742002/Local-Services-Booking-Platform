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
```

Other possible statuses:

- `REJECTED`
- `CANCELLED`

### Rules

- New booking starts as `PENDING`.
- Provider can accept or reject pending bookings.
- Provider can start accepted bookings.
- Provider can complete in-progress bookings.
- Customer can cancel only pending bookings.
- Customer can review only completed bookings.
- Customer cannot review the same booking twice.

## Tech Stack

- Python
- Flask
- Jinja Templates
- HTML
- CSS
- JSON file storage
- Pytest
- GitHub Actions

## Project Structure

```text
local_services_app/
├── app/
│   ├── admin/
│   ├── booking/
│   ├── common/
│   ├── review/
│   ├── service/
│   ├── user/
│   ├── static/
│   └── templates/
├── data/
├── docs/
├── tests/
├── .github/
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Architecture

The project uses a modular clean structure.

Each main feature is separated into layers:

```text
module/
├── api/
├── application/
├── domain/
└── infrastructure/
```

### API Layer

Handles Flask routes, request data, redirects, templates, and flash messages.

### Application Layer

Contains business logic and use cases.

### Domain Layer

Contains core entities and enums.

### Infrastructure Layer

Handles JSON storage and repository logic.

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd local_services_app
```

### 2. Create virtual environment

```bash
python3 -m venv venv
```

### 3. Activate virtual environment

```bash
source venv/bin/activate
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the app

```bash
python3 run.py
```

Open <http://127.0.0.1:5000>.

## Run Tests

```bash
pytest
```

## Test Accounts

For local testing, users are created from the register page.

By default, registered users are created as `CUSTOMER`.

To test provider or admin features in V1, manually update the user role inside `data/users.json`.

Example:

```json
"role": "PROVIDER"
```

or:

```json
"role": "ADMIN"
```

## Main Routes

### Auth

- `/auth/register`
- `/auth/login`
- `/auth/logout`

### Services

- `/services/`
- `/services/<service_id>`
- `/services/provider/my-services`
- `/services/provider/create`

### Bookings

- `/bookings/create/<service_id>`
- `/bookings/my-bookings`
- `/bookings/provider/requests`

### Reviews

- `/reviews/create/<booking_id>`
- `/reviews/my-reviews`

### Admin

- `/admin/dashboard`

## Testing and CI

The project includes unit tests for:

- User validation
- User service
- Service validation
- Service service
- Booking validation
- Booking service
- Review validation
- Review service
- Admin dashboard service

GitHub Actions runs tests automatically on push and pull requests.

## Development Workflow

The project follows a feature-branch workflow:

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

- `feature/user-auth`
- `feature/services`
- `feature/bookings`
- `feature/reviews`
- `feature/admin-dashboard`
- `docs/readme`

## V1 Scope

Implemented in V1:

- Authentication
- Services
- Bookings
- Reviews
- Admin dashboard
- Unit tests
- GitHub Actions

Out of scope for V1:

- Online payment
- Chat
- Notifications
- Provider calendar
- Google Maps
- PostgreSQL database
- Docker deployment
- Advanced admin actions

## Future Improvements

- Move from JSON files to PostgreSQL
- Add provider registration/admin approval
- Add service editing and deletion
- Add booking details page
- Add admin user management
- Add better dashboard analytics
- Add pagination and search
- Add Docker support
- Add deployment configuration

---

## Run Tests

```bash
pytest
```
