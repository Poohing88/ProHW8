import psycopg2
from pprint import pprint


info_db = 'dbname=test_db user=student password=qwerty host=localhost'
students = [{
    'name': 'Vasiliy Petrov',
    'gpa': 4.7,
    'birth': '2011-05-27 15:47:58.138995-07'
},
    {
        'name': 'Ivan Egorov'
    }]

course = 'Python'


def create_table():
    with psycopg2.connect(info_db) as conn:
        with conn.cursor() as curs:
            curs.execute(
                "CREATE TABLE Students (id SERIAL PRIMARY KEY,"
                "name CHAR(64),"
                "gpa numeric(10,2),"
                "birth timestamp with time zone);"
            )
            curs.execute(
                "CREATE TABLE Course (id SERIAL PRIMARY KEY,"
                "name CHAR(64));"
            )
            curs.execute(
                "CREATE TABLE students_course ("
                "id SERIAL PRIMARY KEY,"
                "Student_id INTEGER REFERENCES Students(id),"
                "Course_id INTEGER REFERENCES Course(id));"
            )


def add_student(student_info):
    with psycopg2.connect(info_db) as conn:
        with conn.cursor() as curs:
            curs.execute("insert into students (name, gpa, birth) values (%s, %s, %s);",
                         (student_info.get('name'), student_info.get('gpa'), student_info.get('birth'), ))


def add_course(course):
    with psycopg2.connect(info_db) as conn:
        with conn.cursor() as curs:
            curs.execute("insert into Course (name) values (%s);", (course,))


def get_student(id_student):
    with psycopg2.connect(info_db) as conn:
        with conn.cursor() as curs:
            curs.execute("select name, gpa, birth from Students where id=%s;", (id_student, ))
            info = curs.fetchall()
            return info


def add_students(course_id, list_student_info):
    with psycopg2.connect(info_db) as conn:
        with conn.cursor() as curs:
            for student_info in list_student_info:
                curs.execute("insert into students (name, gpa, birth) values (%s, %s, %s);",
                             (student_info.get('name'), student_info.get('gpa'), student_info.get('birth'),))
                curs.execute("select * from Students;")
                id_student = curs.fetchall()
                curs.execute("insert into students_course (Student_id, Course_id) values ('%s', '%s');",
                             (id_student[-1][0], course_id))


def get_students(course_id):
    info_course_students = []
    with psycopg2.connect(info_db) as conn:
        with conn.cursor() as curs:
            curs.execute("select student_id from students_course  where course_id='%s';", (course_id, ))
            students_id = curs.fetchall()
            for i in students_id:
                info = get_student(i)
                info_course_students.append(info[0])
            return info_course_students


if __name__ == '__main__':
    create_table()
    add_course(course)
    add_students(1, students)
    pprint(get_students(1))