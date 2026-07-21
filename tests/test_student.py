from student import Student


def test_student_creation():
    student = Student(101, "Hari", 22)

    assert student.student_id == 101
    assert student.name == "Hari"
    assert student.age == 22


def test_student_display():
    student = Student(101, "Hari", 22)

    assert student.display() == "ID: 101, Name: Hari, Age: 22"
