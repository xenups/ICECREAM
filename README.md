# **ICE CREAM Instructions** 

<img src="https://raw.githubusercontent.com/xenups/bottle_restfool/master/ICECREAM/statics/images/ice.png" width="50" height="50">
ICE-CREAM framework for Bottle designed for simplify building restful api. It is structured such that any part of the core functionality can be customised to suit the needs of your project. every controller has access to each to reduce complex business logic.

**To run bottle builtin server with commands:**
    
    python manage.py runserver 
    python manage.py runserver 127.0.0.1:8000

**To bind icecream to gunicorn:**
    
    gunicorn --workers=2  'manage:wsgi_app()'

 
Copy and rename .env_example to .env and change the variable as project needs.
Or you can add the parameters manually into .env file
To generate an .env file these values are required:

| Variable Name                     | Description                    |
|-----------------------------------|--------------------------------|
| host                     | icecream host |
| port                     | icecream port |
| db_name                  | your database db_name|
| db_user                  | your database username|
| db_pass                  | your database password|
| db_host                  | your database host|
| db_port                  | your database port|
| project_secret            | needs for jwt authentication: experimental feature|
| jwt_ttl            | jwt time to live|
| sentry_dsn            | sentry address (logging tool), it can be|
| media_files            | static media folder|

already ice-cream is working with postgres

Now you need to check that your website is running. Open your browser (Firefox, Chrome, Safari, Internet Explorer or whatever you use) and enter this address:

browser
http://127.0.0.1:8000/api

Congratulations! You've just created your first website and run it using a web server!
![icecream](https://user-images.githubusercontent.com/18069620/92040998-a654c880-ed8c-11ea-87c8-340306fbbba8.png)


**to create super user:**

    python manage.py createsuperuser
    
**to create new app:**

    python manage.py startapp app_name
    then register app in settings.py

#### **Migration Commands:**
**To initialize migration:** 

    alembic init alembic
    python manage.py makealembic
    

**To make migration:**

    alembic revision --autogenerate -m "Message"

**To migrate:**

    alembic upgrade head

#### **Authentication**:
Unlike some more typical uses of JWTs, this module only generates authentication tokens that will verify the user who is requesting one of your ICECREAM protected API resources. The actual request parameters themselves are not included in the JWT claims which means they are not signed and may be tampered with. To implement user authentication in your application, you need to override the AuthBackend() class in authentication.py in users folder.
to obtaining token and refresh token it need to get it from route which allocated in JWTProviderPlugin

To using authentication needs to using . Add the following URL pattern:
```
    core.route('/users', 'GET', get_users, apply=[jwt_auth_required])
```


#### **File serving:**
**To serving files first  need to create a static folder in root of project:**

     Create a folder like :
    /statics/media/
**After that register the address in the .env:**

    media_files = /statics/media/
    
### **RBAC in ICECREAM**

#### **Role-based User Access Control**

in ICECREAM an access control model is abstracted into two csv file. So switching or upgrading the authorization mechanism for a project is just as simple as modifying a csv files. You can customize your own access control model by combining the available models.
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
### **Caching in ICECREAM**
Caching refers to storing the server response in the client itself, so that a client need not make a server request for the same resource again and again.ICECREAM using Redis to do caching , Redis has more sophisticated mechanisms as it has been described as a "data structure store", thus making it more powerful and flexible. Redis also has a larger advantage because you can store data in any form. In the ICECREAM When the function runs, it checks if the view key is in the cache. If the key exists, then the app retrieves the data from the cache and returns it. If not, ICECREAM queries the database and then stashes the result in the cache with the view key. The first time this function is run, ICECREAM will query the database and render the template, and then will also make a network call to Redis to store the data in the cache. Each subsequent call to the function will completely bypass the database and business logic and will query the Redis cache.
To cache view functions you will use the cache_for() decorator.

```
    @cache_for(24 * 60, cache_key_func='full_path')
    def get_user(pk, db_session):
        user = get_object_or_404(User, db_session, User.id == pk)
        result = user_serializer.dump(user)
        return HTTPResponse(status=200, body=result)
```
or you can pass the decorator in router
```
    core.route('/users', 'GET', get_users,apply=[cache_for(24 * 60, cache_key_func='full_path')])
```
    
### **Full text search in ICECREAM**

Full text search is a more advanced way to search a database. Full text search quickly finds all instances of a term (word) in a table without having to scan rows and without having to know which column a term is stored in. Full text search works by using text indexes.
to provide full text search ICECREAM integrated with SQLAlchemy-Searchable, its provides full text search capabilities for SQLAlchemy models. Currently it only supports PostgreSQL.
to start full text search first we should follow these steps:

as the first step we should define the model in app : 

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
and in the last step it can be sweet as an icecream
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
When making changes to your database schema you have to make sure the associated search triggers and trigger functions get updated also. ICECREAM offers a helper command called index_search for this. to perform this ,its calling SQLAlchemy-Searchable  sync_trigger after every 
```
alembic upgrade head
```
to perform search trigger , should run this command  :
```
python manage.py index_search
```