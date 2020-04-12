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
apps = [
    'app_book.urls.BookApp',
    'app_foo.urls.FOOApp',
    'app_tutorial.urls.ClassApp',
    'app_signup.urls.SignUpApp',
    'app_user.urls.USERApp'
]
default_address = {
    'host': os.getenv('host'),
    'port': os.getenv('port'),
}

database = {
    'db_user': os.getenv('db_user'),
    'db_pass': os.getenv('db_pass'),
    'db_host': os.getenv('db_host'),
    'db_port': os.getenv('db_port'),
    'db_name': os.getenv('db_name')
}
project_secret = os.getenv('project_secret')
jwt_ttl = os.getenv('jwt_ttl')
sentry_dsn = os.getenv('sentry_dsn')

sms = {
    'sms_token_url': os.getenv('sms_token_url'),
    'sms_security_key': os.getenv('sms_security_key'),
    'sms_api_key': os.getenv('sms_api_key'),
    'sms_timeout': os.getenv('sms_timeout'),
    'sms_send_url': os.getenv('sms_send_url'),
    'sms_line_no': os.getenv('sms_line_no'),
}
