from bottle import HTTPError
from marshmallow import ValidationError

from app_tutorial.models import Student, Class, People
from app_tutorial.schemas import StudentSchema, student_serializer, class_serializer, students_serializer, PeopleSchema
from ICECREAM.models.query import get_or_create, get_nested_data


def get_students(db_session):
    try:
        students = db_session.query(Student).all()
        serializer = StudentSchema(many=True)
        result = serializer.dump(students)
        return result
    except Exception as e:
        raise HTTPError(status=400, body={'error': e.args.__str__()})


def new_student(db_session, data):
    try:
        student_serializer.load(data)
        student = Student()
        student.id = data['id']
        student_instance = get_or_create(Student, db_session, Student.id == student.id)
        if student_instance.id is None:
            db_session.add(student)
            db_session.commit()
            result = db_session.query(Student).get(student.id)
            return result
        else:
            return 'person exist'
        # result = room_serializer.dump(db_session.query(Room).get(room.id))

    except ValidationError as err:
        return err.messages


def new_class(db_session, data):
    try:
        class_serializer.load(data)
    except ValidationError as err:
        return err.messages

    class_room = Class()
    class_room.id = data['id']
    class_room_instance = get_or_create(Class, db_session, Class.id == class_room.id)
    if class_room_instance.id is None:
        db_session.add(class_room)

    students = data['students']
    for student in students:
        student_instance = get_or_create(Student, db_session, Student.id == student['id'])
        if student_instance.id is None:
            student_instance.id = student['id']
            class_room_instance.students.append(student_instance)
            db_session.add(student_instance)
    # or instead all of above codes you can use this line to collect nested data by id's
    # class_room_instance.students = get_nested_data(Student, data.get("students"), db_session)
    db_session.add(class_room_instance)
    db_session.commit()
    serialized_class = class_serializer.dump(class_room)
    return serialized_class


def get_peoples(db_session):
    try:
        peoples = db_session.query(People).all()
        serializer = PeopleSchema()
        return peoples
    except HTTPError as e:
        return e.body
