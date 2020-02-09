from marshmallow import Schema, fields


class AuthorSchema(Schema):
    formatted_name = fields.Method("format_name")

    @staticmethod
    def format_name(author):
        return "{}, {}".format(author.last, author.first)

    class Meta:
        fields = ('id', 'first', 'last', "formatted_name")


class QuoteSchema(Schema):
    author = fields.Nested(AuthorSchema)

    class Meta:
        fields = ("id", "content", "posted_at", 'author')


class SchemaError(Exception):
    """Error that is raised when a marshalling or umarshalling error occurs.
    Stores the dictionary of validation errors that occurred.
    """

    def __init__(self, message, errors):
        Exception.__init__(self, message)
        self.errors = errors


author_serializer = AuthorSchema()
quote_serializer = QuoteSchema()
quotes_serializer = QuoteSchema(many=True, only=('id', 'content'))
