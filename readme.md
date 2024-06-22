# ProySales

Welcome to **ProySales**, a Django-based project designed to streamline sales, customer, supplier, and product management. This project provides a robust backend system for handling various aspects of a sales operation, including invoicing, user profiles, and shopping carts.

## Features

- **Brand Management**
- **Supplier Management**
- **Product Management**
- **Category Management**
- **Customer Management**
- **Invoice and Invoice Detail Management**
- **User Profile Management**
- **Shopping Cart Functionality**

## Models Overview

### Brand
Manage product brands with descriptions, user association, and state.

### Supplier
Handle suppliers with details like name, RUC, address, and phone.

### Product
Maintain products with descriptions, cost, price, stock, IVA, expiration date, brand, supplier, and categories.

### Category
Organize products into categories.

### Customer
Manage customer details including names, address, gender, date of birth, phone, email, and profile image.

### Invoice
Create and manage invoices with customer details, issue date, subtotal, IVA, discount, total, payment, and status.

### Invoice Detail
Detailed items within an invoice including product, cost, quantity, price, subtotal, and IVA.

### Profile
Extend user profiles with additional fields and profile images.

### Cart
Manage shopping carts with items and calculate total cost and quantity.

### CartItem
Items within a shopping cart including product and quantity.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/proy_sales.git
    cd proy_sales
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

4. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

5. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6. **Access the application:**
    Open your browser and go to `http://127.0.0.1:8000`.

## Contributing

1. **Fork the repository.**
2. **Create a new branch:**
    ```bash
    git checkout -b feature-name
    ```
3. **Commit your changes:**
    ```bash
    git commit -m 'Add some feature'
    ```
4. **Push to the branch:**
    ```bash
    git push origin feature-name
    ```
5. **Create a pull request.**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Documentation
- Django REST Framework Documentation

---

Enjoy using **ProySales**! Your contributions and feedback are welcome.