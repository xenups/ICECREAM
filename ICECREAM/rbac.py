import csv
import bottle
from rbac.acl import Registry
from app_user.models import User
from rbac.proxy import RegistryProxy
from rbac.context import IdentityContext


class ACLHandler(object):
    def __init__(self, Resource, rules_path="model_rules.csv", roles_path="roles.csv"):
        self.__acl = RegistryProxy(Registry())
        self.__set_roles(roles_path)
        self.__acl.add_resource(Resource)
        self.__resource = Resource
        self.__set_rules(rules_path)

    @staticmethod
    def _read_file(file_name: str) -> list:
        with open(file_name, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            return data

    def __set_roles(self, roles_path: str):
        roles = self._read_file(roles_path)[0]
        for role in roles:
            self.__acl.add_role(str(role))

    def __set_rules(self, rules_path: str):
        rules = self._read_file(rules_path)
        _resource_name = str(self.__resource().__class__.__name__).lower().strip()
        for rule in rules:
            if str(rule[2]).lower() == _resource_name:
                self.__acl.allow(role=str(rule[0]).strip(), operation=str(rule[1]).strip(), resource=self.__resource)

    def get_identity(self, current_user):
        identity = IdentityContext(self.__acl, lambda: current_user.get_roles())
        return identity


def get_user_identity(db_session):
    user = bottle.request.get_user()
    current_user = db_session.query(User).get(user['id'])
    aclh = ACLHandler(Resource=User)
    identity = aclh.get_identity(current_user)
    return identity
