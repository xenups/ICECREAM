from bottle import request
from ICECREAM.db_initializer import DBConnector, get_db_session


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
        except:
            print('ex')
            # logger.exception(LogMsg.COMMIT_ERROR, exc_info=True)
            # raise Http_error(500, Message.COMMIT_FAILED)
        return rtn

    return wrapper


def model_to_dict(obj):
    object_dict = dict((name, getattr(obj, name)) for name in dir(obj) if
                       (not name.startswith('_')) and not name.startswith(
                           'mongo') and not name.startswith(
                           'create_query')) if not isinstance(obj,
                                                              dict) else obj

    if "metadata" in object_dict:
        del object_dict['metadata']
    return object_dict


def jsonify(func):
    def wrapper(*args, **kwargs):
        rtn = func(*args, **kwargs)
        result = None
        if isinstance(rtn, list):
            result = []
            for item in rtn:
                if isinstance(item, str):
                    result.append(item)
                else:
                    result.append(model_to_dict(item))
            result = {"result": result}
        else:
            result = model_to_dict(rtn)
        return result

    return wrapper
