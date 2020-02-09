from marshmallow import ValidationError
from manager.wrappers import model_to_dict
from app_foo.models import Categores, Comments
from app_foo.schemas import CategorySchema, CommentSchema


#
# connection_string = "postgresql://xenups:Qweasd1368@localhost/test"
# engine = create_engine(connection_string)
# Session = sessionmaker()
# Session.configure(bind=engine)
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
# session = Session()

def get_categories(db_session):
    categories = db_session.query(Categores).all()
    category_dict = []
    for category in categories:
        ca = model_to_dict(category)
        category_dict.append(ca)
    return category_dict


def add_category(data, db_session):
    try:
        result = CategorySchema().load(data)
        category_instance = Categores()
        category_instance.name = data.get('name')
        category_instance.id = data.get('id')
        db_session.add(category_instance)
        db_session.commit()
        return 'finished'
    except ValidationError as err:
        print("exception")
        return err.messages


def add_comment(data, db_session):
    try:
        result = CommentSchema().dumps(data)
        comment_instance = Comments()
        comment_instance.comment = data.get('comment')
        comment_instance.id = data.get('id')
        comment_instance.category_id = data.get('category_id')
        db_session.add(comment_instance)
        # db_session.commit()

        return 'finished'
    except ValidationError as err:
        return err.messages
