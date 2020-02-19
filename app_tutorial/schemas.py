"ICECREAM"
from marshmallow import Schema, fields


class StudentSchema(Schema):
    class Meta:
        fields = ("id", "classes")


class ClassSchema(Schema):
    students = fields.Nested(StudentSchema(many=True))

    class Meta:
        fields = ('id', 'students')


student_serializer = StudentSchema()
class_serializer = ClassSchema()
students_serializer = StudentSchema(many=True, only=('id',))
