#!/bin/sh

# Path to the flag file
INIT_FLAG="/app/.initialized"

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Check if the container has been initialized
if [ ! -f "$INIT_FLAG" ]; then
  # Create superuser if not exists
  echo "from django.contrib.auth.models import User; \
  User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or \
  User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" \
  | python manage.py shell

  # Mark the container as initialized
  touch $INIT_FLAG
  echo "Initialization completed."
else
  echo "Container already initialized. Skipping initialization."
fi

# Start the server
exec python manage.py runserver 0.0.0.0:8000 #gunicorn core.wsgi:application --bind 0.0.0.0:8000
