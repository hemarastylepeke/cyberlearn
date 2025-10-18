release: python manage.py makemigrations && python manage.py migrate
web: gunicorn cyberlearn.wsgi --log-file -