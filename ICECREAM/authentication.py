import rootpath
from bottle_jwt import JWTProviderPlugin
from settings import project_secret, jwt_ttl

rootpath.append()
#
# jwt_plugin = JWTProviderPlugin(
#     keyword='jwt',
#     auth_endpoint='/auth',
#     backend=None,
#     fields=('username', 'password'),
#     secret=project_secret,
#     ttl=int(jwt_ttl)
# )
