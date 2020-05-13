from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
#########need to be refactor################
from ICECREAM.http import HTTPError


def get_nested_data(model, data, db_session):
    if not data:
        return []
    _list_object = []
    if hasattr(model(), "id"):
        for _object in data:
            actor_obj = get_object_or_404(model, db_session, model.id == _object.get("id"))
            _list_object.append(actor_obj)
        return _list_object
    HTTPError(400, "Model should has id")


def get_or_create(model, session, **kwargs):
    try:
        # basically check the obj from the db, this syntax might be wrong

        model_object = session.query(model).filter_by(**kwargs).first()
        if model_object is not None:
            return model_object
        model_object = model(**kwargs)
        return model_object

    except Exception as e:  # or whatever error/exception it is on SQLA
        model_object = model()
        print("exception is happened")
        # do it here if you want to save the obj to the db
        return model_object


def get_object(model, session, *args, **kwargs):
    """
    Use get() to return an object, return None if object does not exist.
    """
    try:
        model_object = session.query(model).filter(*args, **kwargs).first()
        return model_object
    except Exception as e:
        return None


def get_object_or_404(model, session, *args, **kwargs):
    """
    Use get() to return an object, or raise a Http404 exception if the object
    does not exist.
    """
    model_object = session.query(model).filter(*args, **kwargs).first()
    if model_object:
        return model_object
    raise HTTPError(404, body=model().__class__.__name__ + "_Not_Found")


def set_objects_limit(list_object: [], limit: int, session: Session):
    """
        Use set_objects_limit to clear last element and hold objects limit count
    """
    offset = (limit - 1) * -1
    if offset == 0:
        [session.delete(_object) for _object in list_object[:]]
    [session.delete(_object) for _object in list_object[:offset]]


def is_object_exist_409(model, session, *args, **kwargs):
    """
        Use is_object_exist_409 if object exist raise Http409.
    """
    model_object = session.query(model).filter(*args, **kwargs).first()
    if model_object:
        raise HTTPError(409, body=model().__class__.__name__ + "_Already_exist")
    return None
