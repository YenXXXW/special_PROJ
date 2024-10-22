## Cane Handicrafts Ecommerce

### Overview

Cane Handicrafts Ecommerce is a Django-based platform designed to connect shops specializing in cane handicrafts with customers. Users can browse products from multiple shops, add items to their cart, adjust quantities, and complete purchases. A superadmin manages the entire website through the built-in Django admin panel, while individual shop admins have their own custom admin panels to manage their products and orders.
Features

    User Registration & Authentication: Users can register, log in, and manage their accounts.
    Multi-Shop Platform: Customers can view products from various shops in one place.
    Product Management: Shop admins can add, update, and delete products from their respective shops.
    Shopping Cart: Users can add items to their cart, increase or decrease quantities, and remove items.
    Checkout Process: Seamless checkout experience for customers to complete their purchases.
    Admin Panels:
        Superadmin Panel: Full control over all shops, users, and site settings.
        Shop Admin Panel: Custom management interface for each shop admin.

### Technologies Used

    Backend: Django
    Database: SQLite (or PostgreSQL, MySQL, etc., depending on deployment)
    Frontend: HTML, CSS, JavaScript (optional frameworks like Bootstrap or React can be integrated)
    Admin Panel: Django Admin and custom admin panels

### Installation
#### Prerequisites

    Python 3.x
    Django
    pip

Steps

    Clone the Repository:

    bash

git clone https://github.com/yourusername/cane-handicrafts-ecommerce.git
cd cane-handicrafts-ecommerce

#### Install Dependencies:

pip install -r requirements.txt

### Apply Migrations:

python manage.py migrate

### Create a Superuser:

python manage.py createsuperuser

### Run the Development Server:


    python manage.py runserver

    Access the Application: Open your web browser and navigate to http://127.0.0.1:8000.

    Admin Panels:
        Superadmin: http://127.0.0.1:8000/admin
        Shop Admin: Access through custom URLs defined in the application.

Usage

    Customers: Register and browse products. Use the cart functionality to manage items before checkout.
    Shop Admins: Log in to your custom admin panel to manage products and orders.
    Superadmin: Use the Django admin panel to manage users, shops, and overall site settings.


