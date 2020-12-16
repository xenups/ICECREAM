import os
import csv
import bottle
from csv import reader
from rbac.acl import Registry
from sqlalchemy.orm import Session
from ICECREAM.http import HTTPError
from app_user.models import User
from rbac.proxy import RegistryProxy
from rbac.context import IdentityContext

from settings import rules_file, roles_file

project_root = os.path.abspath(os.curdir)
roles_path = project_root + "/" + roles_file
rules_path = project_root + "/" + rules_file


class ACLHandler(object):
    def __init__(self, Resource):
        self.__acl = RegistryProxy(Registry())
        self.__set_roles()
        self.__acl.add_resource(Resource)
        self.__resource = Resource
        self.__set_rules()

    @staticmethod
    def _read_file(file_name: str) -> list:
        with open(file_name, newline='') as f:
            _reader = csv.reader(f)
            data = list(_reader)
            return data

    def add_resource(self, Resource):
        self.__acl.add_resource(Resource)
        self.__resource = Resource

    def __set_roles(self, ):
        roles = self._read_file(roles_path)[0]
        for role in roles:
            self.__acl.add_role(str(role))

    def __set_rules(self):
        rules = self._read_file(rules_path)
        _resource_name = str(self.__resource().__class__.__name__).lower().strip()
        for rule in rules:
            if str(rule[2]).lower() == _resource_name:
                self.__acl.allow(role=str(rule[0]).strip(), operation=str(rule[1]).strip(), resource=self.__resource)

    def get_identity(self, current_user):
        identity = IdentityContext(self.__acl, lambda: current_user.get_roles())
        return identity


def get_rules_json(user):
    roles = user.get_roles()
    rules = []
    with open(rules_path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            # rule = {"role": row[0], "rule": row[1], "object": row[2]}
            if row[0] in roles:
                rules.append(row[1])
    return rules


def get_roles_json():
    rules = []
    with open(roles_path, 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            rule = {"role": row}
            rules.append(rule)
    return rules


def get_roles_list():
    roles = ([a['role'] for a in get_roles_json()])
    return roles[0]


def get_user_identity(db_session, model):
    user = bottle.request.get_user()
    current_user = db_session.query(User).get(user['id'])
    aclh = ACLHandler(Resource=model)
    aclh.add_resource(model)
    identity = aclh.get_identity(current_user)
    return identity


def validate_permission(rule: str, db_session: Session, model):
    identity = get_user_identity(db_session, model)
    if identity.check_permission(rule, model):
        return True
    raise HTTPError(status=403, body="Access_denied")


def validate_permissions(rules: [], db_session: Session, model):
    identity = get_user_identity(db_session, model)
    for rule in rules:
        if not identity.check_permission(rule, model):
            raise HTTPError(status=403, body="Access_denied")
    return True
