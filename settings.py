# icecream framework settings
import os
import rootpath
from dotenv import load_dotenv, find_dotenv

rootpath.append()
load_dotenv(find_dotenv())
project_root = rootpath.detect()
media_path = project_root + os.getenv('media_files')
# you can using instead of os.getenv  media_files = /statics/media/
DEBUG: bool = True

searches_index = [
    # ('users', 'search_vector', ['user_name']),
]

apps = [
    'app_book.urls.BookApp',
    'app_foo.urls.FOOApp',
    'app_user.urls.USERApp'
]
rules_file = os.getenv("rules_file")
roles_file = os.getenv("roles_file")
default_address = {
    'host': os.getenv('host') or '127.0.0.1',
    'port': os.getenv('port') or 8888,
}
redis_cache = {
    'redis_host': os.getenv('redis_host') or '127.0.0.1',
    'redis_port': (os.getenv('redis_port')) or 6379,
    'redis_pass': os.getenv('redis_pass') or None,
}
database = {
    'db_user': os.getenv('db_user'),
    'db_pass': os.getenv('db_pass'),
    'db_host': os.getenv('db_host'),
    'db_port': os.getenv('db_port'),
    'db_name': os.getenv('db_name'),
    'db_type': os.getenv('db_type') or "sqlite"
}
project_secret = os.getenv('project_secret')
jwt_ttl = os.getenv('jwt_ttl') or 64000
sentry_dsn = os.getenv('sentry_dsn')
