###  **ICE CREAM Instructions**

**To run bottle builtin server with commands:**
    
    python manage.py runserver 
    python manage.py runserver 127.0.0.1:8000

**To bind icecream to gunicorn:**
    
    gunicorn --workers=2  'wsgi:wsgi_app()'
    

**to create new app:**

    python manage.py startapp app_name
    {app must inherit from BaseApp like samples}
    then register app in settings.py

**Migration Commands:**

**To make migration:**

    alembic revision --autogenerate -m "Message"

**To migrate:**

    alembic upgrade head


 
