
  
## Table of Contents  
- [Introduction](#ice-cream)  
- [Quickstart](#quickstart)  
- [Running builtin server](#builtin-server)  
- [Binding to gunicorn](#binding-to-gunicorn)  
- [Env parameters](#env-parameters)  
- [Welcome Page](#welcome-page)  
- [Ice-cream commands](#ice-cream-commands)  
- [Migration commands](#migration-commands)    
- [Authentication](#authentication)    
- [Filtering](#filtering)    
- [RBAC-in-icecream](#rbac-in-icecream)
- [Caching](#caching-in-icecream)
- [Relations](#relations-in-icecream)
- [Full Text Search](#full-text-search-in-icecream)

# ICE CREAM

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Requirements](https://img.shields.io/badge/Requirements-See%20Here-orange)](https://github.com/xenups/bottle_restfool/blob/master/requirements.txt)
[![Downloads](https://pepy.tech/badge/icecreamy)](https://pepy.tech/project/icecreamy)

<img src="https://raw.githubusercontent.com/xenups/bottle_restfool/master/ICECREAM/statics/images/ice.png" width="50" height="50">
ICE-CREAM framework for Bottle designed to simplify building restful API. It is structured such that any part of the core functionality can be customized to suit the needs of your project.

## Quickstart:

   	#install it from Pypi:
    pip install icecreamy
    
    #to make icecream project, run:
    make_project.py 

	#make migration
	python manage.py  makemigrations init
	
	#to migrate
	alembic upgrade head
	
	#runing server
    python manage.py runserver 


     
and access to http://localhost:8888/api
# 

## Builtin server:
**To run bottle builtin server with commands:**
    
    python manage.py runserver 
    python manage.py runserver 127.0.0.1:8000
# 
## Binding to Gunicorn:
**To bind icecream to gunicorn:**
    
    gunicorn --workers=2  'manage:wsgi_app()'

#  
## .Env Parameters:
Copy and rename .env_example to .env and change the variable as project needs.
Or you can add the parameters manually into the .env file
To generate a .env file these values are required:

| Variable Name                     | Description                    |
|-----------------------------------|--------------------------------|
| host                     | icecream host |
| port                     | icecream port |
| db_name                  | your database db_name|
| db_type                  | sqlite or postgres|
| db_user                  | your database username|
| db_pass                  | your database password|
| db_host                  | your database host|
| db_port                  | your database port|
| project_secret            | needs for jwt authentication|
| jwt_ttl            | jwt time to live|
| sentry_dsn            | sentry address (logging tool), it can be|
| media_files            | static media folder|
# 
already ice-cream is working with Postgres
# 
## Welcome Page:
Now you need to check that your website is running. Open your browser (Firefox, Chrome, Safari, Internet Explorer or whatever you use) and enter this address:

browser
http://127.0.0.1:8000/api

Congratulations! You've just created your first website and run it using a web server!
![icecream](https://user-images.githubusercontent.com/18069620/92040998-a654c880-ed8c-11ea-87c8-340306fbbba8.png)
# 

## ice-cream commands:
**To create superuser:**

    python manage.py createsuperuser

**To create new app:**

    python manage.py startapp app_name
    then register app in settings.py

## Migration Commands:
**To make migration:**

    python manage.py  makemigrations your_message

**To migrate:**

    alembic upgrade head

## Authentication:
Unlike some more typical uses of JWTs, this module only generates authentication tokens that will verify the user who is requesting one of your ICECREAM protected API resources. The actual request parameters themselves are not included in the JWT claims which means they are not signed and may be tampered with. To implement user authentication in your application, you need to override the AuthBackend() class in authentication.py in the users folder.
to obtaining token and refresh token it needs to get it from the route allocated in JWTProviderPlugin

To using authentication needs to using . Add the following URL pattern:
```
    core.route('/users', 'GET', get_users, apply=[jwt_auth_required])
```
# 
## Filtering:
ICECREAM is using py-mongosql to apply filters query
to get a query from URL need to use this function 

	query = get_query_from_url("query")

then apply query into MongoFilter like what we did in foo_app

 	filtered_query = MongoFilter(Room, rooms_query, query).filter()
The following are some quick examples of making filtered GET requests from different types of clients. More complete documentation is in the subsequent link. In these examples, each client will filter by instances of the model Room which sorted by name.

	http://127.0.0.1:8000/rooms/filter?query={"sort":"name-",}

This link has more complete versions of these examples.
#### 	[py-mongosql](https://github.com/kolypto/py-mongosql "py-mongosql")
# 
#### **File serving:**
**To serving files first  need to create a static folder in the root of the project:**

     Create a folder like :
    /statics/media/
**After that register the address in the .env:**

    media_files = /statics/media/
#     
## RBAC in ICECREAM:

#### **Role-based User Access Control**

in ICECREAM an access control model is abstracted into two CSV files. So switching or upgrading the authorization mechanism for a project is just as simple as modifying a CSV file. You can customize your own access control model by combining the available models.
we assume we had 2 roles.

we define roles into roles.csv :

| admin                     | staff                    |
|-----------------------------------|--------------------------------|

in the next step we will define our policy in model_rules:

| role                     | operation                    |       object_you_want to modify      |
|-----------------------------------|--------------------------------|--------------------------------|

like this: 

| staff                     | create                    |       message      |
|-----------------------------------|--------------------------------|--------------------------------|

so in the last step we pass the Model to the ACLHandler
and pass the current user to check permission as bellow:

    aclh = ACLHandler(Resource=Message)
    identity = aclh.get_identity(current_user)
# 
## Caching in ICECREAM:
Caching refers to storing the server response in the client itself so that a client need not make a server request for the same resource again and again.ICECREAM using Redis to do caching, Redis has more sophisticated mechanisms as it has been described as a "data structure store", thus making it more powerful and flexible. Redis also has a larger advantage because you can store data in any form. In the ICECREAM When the function runs, it checks if the view key is in the cache. If the key exists, then the app retrieves the data from the cache and returns it. If not, ICECREAM queries the database and then stashes the result in the cache with the view key. The first time this function is run, ICECREAM will query the database and render the template, and then will also make a network call to Redis to store the data in the cache. Each subsequent call to the function will completely bypass the database and business logic and will query the Redis cache.
To cache view functions you will use the cache_for(), decorator.

```
    @cache_for(24 * 60, cache_key_func='full_path')
    def get_user(pk, db_session):
        user = get_object_or_404(User, db_session, User.id == pk)
        result = user_serializer.dump(user)
        return HTTPResponse(status=200, body=result)
```
or you can pass the decorator in the router
```
    core.route('/users', 'GET', get_users,apply=[cache_for(24 * 60, cache_key_func='full_path')])
```
#  
## Relations in ICECREAM:
ICECREAM is using SQLAlchemy ORM to see how the relationship is working
you can check this gist quickly

[SQLAlchemy basic relationship patterns](https://gist.github.com/xenups/31c81324b3d4db2e57abca868af2f0c2 "SQLAlchemy basic relationship patterns")

# 
## Full text search in ICECREAM:

Full-text search is a more advanced way to search a database. Full-text search quickly finds all instances of a term (word) in a table without having to scan rows and without having to know which column a term is stored in. Full-text search works by using text indexes.
to provide full-text search ICECREAM integrated with SQLAlchemy-Searchable, it provides full-text search capabilities for SQLAlchemy models. Currently, it only supports PostgreSQL.
to start a full-text search first we should follow these steps:

as the first step we should define the model in-app : 

```
class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
        name = Column(Unicode(255))
        content = Column(sa.UnicodeText)
        search_vector = Column(TSVectorType('name', 'content'))

```
after define models, need to add these lines to ICECREAM settings:
```
searches_index = [
    ('article', 'search_vector', ['name','content'])
]
```
and in the last step, it can be sweet as an icecream
```
article1 = Article(name=u'First article', content=u'This is the first article')
article2 = Article(name=u'Second article', content=u'This is the second article')
session.add(article1)
session.add(article2)
session.commit()

query = session.query(Article)

query = search(query, 'first')

print query.first().name
# First article
```
Optionally specify sort=True to get results in order of relevance (ts_rank_cd):

```
query = search(query, 'first', sort=True)
```
When making changes to your database schema you have to make sure the associated search triggers and trigger functions get updated also. ICECREAM offers a helper command called index_search for this. to perform this, its calling SQLAlchemy-Searchable  sync_trigger after every 
```
alembic upgrade head
```
to perform search trigger, should run this command  :
```
python manage.py index_search
```