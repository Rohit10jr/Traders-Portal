# Traders-Portal

A Django REST API project for managing companies and user watchlists.  
This project was created for a Fingrad job task and is designed to demonstrate Django REST practices, token authentication (JWT), async tasks with Celery+Redis, custom logging, and auto-generated API documentation using Swagger (drf-yasg), and Gcp.

---

## Features

- **User Registration & JWT Authentication**  
  - Register new users via API
  - Secure authentication using JWT (SimpleJWT)
  - Endpoints for login, refresh tokens

- **Company & Watchlist Management**  
  - CRUD for companies
  - Users can manage their own watchlists
  - Filtering and searching companies

- **API Documentation**  
  - Swagger UI (`/swagger/`)
  - ReDoc UI (`/redoc/`)
  - Uses drf-yasg for OpenAPI/Swagger generation

- **Asynchronous Tasks**  
  - Celery tasks for loading companies from CSV
  - Celery worker and beat integration
  - Redis as message broker

- **Logging**  
  - Custom logging configuration for both project and critical API events
  - Logs written to `logs/project.log` and `logs/critical_api.log`

- **Rate Limiting**  
  - Configurable anonymous and user rate throttling (REST framework)

---

## Tech Stack

- **Backend:** Django 5.2.x, Django REST Framework
- **Auth:** SimpleJWT (JWT tokens)
- **Async Tasks:** Celery 5.x, Redis
- **API Docs:** drf-yasg (Swagger/OpenAPI)
- **Database:** SQLite (default, can be changed)
- **Other:** Python 3.11+

---

## Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/Rohit10jr/Traders-Portal.git
   cd Traders-Portal
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Database migrations**
   ```sh
   python manage.py migrate
   ```

4. **Run the development server**
   ```sh
   python manage.py runserver
   ```

5. **Start Redis server**  
   (Ensure Redis is installed locally)
   ```sh
   redis-server
   ```

6. **Start Celery worker and beat**
   ```sh
   celery -A traders_portal worker --loglevel=info --pool=solo
   celery -A traders_portal beat --loglevel=info
   ```

---

## Developer Workflow & Troubleshooting

Here are common commands for development, testing, coverage, and troubleshooting:

### Server & Port Troubleshooting

```sh
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process by PID (replace 3812 with your PID)
taskkill /PID 3812 /F
```

### Testing & Coverage

```sh
# Run Django tests
python311 manage.py test

# Run tests with coverage tracking
coverage run manage.py test

# Generate coverage report in terminal
coverage report

# Generate HTML coverage report
coverage html

# Open coverage report (Windows only)
start htmlcov/index.html
```

### Data Loading

```sh
# Load companies using Django shell and a script
python311 manage.py shell < load_companies.py
```

### Celery & Redis

```sh
# Start Redis server (Windows)
redis-server.exe

# Start Celery worker
celery -A traders_portal worker --loglevel=info --pool=solo

# Start Celery beat scheduler
celery -A traders_portal beat --loglevel=info
```

### Migration & Database Cleanup

```sh
# Remove migration Python files except __init__.py
find core/migrations -path "*__init__.py" -prune -o -name "*.py" -exec rm -f {} \;

# Remove compiled Python files in migrations
find core/migrations -name "*.pyc" -delete

# Remove database file
rm db.sqlite3
```

---

## API Endpoints

- **User Registration:** `/api/register/`
- **JWT Login:** `/api/login/`
- **Token Refresh:** `/api/token/refresh/`
- **Company CRUD:** `/api/companies/` (list/create), `/api/companies/<id>/` (detail/update/delete)
- **Watchlist CRUD:** `/api/watchlist/` (list/add)
- **Swagger Docs:** `/swagger/`
- **ReDoc Docs:** `/redoc/`

---

## Celery Tasks

- Example: Load companies from CSV file (`master.csv`)
  ```python
  @shared_task
  def load_all_companies_from_csv(): ...
  ```

---

## Logging

- All logs are stored in the `logs/` directory.
- Separate log files for general and critical API errors.

---

<!-- ## Thank you -->

