from sqlalchemy.orm.exc import NoResultFound


#########need to be refactor################
def get_or_create(model, session, **kwargs):
    try:
        # basically check the obj from the db, this syntax might be wrong

        object = session.query(model).filter_by(**kwargs).first()
        if object is not None:
            return object
        object = model()
        return object

    except Exception as e:  # or whatever error/exception it is on SQLA
        object = model()
        print("exception is happened")
        # do it here if you want to save the obj to the db
        return object
