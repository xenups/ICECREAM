
db = {'db_user': 'fajr', 'db_pass': 'pass', 'db_host': 'host', 'db_port': 'port', 'db_name': 'name'}

DATABASE_URI = 'postgres+psycopg2://{}:{}@{}:{}/{}'.format(db['db_user'], db['db_pass'],
                                                           db['host'], db['db_port'],
                                                           db['db_name'])


# ADMINISTRATORS = ['admin', 'kk']
# SIGNUP_USER = 'signup_user'
