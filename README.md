# FastAPI JWT RBAC Example

A simple FastAPI application demonstrating JWT authentication and Role-Based Access Control (RBAC).

## Features

- JWT token-based authentication
- Role-Based Access Control (RBAC) with three roles: Admin, User, and Moderator
- Protected endpoints with role-specific access
- Password hashing with bcrypt
- OAuth2 password flow

## Project Structure

```
.
├── main.py           # FastAPI application with endpoints
├── models.py         # Pydantic models for User, Token, and Roles
├── auth.py           # Authentication logic and JWT handling
├── dependencies.py   # Dependency injection for authentication and RBAC
└── requirements.txt  # Python dependencies
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Default Users

The application comes with three pre-configured users:

| Username  | Password | Role      |
|-----------|----------|-----------|
| admin     | secret   | admin     |
| moderator | secret   | moderator |
| user      | secret   | user      |

## Usage Examples

### 1. Get JWT Token

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Access Protected Endpoint

```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Access Role-Specific Endpoint

Admin-only endpoint:
```bash
curl -X GET "http://localhost:8000/admin-only" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

## Endpoints

| Method | Endpoint      | Auth Required | Roles Allowed           | Description                    |
|--------|---------------|---------------|-------------------------|--------------------------------|
| GET    | /             | No            | Public                  | Public welcome message         |
| POST   | /token        | No            | Public                  | Login and get JWT token        |
| GET    | /users/me     | Yes           | All authenticated       | Get current user info          |
| GET    | /user-only    | Yes           | All authenticated       | User-accessible content        |
| GET    | /moderate     | Yes           | Admin, Moderator        | Moderation endpoint            |
| GET    | /users/all    | Yes           | Admin only              | Get all users (admin only)     |
| GET    | /admin-only   | Yes           | Admin only              | Admin-only content             |

## RBAC Implementation

The RBAC system uses the `RoleChecker` dependency:

```python
@app.get("/admin-only")
async def admin_only_endpoint(
    current_user: User = Depends(RoleChecker([Role.ADMIN]))
):
    return {"message": "Admin-only content"}
```

This ensures only users with the ADMIN role can access the endpoint.

## Security Notes

- The `SECRET_KEY` in `auth.py` should be changed in production
- Currently uses an in-memory fake database - replace with a real database
- All passwords are hashed using bcrypt
- Tokens expire after 30 minutes (configurable)

## Technologies Used

- FastAPI - Modern web framework
- Python-JOSE - JWT token handling
- Passlib - Password hashing
- Pydantic - Data validation
- Uvicorn - ASGI server

## License

MIT
