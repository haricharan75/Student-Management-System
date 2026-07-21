from database import Database


def test_add_student():
    db = Database()

    student = db.add_student(101, "Hari", 22)

    assert student.student_id == 101
    assert student.name == "Hari"
    assert student.age == 22
    assert len(db.get_all_students()) == 1


def test_get_students():
    db = Database()

    db.add_student(101, "Hari", 22)
    db.add_student(102, "Ravi", 23)

    students = db.get_all_students()

    assert len(students) == 2
    assert students[0].name == "Hari"
    assert students[1].name == "Ravi"
