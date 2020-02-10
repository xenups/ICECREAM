from bottle import request, HTTPError, HTTPResponse
from marshmallow import ValidationError
from psycopg2._psycopg import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from app_book.models import Author, Quote
from app_book.schemas import AuthorSchema, quote_serializer, author_serializer, quotes_serializer


# connection_string = "postgresql://xenups:Qweasd1368@localhost/test"
# engine = create_engine(connection_string)
# Session = sessionmaker()
# Session.configure(bind=engine)
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
# session = Session()


def get_authors(db_session):
    try:
        authors = db_session.query(Author).all()
        serializer = AuthorSchema(many=True)
        result = serializer.dump(authors)
        return HTTPResponse(status=200, body={'result': result})
    except Exception as e:
        raise HTTPError(status=400)


def new_quote(db_session, data):
    try:
        quote_serializer.load(data)
        author = data['author']
        first = author['first']
        last = author['last']
        content = data['content']
        author = db_session.query(Author).filter_by(first=first, last=last).first()
        if author is None:
            author = Author(first, last)
            db_session.add(author)
        quote = Quote(content, author)
        db_session.add(quote)
        db_session.commit()
        result = quote_serializer.dump(db_session.query(Quote).get(quote.id))
        return HTTPResponse(status=200, body={'result': result})
    except ValidationError as err:
        print(err.messages)
        return err.messages


def get_author(pk, db_session):
    try:
        author = db_session.query(Author).get(pk)
        if author is not None:
            author_result = author_serializer.dump(author)
            quotes_result = quotes_serializer.dump(author.quotes.all())
            return HTTPResponse(status=200, body={'quotes': quotes_result, 'author': author_result})
        else:
            raise HTTPError(status=404, body='Not found {0}'.format(pk))
    except NoResultFound as e:
        print(e)


def get_quotes(db_session):
    quotes = db_session.query(Quote).all()
    result = quotes_serializer.dump(quotes)
    return HTTPResponse(status=200, body={'quote': result})


def get_quote(pk, db_session):
    try:
        quote = db_session.query(Quote).get(pk)
    except IntegrityError:
        raise HTTPError(status=404, body='Not found {0}'.format(pk))
    result = quote_serializer.dump(quote)
    if quote is not None:
        return HTTPResponse(status=200, body={'quote': result})


def delete_quote(pk, db_session):
    pass
