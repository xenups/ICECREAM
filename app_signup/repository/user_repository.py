from app_user.models import User, Person


def user_by_cell_number(cell_no, db_session):
    user = db_session.query(User).filter(User.username == cell_no).first()
    if not user:
        person = db_session.query(Person).filter(Person.cell_no == cell_no).first()
        if person is not None:
            user = db_session.query(User).filter(User.person_id == person.id).first()

    return user
