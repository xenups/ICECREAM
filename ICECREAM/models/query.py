from sqlalchemy.orm.exc import NoResultFound


#########need to be refactor################
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
