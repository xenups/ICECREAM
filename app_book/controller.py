from bottle import request, HTTPError
from marshmallow import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app_book.models import Author, Quote
from app_book.schemas import AuthorSchema, quote_serializer
from manager.db_initializer import Base


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
        return result
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
        return result
    except ValidationError as err:
        print(err.messages)
        return err.messages

# @app.route("/api/v1/authors/<int:pk>")
# def get_author(pk):
#     try:
#         author = Author.query.get(pk)
#     except IntegrityError:
#         return jsonify({"message": "Author could not be found."}), 400
#     author_result = author_serializer.dump(author)
#     quotes_result = quotes_serializer.dump(author.quotes.all())
#     return jsonify({'author': author_result.data, 'quotes': quotes_result.data})
#
# @app.route('/api/v1/quotes', methods=['GET'])
# def get_quotes():
#     quotes = Quote.query.all()
#     result = quotes_serializer.dump(quotes)
#     return jsonify({"quotes": result.data})
#
# @app.route("/api/v1/quotes/<int:pk>")
# def get_quote(pk):
#     try:
#         quote = Quote.query.get(pk)
#     except IntegrityError:
#         return jsonify({"message": "Quote could not be found."}), 400
#     result = quote_serializer.dump(quote)
#     return jsonify({"quote": result.data})
#
# @app.route("/api/v1/quotes/new", methods=["POST"])
# def new_quote():
#     first, last = request.json['author'].split(" ")
#     content = request.json['quote']
#     author = Author.query.filter_by(first=first, last=last).first()
#     if author is None:
#         # Create a new author
#         author = Author(first, last)
#         db.session.add(author)
#     # Create new quote
#     quote = Quote(content, author)
#     db.session.add(quote)
#     db.session.commit()
#     result = quote_serializer.dump(Quote.query.get(quote.id))
#     return jsonify({"message": "Created new quote.",
#                     "quote": result.data})
