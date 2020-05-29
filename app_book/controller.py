from marshmallow import ValidationError

from ICECREAM.http import HTTPResponse
from ICECREAM.models.query import get_or_create
from ICECREAM.validators import validate_data
from app_book.models import Author, Quote
from app_book.schemas import AuthorSchema, quote_serializer, author_serializer, quotes_serializer


def get_authors(db_session):
    authors = db_session.query(Author).all()
    serializer = AuthorSchema(many=True)
    result = serializer.dump(authors)
    return HTTPResponse(status=200, body=result)


def new_quote(data, db_session):
    validate_data(data=data, serializer=quote_serializer)
    author = data['author']

    first = author['first']
    last = author['last']

    content = data['content']

    author = get_or_create(Author, db_session, Author.first == first, Author.last == last)

    if author is None:
        author = Author(first, last)
        db_session.add(author)
    quote = Quote(content, author)

    db_session.add(quote)
    db_session.commit()

    result = quote_serializer.dump(db_session.query(Quote).get(quote.id))
    return HTTPResponse(status=200, body=result)


def get_author(pk, db_session):
    author = db_session.query(Author).get(pk)
    author_result = author_serializer.dump(author)
    quotes_result = quotes_serializer.dump(author.quotes.all())
    author_result.update({"quotes": quotes_result})
    return HTTPResponse(status=200, body=author_result)


def get_quotes(db_session):
    quotes = db_session.query(Quote).all()
    result = quotes_serializer.dump(quotes)
    return HTTPResponse(status=200, body=result)


def get_quote(pk, db_session):
    quote = db_session.query(Quote).get(pk)
    result = quote_serializer.dump(quote)
    return HTTPResponse(status=200, body=result)


def delete_quote(pk, db_session):
    pass
