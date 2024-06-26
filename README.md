# library-management-system-api
This project is a RESTful API for managing books in a library system. The API allows users to perform CRUD (Create, Read, Update, Delete) operations on books and includes user sessions to provide a personalized experience.

## Features

- **CRUD Operations**: Create, read, update, and delete books.
- **User Authentication**: Users can register, login, and manage their sessions.
- **Favorites**: Users can mark books as favorites.
- **API Endpoints**: Well-defined API endpoints for managing books and user sessions.

## Technologies Used

- **Python**: Programming language.
- **Django**: Web framework.
- **Django REST Framework (DRF)**: Toolkit for building Web APIs in Django.
- **SQLite**: Default database for development.

## Installation

### Prerequisites

- Python 3.x
- Django
- Django REST Framework

### Clone the Repository

```bash
git clone https://github.com/krachid98/library-management-system-api.git
cd library-management-system-api
```

## Create and Activate Virtual Environment
```bash
python3 -m venv env
source venv/bin/activate
```

## Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Create superuser and runserver
```bash
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoints
## Authentication
- Register: POST /api/register/
- Login: POST /api/login/
- Logout: POST /api/logout/

## Books
- List Books: GET /api/books/
- Create Book: POST /api/books/
- Retrieve Book: GET /api/books/{id}/
- Update Book: PUT /api/books/{id}/
- Delete Book: DELETE /api/books/{id}/

## Favorites
- List Favorites: GET /api/favorites/
- Add Favorite: POST /api/favorites/{bookId}/
- Remove Favorite: DELETE /api/favorites/{bookId}/

## Usage
Register a New User
Send a POST request to /api/register/ with the following payload:

```bash
{
    "username": "yourusername",
    "password": "yourpassword",
    "email": "youremail@example.com"
}
```

## Login
Send a POST request to /api/login/ with the following payload:

```bash
{
    "username": "yourusername",
    "password": "yourpassword"
}
```

The response will include an authentication token that should be used for authenticated requests.

## Managing Books
After logging in, use the provided token to perform CRUD operations on books. 
For example, to list all books, send a GET request to /api/books/ with the token in the Authorization header:

```bash
GET /api/books/
Authorization: Token your-auth-token
```

To add a new book, send a POST request to api/books/ with the with the token in the Authorization header and the following payload:

```bash
{
    "titolo": "title",
    "autore": "author",
    "isbn": "isbn",
    "pubyear": "2024"
}
```

Use the same payload with the following PUT request /api/books/{id}/ to edit a specific book.

```bash
PUT /api/books/{id}/
Authorization: Token your-auth-token
```

## Managing Favorites
- To add a book to favorites, send a POST request to /api/favorites/{bookId}/ with the token in the Authorization header.
- To delete a book to favorites, send a DELETE request to /api/favorites/{bookId}/ with the token in the Authorization header.
- To retrive user favorites, send a GET request to /api/favorites/ with the token in the Authorization header.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes.
