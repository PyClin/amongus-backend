# amongus-backend

To run this application:
```
docker-compose up -d
```

Create and activate your virtualenv 
Go to the root of the project (where manage.py is present)
```
pip install -r requirements.txt
```

```
python manage.py migrate
```

```
python manage.py runserver 8000
```

```
celery -A amongus worker --loglevel=INFO -P solo -c 10

```

Get the .env file from Bhavesh and place it in the same directory as the manage.py file
