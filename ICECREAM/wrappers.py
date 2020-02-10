from bottle import request

from ICECREAM.db_initializer import get_db_session


def pass_data(func):
    def wrapper(*args, **kwargs):
        if request.json is not None:
            kwargs['data'] = request.json
        elif request.forms is not None:
            my_data = {}
            data_list = request.forms.dict
            for key in data_list.keys():
                my_data[key] = data_list[key][0]
            if request.files is not None and request.files.dict is not None:
                my_data['files'] = request.files.dict.get('files')

            kwargs['data'] = my_data

        rtn = func(*args, **kwargs)
        return rtn

    return wrapper


def db_handler(func):
    def wrapper(*args, **kwargs):
        kwargs['db_session'] = get_db_session()
        rtn = func(*args, **kwargs)
        db_session = kwargs['db_session']
        try:
            db_session.commit()
        except Exception as e:
            print(e)
        return rtn

    return wrapper
