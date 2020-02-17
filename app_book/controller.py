from marshmallow import ValidationError

from ICECREAM.models.query import get_or_create
from app_book.models import Author, Quote
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from bottle import request, HTTPError, HTTPResponse
from app_book.schemas import AuthorSchema, quote_serializer, author_serializer, quotes_serializer


def get_authors(db_session):
    try:
        authors = db_session.query(Author).all()
        serializer = AuthorSchema(many=True)
        result = serializer.dump(authors)
        return result
    except Exception as e:
        raise HTTPError(status=400, body={'error': e.args.__str__()})


def new_quote(db_session, data):
    try:
        quote_serializer.load(data)
        author = data['author']
        first = author['first']
        last = author['last']
        content = data['content']
        author = get_or_create(Author, db_session, first=first, last=last)
        if author is None:
            author = Author(first, last)
            db_session.add(author)
        quote = Quote(content, author)
        db_session.add(quote)
        db_session.commit()
        result = quote_serializer.dump(db_session.query(Quote).get(quote.id))
        return result
    except ValidationError as err:
        return err.messages


def get_author(pk, db_session):
    try:
        author = db_session.query(Author).get(pk)
        if author is not None:
            author_result = author_serializer.dump(author)
            quotes_result = quotes_serializer.dump(author.quotes.all())
            author_result.update({"quotes": quotes_result})
            return author_result
        else:
            raise HTTPError(status=404, body='Not found {0}'.format(pk))
    except NoResultFound as e:
        raise HTTPError(status=400, body={'error': e.args.__str__()})


def get_quotes(db_session):
    quotes = db_session.query(Quote).all()
    result = quotes_serializer.dump(quotes)
    return result


def get_quote(pk, db_session):
    try:
        quote = db_session.query(Quote).get(pk)
    except IntegrityError:
        raise HTTPError(status=404, body='Not found {0}'.format(pk))
    result = quote_serializer.dump(quote)
    if quote is not None:
        return result


def delete_quote(pk, db_session):
    pass
