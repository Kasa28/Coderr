# Coderr Backend

Coderr is a marketplace application for digital services. Business users can create offers with different packages, while customers can browse offers, place orders, and review providers.

This repository contains the Django REST API for the separate Coderr frontend.

## Features

- Registration and token-based login
- Customer and business user roles
- Guest login for demo users
- Customer and business profiles
- Offers with Basic, Standard, and Premium packages
- Offer search, filtering, ordering, and pagination
- Order and order status management
- Reviews for business users
- Automated API tests

## Technologies

- Python
- Django 6
- Django REST Framework
- Django Filter
- SQLite
- Token Authentication
- django-cors-headers
- Pillow

## Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Apply the database migrations:

```powershell
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```

The API is available at:

```text
http://127.0.0.1:8000/api/
```

The separate frontend can be started with VS Code Live Server at `http://127.0.0.1:5500/`.

## Guest Login

The application provides guest access for both user roles without registration or a password.

```text
POST /api/guest-login/
```

Example request:

```json
{
  "type": "customer"
}
```

The allowed values are `customer` and `business`.

Guest accounts are shared between visitors and are intended only for demonstration and testing. Changes made by one guest may be visible to other visitors.

## Authentication

Protected API requests require the token returned by the login endpoint:

```text
Authorization: Token YOUR_TOKEN
```

## Main API Routes

- `/api/registration/`
- `/api/login/`
- `/api/guest-login/`
- `/api/profile/<user_id>/`
- `/api/offers/`
- `/api/orders/`
- `/api/reviews/`
- `/api/base-info/`

## Tests

Run all tests with:

```powershell
python manage.py test
```

Run the tests for a specific app with, for example:

```powershell
python manage.py test profile_app
```

## Note

The current settings are intended for local development. Before a public deployment, values such as the secret key, debug mode, allowed hosts, CORS settings, and database configuration must be prepared for production.
