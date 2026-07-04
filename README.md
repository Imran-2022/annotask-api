README for Task Management Backend
==================================

## Setup Instructions

### 1. Create virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Run migrations
```
python manage.py migrate
```

### 4. Create superuser (optional, for admin panel)
```
python manage.py createsuperuser
```

### 5. Run development server
```
python manage.py runserver
```

The server will run on http://localhost:8000

## API Endpoints

### Authentication
- POST `/api/auth/auth/register/` - Register new user
- POST `/api/auth/auth/login/` - Login user
- POST `/api/auth/auth/logout/` - Logout user
- GET `/api/auth/auth/me/` - Get current user info

### Tasks
- GET `/api/tasks/` - Get all user's tasks
- POST `/api/tasks/` - Create new task
- PUT `/api/tasks/{id}/` - Update task
- DELETE `/api/tasks/{id}/` - Delete task
- GET `/api/tasks/by_date/?date=YYYY-MM-DD` - Get tasks for specific date
- GET `/api/tasks/by_date_range/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` - Get tasks for date range
- POST `/api/tasks/{id}/change_status/` - Change task status
- POST `/api/tasks/reorder/` - Reorder tasks

## Admin Panel
Access admin panel at `/admin/` with superuser credentials
