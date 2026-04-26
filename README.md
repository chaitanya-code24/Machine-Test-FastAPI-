# FastAPI Machine Test

A production-ready FastAPI backend for managing categories and products using PostgreSQL, SQLAlchemy ORM, and Python-based configuration.

This project implements the machine test requirements:

- RESTful APIs using FastAPI
- PostgreSQL database integration
- SQLAlchemy ORM models
- Python-based configuration with `.env`
- Category CRUD APIs
- Product CRUD APIs
- One-to-many relationship between Category and Product
- Server-side pagination using `page` and `limit`
- Product detail API with associated category details
- Swagger UI for API testing
- Automated pytest coverage for all required endpoints

## Tech Stack

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic
- Uvicorn
- Pytest

## Project Structure

```text
app/
- main.py
- config.py
- database.py
- models.py
- schemas.py
- crud.py
- routes/
  - __init__.py
  - category.py
  - product.py
tests/
- test_api_endpoints.py
requirements.txt
requirements-dev.txt
.env.example
README.md
```

## API Endpoints

### Category APIs

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/categories?page=1&limit=10` | Fetch categories with server-side pagination |
| POST | `/api/categories` | Create a new category |
| GET | `/api/categories/{id}` | Fetch category by ID |
| PUT | `/api/categories/{id}` | Update category by ID |
| DELETE | `/api/categories/{id}` | Delete category by ID |

### Product APIs

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/products?page=1&limit=10` | Fetch products with server-side pagination |
| POST | `/api/products` | Create a new product |
| GET | `/api/products/{id}` | Fetch product by ID with category details |
| PUT | `/api/products/{id}` | Update product by ID |
| DELETE | `/api/products/{id}` | Delete product by ID |

### Health Check

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Check application status |

## Database Schema

### `categories` Table

| Column | Type | Constraint |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `name` | String(100) | Required, unique, indexed |
| `description` | Text | Optional |
| `created_at` | DateTime | Auto-generated |
| `updated_at` | DateTime | Auto-generated and updated on changes |

### `products` Table

| Column | Type | Constraint |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `name` | String(150) | Required, indexed |
| `description` | Text | Optional |
| `price` | Numeric(10, 2) | Required |
| `quantity` | Integer | Required, defaults to `0` |
| `category_id` | Integer | Foreign key to `categories.id` |
| `created_at` | DateTime | Auto-generated |
| `updated_at` | DateTime | Auto-generated and updated on changes |

### Relationship

```text
One Category -> Many Products
Each Product -> One Category
```

The `products.category_id` column references `categories.id`.

When a category is deleted, its related products are also deleted because the model uses cascade delete behavior.

## Setup Instructions

### 1. Clone or Open the Project

Open the project folder in terminal:

```powershell
cd "C:\Users\chait\OneDrive\Desktop\Machine Test (FastAPI)"
```

### 2. Create Virtual Environment

```powershell
python -m venv .venv
```

### 3. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Create PostgreSQL Database

Open PostgreSQL SQL Shell or pgAdmin and run:

```sql
CREATE DATABASE fastapi_machine_test;
```

### 6. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+psycopg2://postgres:root@localhost:5432/fastapi_machine_test
APP_NAME=FastAPI Machine Test
APP_DEBUG=True
```

Update the username and password according to your local PostgreSQL setup.

## Run the Application

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

## Sample Requests

### Create Category

```json
{
  "name": "Electronics",
  "description": "Electronic items and gadgets"
}
```

### Create Product

```json
{
  "name": "Mobile Phone",
  "description": "Android smartphone",
  "price": "15000.00",
  "quantity": 10,
  "category_id": 1
}
```

### Product Detail Response

`GET /api/products/{id}` returns product details with category details:

```json
{
  "name": "Mobile Phone",
  "description": "Android smartphone",
  "price": "15000.00",
  "quantity": 10,
  "category_id": 1,
  "id": 1,
  "created_at": "2026-04-26T16:53:18.201435+05:30",
  "updated_at": "2026-04-26T16:53:18.201435+05:30",
  "category": {
    "name": "Electronics",
    "description": "Electronic items and gadgets",
    "id": 1,
    "created_at": "2026-04-26T16:53:18.179577+05:30",
    "updated_at": "2026-04-26T16:53:18.179577+05:30"
  }
}
```

## Run Automated Tests

Install development dependencies:

```powershell
pip install -r requirements-dev.txt
```

Run tests:

```powershell
python -m pytest -q
```

Expected result:

```text
1 passed
```

The test suite verifies:

- Health endpoint
- Category CRUD
- Product CRUD
- Server-side pagination
- Product detail response with nested category
- Delete behavior and `404` response after deletion

## Notes

- Do not commit the real `.env` file.
- Use `.env.example` as the shared configuration template.
- Database tables are created automatically when the application starts.
- Validation errors are handled by FastAPI and Pydantic.
- Missing records return `404 Not Found`.
- Duplicate category names return `409 Conflict`.
