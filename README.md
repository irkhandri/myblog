# 

## myblog Overview

This project is a Django-based blog system that allows users to create and manage blog posts, comments, assign tags to posts, view authors' profiles and interests, and exchange messages with authors.

## Features

- Create, read, update, and delete blog posts.
- Tagging for categorizing blog posts.
- Commenting and rate blog posts.
- Author profiles with information about their interests.
- Messaging system to contact authors.

## Getting Started

### Prerequisites

Before you get started, make sure you have the following installed:

- Python 3
- Django
- Other project dependencies ( in `requirements.txt`)

### Installation

1. Clone the repository:

   
   git clone https://github.com/irkhandri/myblog.git
   cd django-blog-project

2. Create a virtual environment and activate:
   python -m venv venv
     depends on OS
   source venv/bin/activate
3. Install project dependencies:
   pip install -r requirements.txt
4. Apply database migrations:
   python manage.py migrate
5. Ceate a superuser (admin) for managing the blog:
   python manage.py createsuperuser
6. Start the development server:
   python manage.py runserver


## Usage

Access the admin panel at http://localhost:8000/admin/ to manage blog posts, tags, authors, comments, and messages.
Visit the blog homepage at http://localhost:8000/ to view and interact with the blog.

##Project Structure

blogs/: Django app for the main blog functionality, blog post tags, comments.
users/: Django app for managing author profiles and interests, messages.
templates/: HTML templates for the project.
static/: Static files (CSS, JavaScript, images, etc.).

## API

api/: Django app for creating API endpoints.

