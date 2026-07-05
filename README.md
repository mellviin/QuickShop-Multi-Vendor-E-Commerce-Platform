# Quickshop E-commerce

**Quickshop** is a Django-based grocery marketplace web application that supports two roles: consumers and sellers. Consumers can browse products, manage carts and wishlists, checkout, and view order history. Sellers can add and manage products, view incoming orders, and update order statuses.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Models](#models)
- [URLs and Pages](#urls-and-pages)
- [Requirements](#requirements)
- [Local Setup](#local-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development Notes](#development-notes)
- [Known Limitations](#known-limitations)
- [Recommended Improvements](#recommended-improvements)
- [License](#license)

## Features

- Role-based authentication and authorization
  - Consumer account registration, login, logout, profile view/edit
  - Seller account registration, login, seller dashboard access
  - Custom role validation during login
- Product catalog management
  - Product listing for consumers
  - Product detail pages
  - Seller product creation, editing, and deletion
- Cart and wishlist functionality
  - Add/remove products from cart
  - Add/remove products from wishlist
  - Buy-now flow from product page
- Order management
  - Checkout page with shipping details
  - Payment page and simulated payment processing
  - Order confirmation and order history for consumers
  - Seller order list and status update capability
- Notifications and email flow
  - Order confirmation email to customer
  - New order notification email to seller
- Admin support
  - Django admin available at `/admin/`
  - Custom admin panel available at `/admin-panel/dashboard/`
- File upload support
  - Product images stored in `media/products/`

## Technology Stack

- Python 3
- Django web framework
- SQLite database (`db.sqlite3`)
- HTML templates and CSS
- Local static files in `static/`
- Local media uploads in `media/`

## Architecture

The application follows a modular Django app structure.

- `quickshop/accounts/` — authentication, registration, profile management
- `quickshop/products/` — product listing and product detail pages
- `quickshop/cart/` — cart and wishlist handling
- `quickshop/orders/` — checkout and order history
- `quickshop/seller/` — seller dashboard and order status control
- `admin_app/` — additional admin dashboard views
- `payment/` — payment processing flow and confirmation
- `templates/` — HTML templates used by each app
- `static/` — CSS, JavaScript, and image assets

## Models

- `Profile`
  - Extends Django `User` with `role` and optional `phone`
  - Role choices: `consumer`, `seller`
- `Product`
  - Seller-owned product
  - Fields: `name`, `category`, `description`, `price`, `quantity`, `image`
- `CartItem`
  - Product items saved in a user's cart
  - Unique per `(user, product)`
- `WishlistItem`
  - Items a user added to their wishlist
  - Unique per `(user, product)`
- `Order`
  - Stores order requests from consumers
  - Tracks shipping address, payment method, current status

## URLs and Pages

### Global URLs

- `/` — account login and registration flow
- `/admin/` — Django admin site
- `/admin-panel/dashboard/` — custom admin panel view
- `/products/` — consumer home / product listing
- `/products/detail/<product_id>/` — product detail page
- `/cart/` — cart page
- `/cart/add/<product_id>/` — add product to cart
- `/cart/remove/<item_id>/` — remove product from cart
- `/cart/wishlist/` — user wishlist page
- `/cart/wishlist/add/<product_id>/` — add product to wishlist
- `/cart/wishlist/remove/<item_id>/` — remove wishlist item
- `/cart/buy-now/<product_id>/` — buy now shortcut to checkout
- `/orders/checkout/` — shipping details and checkout page
- `/orders/payment/` — payment entry page
- `/orders/payment-success/` — order success page
- `/orders/` — user order history page
- `/seller/dashboard/` — seller dashboard
- `/payment/process/` — simulated payment processing
- `/payment/success/` — payment success page

## Requirements

- Python 3.8 or later
- Django
- Pillow

> This repository does not include a `requirements.txt` file. Install dependencies manually until one is added.

## Local Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install django pillow
```

### 3. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

### 6. Open in browser

- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Configuration

### Recommended environment variables

Do not use the hard-coded secret key or email credentials in production. Replace them with environment variables and secure configuration.

Suggested settings to configure:

- `SECRET_KEY`
- `DEBUG=False` in production
- `ALLOWED_HOSTS`
- `DATABASE_URL` or SQLite path
- SMTP settings for email delivery

### Email settings in `quickshop/settings.py`

The app currently configures Gmail SMTP with hard-coded values. For development, use Django's console email backend or environment-based mail settings.

## Usage

### Consumer flow

1. Register as a consumer on the home page.
2. Login and browse products at `/products/`.
3. View product details on `/products/detail/<product_id>/`.
4. Add items to cart or wishlist.
5. Use Buy Now to move directly to checkout.
6. Complete checkout with shipping details.
7. View payment confirmation and order history at `/orders/`.

### Seller flow

1. Register as a seller.
2. Login and access `/seller/dashboard/`.
3. Add new products with name, category, price, quantity, description, and image.
4. Edit or delete existing products.
5. View incoming orders and update their status.

### Admin flow

1. Visit `/admin/` for Django admin.
2. Manage users, products, orders, and posted data from the Django backend.
3. Visit `/admin-panel/dashboard/` for the custom admin dashboard page.

## Development Notes

- The payment flow is simulated through `payment/views.py`; it does not integrate with a real payment gateway.
- Order confirmation emails are sent via Django's `send_mail` if email settings are configured.
- Uploaded product images are written to `media/products/`.
- Customer checkout data is temporarily stored in session during the payment process.
- There are duplicated `orders/views.py` sections; one copy likely reflects older code. Review and clean duplicates before extending the app.

## Known Limitations

- No `requirements.txt` or dependency lock file is present.
- Hard-coded credentials in `quickshop/settings.py` are insecure.
- The payment process is not production-ready.
- There are no automated tests included in this repository.
- Email sending uses Gmail SMTP credentials from source code.

## Recommended Improvements

- Add `requirements.txt` or `pyproject.toml`
- Add unit tests and integration tests
- Use environment variables for sensitive settings
- Replace simulated payment with a real gateway integration
- Improve order and checkout data models
- Add search, filtering, and category navigation for products
- Add user-friendly error handling in forms
- Add documentation for data seeding and sample content

## License

This repository does not include an explicit license file.
