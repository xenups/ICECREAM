import os
import secrets
from distutils.util import strtobool
from bottle import request


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def generate_otp_code():
    return secrets.SystemRandom().randrange(999, 9999)


def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


def get_media_link(file_name):
    host = request.get_header('host')
    # for production
    return 'http://{}/api/media/{}'.format(host, file_name)


def str_to_bool(val):
    try:
        return strtobool(val)
    except Exception as e:
        return None


def detect_file_path(task_file="tasks.py", exclude_folders=None):
    if exclude_folders is None:
        exclude_folders = []
    project_root = os.getcwd()
    tasks = []
    file_path = os.path.join(project_root)
    for root, dirs, files in os.walk(file_path):
        files = [filename for filename in files if not filename[0] == '.']
        dirs[:] = [dirname for dirname in dirs if not dirname[0] == '.']
        dirs[:] = [dirname for dirname in dirs if dirname not in exclude_folders]
        for filename in files:
            if root is not project_root:
                if os.path.basename(root) == 'tasks' or filename == task_file:
                    dirname = root.split(os.path.sep)[-1]
                    if filename != '__init__.py' and filename.endswith('.py'):
                        task = os.path.join(dirname, filename).replace('/', '.').replace('.py', '')
                        tasks.append(task)
    return tuple(tasks)
