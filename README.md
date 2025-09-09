# 🍋 Little Lemon Restaurant API

A Django REST Framework (DRF) powered backend API for the fictional **Little Lemon Restaurant**.  
This project implements **user authentication**, **role-based access control**, and full restaurant operations:  
menu management, cart system, and order processing.

---

## 🚀 Features

- 👤 **User Management**
  - Register new users (`/api/users/`)
  - Get current user profile (`/api/users/users/me/`)
  - Login with token-based authentication (`/token/login/`)

- 👥 **Role-based Access**
  - Manager group: manage staff & menu
  - Delivery crew: access assigned orders
  - Customers: browse menu, manage cart, place orders

- 🍽️ **Menu & Orders**
  - List & manage menu items (`/api/menu-items/`)
  - Add items to cart (`/api/cart/menu-items/`)
  - Place and track orders (`/api/orders/`)

---

## ⚙️ Tech Stack

- [Django 5.x](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Djoser](https://djoser.readthedocs.io/) (user management endpoints)
- Token Authentication

---

## 📂 API Endpoints

### 🔐 Authentication
| Endpoint              | Method | Role        | Description |
|-----------------------|--------|------------|-------------|
| `/api/users/`         | POST   | Public     | Register a new user |
| `/api/users/users/me/`| GET    | Auth User  | Get current user details |
| `/token/login/`       | POST   | Public     | Obtain authentication token |

### 🍴 Menu
| Endpoint              | Method | Role        | Description |
|-----------------------|--------|------------|-------------|
| `/api/menu-items/`    | GET    | Public     | List all menu items |
| `/api/menu-items/`    | POST   | Manager    | Add new menu item |
| `/api/menu-items/<id>/` | PUT/PATCH/DELETE | Manager | Update/Delete item |

### 🛒 Cart
| Endpoint              | Method | Role        | Description |
|-----------------------|--------|------------|-------------|
| `/api/cart/menu-items/` | GET   | Customer   | View current user cart |
| `/api/cart/menu-items/` | POST  | Customer   | Add menu item to cart |
| `/api/cart/menu-items/` | DELETE| Customer   | Clear cart |

### 📦 Orders
| Endpoint              | Method | Role        | Description |
|-----------------------|--------|------------|-------------|
| `/api/orders/`        | GET/POST | Customer | List or place orders |
| `/api/orders/<id>/`   | GET    | Authenticated | View specific order |
| `/api/orders/<id>/`   | PATCH  | Manager/Delivery Crew | Update order status |

---

## 🛠️ Setup & Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/littlelemon-django-api.git
   cd littlelemon-django-api
