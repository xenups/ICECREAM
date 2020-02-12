from manage import main
import sys


def wsgi_app(*args, **kwargs):
    sys.argv = ['--gunicorn']
    for k in kwargs:
        sys.argv.append("--" + k)
        sys.argv.append(kwargs[k])
    return main()
