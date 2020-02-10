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


author_serializer = AuthorSchema()
quote_serializer = QuoteSchema()
quotes_serializer = QuoteSchema(many=True, only=('id', 'content'))
