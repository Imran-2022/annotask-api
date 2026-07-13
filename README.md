Task Management + Image Annotation Backend
===========================================

## Local Setup

### Requirements
- Python 3.13+
- pip
- sqlite3 (default local database)

### 1. Create and activate virtual environment
```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows PowerShell
venv\Scripts\Activate.ps1
# Windows CMD
venv\Scripts\activate
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Optional environment variables
Create `.env` in the backend root to override defaults. Example values:
```bash
SECRET_KEY=django-insecure-change-this
DEBUG=True
DATABASE_URL=
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 4. Apply database migrations
```bash
python manage.py migrate
```

### 5. Run the development server
```bash
python manage.py runserver
```

The backend service will run on `http://localhost:8000` by default.

## Notes
- Local development uses SQLite by default.
- If `DATABASE_URL` is provided, the app uses PostgreSQL via dj-database-url.
- The backend uses Django + Django REST Framework with JWT authentication.

## Supported API Endpoints

### Authentication
- POST `/api/auth/auth/register/`
- POST `/api/auth/auth/login/`
- POST `/api/auth/auth/logout/`
- GET `/api/auth/auth/me/`

### Task Management
- GET `/api/tasks/`
- POST `/api/tasks/`
- PUT `/api/tasks/{id}/`
- DELETE `/api/tasks/{id}/`
- GET `/api/tasks/by_date/?date=YYYY-MM-DD`
- GET `/api/tasks/by_date_range/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- POST `/api/tasks/{id}/change_status/`
- POST `/api/tasks/reorder/`

### Image annotation and media
- GET `/api/images/`
- POST `/api/images/` (image upload)
- POST `/api/images/upload/` (multi-file upload)
- GET `/api/annotations/`
- POST `/api/annotations/`
- PUT `/api/annotations/{id}/`
- DELETE `/api/annotations/{id}/`

## Project alignment
This backend is aligned with the 404 project requirements: Django backend, task persistence, JWT auth, image upload, and annotation persistence via REST API.

