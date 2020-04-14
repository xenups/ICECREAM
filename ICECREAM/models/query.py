from sqlalchemy.orm.exc import NoResultFound

#########need to be refactor################
from ICECREAM.http import HTTPError
from app_user.models import Person, User


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
        return None


def get(model, session, **kwargs):
    try:
        model_object = session.query(model).filter_by(**kwargs).first()
        return model_object
    except Exception as e:
        model_object = model()
        return model_object


def get_object_or_404(model, session, *args, **kwargs):
    """
    Use get() to return an object, or raise a Http404 exception if the object
    does not exist.
    """
    model_object = session.query(model).filter(*args, **kwargs).first()
    if model_object:
        return model_object
    raise HTTPError(404, body="Not Found!")


def is_object_exist(model, session, *args, **kwargs):
    model_object = session.query(model).filter(*args, **kwargs).first()
    if model_object:
        raise HTTPError(409, body="Already exist")
    return None
