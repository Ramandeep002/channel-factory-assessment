## GeoRouteAPI

GeoRouteAPI is a Django-based project that provides geocoding, reverse geocoding, and distance calculation services using the Google Maps API. This project leverages the Django Rest Framework (DRF) for creating and managing API endpoints.

### Table of Contents

- [Installation](#installation)
- [Setting Up PostgreSQL](#setting-up-postgresql)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Examples](#examples)
- [Contributing](#contributing)


### Installation

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
1. **Run via Docker (Optional):**
    ```bash
    docker compose build
    docker compose up -d
    ```
   
3. **Create and activate a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Set up environment variables:**
    Create a `.env` file in the `core` directory and add your Google Maps API key:
    ```env
    GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'
    ```

6. **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

7. **Create a superuser (optional):**
    ```bash
    python manage.py createsuperuser
    ```

8. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

### Setting Up PostgreSQL

### Step 1: Install PostgreSQL

1. **Install PostgreSQL on your system:**
    - **Ubuntu:**
      ```bash
      sudo apt update
      sudo apt install postgresql postgresql-contrib
      ```
    - **MacOS:**
      ```bash
      brew install postgresql
      ```
    - **Windows:** Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/).

2. **Start the PostgreSQL service:**
    - **Ubuntu:**
      ```bash
      sudo service postgresql start
      ```
    - **MacOS:**
      ```bash
      brew services start postgresql
      ```
    - **Windows:** Start the PostgreSQL service from the Services app.

### Step 2: Create a PostgreSQL Database and User

1. **Log into the PostgreSQL prompt:**
    ```bash
    sudo -u postgres psql
    ```
    - **Windows:** Use `psql` from the PostgreSQL installation directory.

2. **Create a new database:**
    ```sql
    CREATE DATABASE georouteapi;
    ```

3. **Create a new database user:**
    ```sql
    CREATE USER your_db_user WITH PASSWORD 'your_db_password';
    ```

4. **Grant the user access to the database:**
    ```sql
    GRANT ALL PRIVILEGES ON DATABASE georouteapi TO your_db_user;
    ```

5. **Exit the PostgreSQL prompt:**
    ```sql
    \q
    ```

### Step 3: Install PostgreSQL Client for Django

1. **Install the PostgreSQL client for Django:**
    ```bash
    pip install psycopg2-binary
    ```

### Step 4: Configure Django to Use PostgreSQL

1. **Update the `DATABASES` setting in your `settings.py` file:**
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'georouteapi',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

### Step 5: Apply Migrations

1. **Run the migrations to create the necessary database tables:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Step 6: Verify the Setup

1. **Create a superuser to access the Django admin interface:**
    ```bash
    python manage.py createsuperuser
    ```

2. **Run the Django development server:**
    ```bash
    python manage.py runserver
    ```

3. **Access the Django admin interface at** `http://127.0.0.1:8000/admin/` **and log in with the superuser credentials you created. Verify that you can see the tables in the admin interface.**

With these steps, your Django project should now be set up to use PostgreSQL as the database.

### Project Structure

```
core/
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── geodistance/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .env
├── manage.py
├── requirements.txt
└── README.md
```

### API Endpoints

1. **Geocode:**
    - **Endpoint:** `/api/geocode/`
    - **Method:** `GET`
    - **Parameters:** `address` (string)
    - **Description:** Returns the geocoded address with formatted address, latitude, and longitude.

2. **Reverse Geocode:**
    - **Endpoint:** `/api/reverse-geocode/`
    - **Method:** `GET`
    - **Parameters:** `lat` (float), `lng` (float)
    - **Description:** Returns the address for the given latitude and longitude.

3. **Distance Calculation:**
    - **Endpoint:** `/api/distance/`
    - **Method:** `GET`
    - **Parameters:** `lat1` (float), `lng1` (float), `lat2` (float), `lng2` (float)
    - **Description:** Returns the distance in kilometers between two geographic coordinates.

### Examples

1. **Geocode Example:**
    ```bash
    http://localhost:8000/api/geocode/?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA
    ```

2. **Reverse Geocode Example:**
    ```bash
    http://localhost:8000/api/reverse-geocode/?lat=40.714224&lng=-73.961452
    ```

3. **Distance Calculation Example:**
    ```bash
    http://localhost:8000/api/distance/?lat1=40.714224&lng1=-73.961452&lat2=34.052235&lng2=-118.243683
    ```

## Sample Env File

```bash
GOOGLE_MAPS_API_KEY =
DB_PWD =
DB_HOST =
DB_USER =
DB_DATABASE_NAME =
```