# Local Services Booking Platform

This is a Flask web application for booking local services between customers and providers. Customers can browse services, place bookings, save booking drafts in the browser with `localStorage`, and review completed work, while providers can publish services and manage booking requests through the full status flow.

The main feature I implemented beyond the basic booking flow is browser-side booking draft persistence, so a partially completed booking form survives refreshes until the user submits it.

## Prerequisites

No extra Python modules are required beyond the dependencies already listed in `requirements.txt`. The project uses Flask together with standard library modules such as `datetime`, `uuid`, `json`, `pathlib`, `os`, and `re`.

## Project Checklist

- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
  - Entry point: [run.py](run.py#L1)
  - App factory and blueprint registration: [app/__init__.py](app/__init__.py#L1)
- [x] It uses at least one module from the Python Standard Library other than the random module.
  - Module names: `datetime`, `uuid`, `json`, `pathlib`, `os`, `re`
- [x] It contains at least one class written by you that has both properties and methods.
  - Class definition: [app/booking/domain/booking.py](app/booking/domain/booking.py#L5)
  - Two properties: `customer_id`, `status`
  - Two methods: `get_status_label`, `can_customer_cancel`
  - Methods used in the app: [app/templates/bookings/customer_bookings.html](app/templates/bookings/customer_bookings.html#L63), [app/templates/bookings/customer_bookings.html](app/templates/bookings/customer_bookings.html#L98), [app/templates/bookings/provider_bookings.html](app/templates/bookings/provider_bookings.html#L48)
- [x] It makes use of JavaScript in the front end and uses the `localStorage` of the web browser.
  - Booking draft handling: [app/static/js/booking_draft.js](app/static/js/booking_draft.js#L1)
- [x] It uses modern JavaScript.
  - The front-end scripts use `const` and modern DOM event handling in [app/static/js/booking_draft.js](app/static/js/booking_draft.js#L1) and [app/static/js/services.js](app/static/js/services.js#L1)
- [x] It makes use of the reading and writing to the same file feature.
  - JSON repositories read and write the same files in [app/booking/infrastructure/booking_repository.py](app/booking/infrastructure/booking_repository.py#L1), [app/service/infrastructure/service_repository.py](app/service/infrastructure/service_repository.py#L1), and [app/user/infrastructure/user_repository.py](app/user/infrastructure/user_repository.py#L1)
- [x] It contains conditional statements.
  - Example: [app/booking/api/booking_routes.py](app/booking/api/booking_routes.py#L31)
- [x] It contains loops.
  - Example: [app/service/api/service_routes.py](app/service/api/service_routes.py#L94)
- [x] It lets the user enter a value in a text box at some point.
  - Booking form values are received and validated in [app/booking/api/booking_routes.py](app/booking/api/booking_routes.py#L58) and [app/booking/api/booking_validator.py](app/booking/api/booking_validator.py#L1)
  - Service form values are received and validated in [app/service/api/service_routes.py](app/service/api/service_routes.py#L63) and [app/service/api/service_validator.py](app/service/api/service_validator.py#L1)
- [x] It doesn't generate any error message even if the user enters a wrong input.
  - Invalid input is handled with validation and browser flash messages in [app/booking/api/booking_routes.py](app/booking/api/booking_routes.py#L64) and [app/service/api/service_routes.py](app/service/api/service_routes.py#L74)
- [x] It is styled using your own CSS.
- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code.
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Run the app:

   ```powershell
   python run.py
   ```

4. Open the app in your browser at `http://127.0.0.1:5000`.

## Tests

Run the test suite with:

```powershell
pytest 
```