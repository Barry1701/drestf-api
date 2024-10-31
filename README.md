# DRESTF-API Backend

This project is a backend API for a social platform centered around product recommendations and interactions. Built with Django and Django REST Framework, it provides endpoints for managing user profiles, posts, products, categories, comments, likes, and followers.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)

---

## Features

- **User Authentication:** Registration, login, logout, and token-based authentication (JWT).
- **Profiles and Followers:** Manage user profiles, and follow/unfollow functionality.
- **Posts and Comments:** Create, read, update, and delete posts and comments.
- **Product and Category Management:** Allows adding products with categories for easy filtering.
- **Likes and Interactions:** Like posts, and view popular profiles.

## Technologies

- **Django** - Web framework for building the backend.
- **Django REST Framework** - API framework for building RESTful endpoints.
- **PostgreSQL** - Database for data persistence.
- **Cloudinary** - Cloud storage for media files.
- **Gunicorn** - WSGI HTTP Server for deployment.
- **JWT Authentication** - For secure user authentication.

## Getting Started

To run this project locally, follow these steps.

### Prerequisites

- **Python 3.x** - Ensure Python is installed on your system.
- **PostgreSQL** - Install PostgreSQL for database management.

### Installation

1. Clone the repository:
   ```bash
   git clone <https://barry1701-drestfapi-55a6l76ssak.ws.codeinstitute-ide.net/>
   cd DRESTF-API
2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt

## Database Setup and Running the Project

1. Run migrations to set up the database schema and to start Dev Server:
   ```bash
   python manage.py migrate

   python manage.py runserver

2. Create a superuser for accessing the Django admin panel:

   ```bash
   python manage.py createsuperuser
Navigate to `http://127.0.0.1:8000/` in your browser to access the API locally.

## Deployment

The project is set up for deployment on platforms like **Heroku**. Make sure to set `DEBUG=False` and configure your database and environment variables on the hosting platform.

 ## API Endpoints

Here’s a list of the primary endpoints in the API:

### Authentication
- `POST /dj-rest-auth/login/` - Login
- `POST /dj-rest-auth/logout/` - Logout
- `POST /dj-rest-auth/registration/` - Register

### Profiles
- `GET /profiles/` - List all profiles
- `GET /profiles/<id>/` - Get a single profile

### Posts
- `GET /posts/` - List all posts
- `POST /posts/` - Create a new post
- `GET /posts/<id>/` - Get a single post

### Comments
- `POST /comments/` - Add a comment to a post
- `DELETE /comments/<id>/` - Delete a comment

### Products and Categories
- `GET /products/` - List all products
- `GET /categories/` - List all categories
- `POST /products/` - Add a product with a category
  
## Environment Variables

Set up your `.env` file in the root directory to include the following environment variables:

```plaintext
SECRET_KEY=your_secret_key
DEBUG=True  # Set to False in production
DATABASE_URL=your_database_url  # e.g., postgresql://user:password@localhost:5432/dbname
CLOUDINARY_URL=your_cloudinary_url
ALLOWED_HOSTS=localhost,127.0.0.1  # Add your domain here in production

