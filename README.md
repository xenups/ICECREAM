# **ICE CREAM Instructions** 

<img src="https://raw.githubusercontent.com/xenups/bottle_restfool/master/ICECREAM/statics/images/ice.png" width="50" height="50">
ICE-CREAM framework for Bottle designed for simplify building restful api. It is structured such that any part of the core functionality can be customised to suit the needs of your project. every controller has access to each to reduce complex business logic.

**To run bottle builtin server with commands:**
    
    python manage.py runserver 
    python manage.py runserver 127.0.0.1:8000

**To bind icecream to gunicorn:**
    
    gunicorn --workers=2  'manage:wsgi_app()'
    

**to create new app:**

    python manage.py startapp app_name
    then register app in settings.py

#### **Migration Commands:**
**To initialize migration:**

    alembic init alembic
after intializing alembic config the env.py in alembic folder  like env.py file exist into the  project

**To make migration:**

    alembic revision --autogenerate -m "Message"

**To migrate:**

    alembic upgrade head


 
