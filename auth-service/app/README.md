
Auth Service
------------
Endpoints:
- POST /register
- POST /login (form-data username/password)
- GET /me (requires Bearer token)
- GET /admin-only (requires admin role)
Run with: uvicorn main:app --reload
