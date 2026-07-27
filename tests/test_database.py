import pytest

from database import StudentDatabase


@pytest.fixture
def database():
    return StudentDatabase()


def test_add_student(database):
    student = database.add_student(101, "Hari", 21)

    assert student.student_id == 101
    assert database.count_students() == 1


def test_duplicate_student(database):
    database.add_student(101, "Hari", 21)

    with pytest.raises(ValueError):
        database.add_student(101, "Charan", 22)


def test_find_student_by_id(database):
    database.add_student(101, "Hari", 21)

    student = database.find_student_by_id(101)

    assert student.name == "Hari"


def test_find_student_by_invalid_id(database):
    assert database.find_student_by_id(999) is None


def test_find_student_by_name(database):
    database.add_student(101, "Hari", 21)

    students = database.find_student_by_name("Hari")

    assert len(students) == 1
    assert students[0].student_id == 101


def test_find_student_by_name_case_insensitive():
    """Test that name search is case-insensitive"""
    database = StudentDatabase()
    database.add_student(101, "Hari", 21)

    students = database.find_student_by_name("hari")

    assert len(students) == 1
    assert students[0].name == "Hari"


def test_find_multiple_students_same_name():
    """Test finding multiple students with the same name"""
    database = StudentDatabase()
    database.add_student(101, "Hari", 21)
    database.add_student(102, "Hari", 22)

    students = database.find_student_by_name("Hari")

    assert len(students) == 2


def test_find_student_by_name_not_found(database):
    """Test that search returns empty list when name not found"""
    result = database.find_student_by_name("NonExistent")

    assert result == []


def test_update_student_name(database):
    database.add_student(101, "Hari", 21)

    result = database.update_student_name(101, "Charan")

    assert result is True
    assert database.find_student_by_id(101).name == "Charan"


def test_update_non_existent_student_name(database):
    """Test updating name for non-existent student"""
    result = database.update_student_name(999, "Charan")

    assert result is False


def test_update_student_age(database):
    database.add_student(101, "Hari", 21)

    result = database.update_student_age(101, 25)

    assert result is True
    assert database.find_student_by_id(101).age == 25


def test_update_non_existent_student_age(database):
    """Test updating age for non-existent student"""
    result = database.update_student_age(999, 25)

    assert result is False


def test_delete_student(database):
    database.add_student(101, "Hari", 21)

    result = database.delete_student(101)

    assert result is True
    assert database.count_students() == 0


def test_delete_invalid_student(database):
    assert database.delete_student(999) is False


def test_count_students(database):
    database.add_student(101, "Hari", 21)
    database.add_student(102, "Charan", 22)

    assert database.count_students() == 2


def test_count_students_empty(database):
    """Test count on empty database"""
    assert database.count_students() == 0


def test_clear_database(database):
    database.add_student(101, "Hari", 21)
    database.add_student(102, "Charan", 22)

    database.clear_database()

    assert database.count_students() == 0


def test_add_marks(database):
    database.add_student(101, "Hari", 21)

    result = database.add_marks(101, "Python", 95)

    assert result is True
    assert database.find_student_by_id(101).marks["Python"] == 95


def test_add_marks_non_existent_student(database):
    """Test adding marks for non-existent student"""
    result = database.add_marks(999, "Python", 95)

    assert result is False


def test_add_marks_multiple_subjects(database):
    """Test adding marks for multiple subjects"""
    database.add_student(101, "Hari", 21)

    database.add_marks(101, "Python", 90)
    database.add_marks(101, "Java", 85)

    student = database.find_student_by_id(101)

    assert len(student.marks) == 2


def test_enroll_student(database):
    database.add_student(101, "Hari", 21)

    result = database.enroll_student(101, "Python")

    assert result is True
    assert "Python" in database.find_student_by_id(101).courses


def test_enroll_non_existent_student(database):
    """Test enrolling non-existent student in course"""
    result = database.enroll_student(999, "Python")

    assert result is False


def test_enroll_multiple_courses(database):
    """Test enrolling in multiple courses"""
    database.add_student(101, "Hari", 21)

    database.enroll_student(101, "Python")
    database.enroll_student(101, "Java")

    student = database.find_student_by_id(101)

    assert len(student.courses) == 2


def test_get_all_students(database):
    """Test getting all students"""
    database.add_student(101, "Hari", 21)
    database.add_student(102, "Charan", 22)

    students = database.get_all_students()

    assert len(students) == 2


def test_get_all_students_empty(database):
    """Test getting students from empty database"""
    students = database.get_all_students()

    assert students == []


def test_get_passed_students(database):
    student = database.add_student(101, "Hari", 21)

    student.add_mark("Python", 80)

    passed = database.get_passed_students()

    assert len(passed) == 1


def test_get_passed_students_empty(database):
    """Test getting passed students when none exist"""
    passed = database.get_passed_students()

    assert passed == []


def test_get_passed_and_failed_students(database):
    """Test with mix of passed and failed students"""
    student1 = database.add_student(101, "Hari", 21)
    student2 = database.add_student(102, "Charan", 22)

    student1.add_mark("Python", 80)
    student2.add_mark("Python", 30)

    passed = database.get_passed_students()
    failed = database.get_failed_students()

    assert len(passed) == 1
    assert len(failed) == 1
    assert passed[0].name == "Hari"
    assert failed[0].name == "Charan"


def test_get_failed_students(database):
    student = database.add_student(101, "Hari", 21)

    student.add_mark("Python", 20)

    failed = database.get_failed_students()

    assert len(failed) == 1


def test_get_failed_students_empty(database):
    """Test getting failed students when none exist"""
    failed = database.get_failed_students()

    assert failed == []


def test_sort_by_name(database):
    database.add_student(102, "Zara", 20)
    database.add_student(101, "Hari", 21)

    database.sort_by_name()

    students = database.get_all_students()

    assert students[0].name == "Hari"


def test_sort_by_name_case_insensitive():
    """Test sorting by name with mixed case"""
    database = StudentDatabase()
    database.add_student(102, "zara", 20)
    database.add_student(101, "Hari", 21)
    database.add_student(103, "CHARAN", 22)

    database.sort_by_name()

    students = database.get_all_students()

    assert students[0].name == "CHARAN"
    assert students[1].name == "Hari"
    assert students[2].name == "zara"


def test_sort_by_name_multiple_same_name():
    """Test sorting when multiple students have same name"""
    database = StudentDatabase()
    database.add_student(102, "Hari", 20)
    database.add_student(101, "Hari", 21)

    database.sort_by_name()

    students = database.get_all_students()

    assert students[0].name == "Hari"
    assert students[1].name == "Hari"


def test_sort_by_average(database):
    first = database.add_student(101, "Hari", 21)
    second = database.add_student(102, "Charan", 22)

    first.add_mark("Python", 70)
    second.add_mark("Python", 95)

    database.sort_by_average()

    students = database.get_all_students()

    assert students[0].name == "Charan"


def test_sort_by_average_tied_averages():
    """Test sorting when students have same average"""
    database = StudentDatabase()
    first = database.add_student(101, "Hari", 21)
    second = database.add_student(102, "Charan", 22)

    first.add_mark("Python", 85)
    second.add_mark("Python", 85)

    database.sort_by_average()

    students = database.get_all_students()

    assert len(students) == 2
    assert students[0].calculate_average() == students[1].calculate_average()


def test_sort_by_average_no_marks():
    """Test sorting includes students with no marks"""
    database = StudentDatabase()
    first = database.add_student(101, "Hari", 21)
    second = database.add_student(102, "Charan", 22)

    first.add_mark("Python", 95)

    database.sort_by_average()

    students = database.get_all_students()

    assert students[0].name == "Hari"
    assert students[1].name == "Charan"


def test_get_top_student(database):
    first = database.add_student(101, "Hari", 21)
    second = database.add_student(102, "Charan", 22)

    first.add_mark("Python", 75)
    second.add_mark("Python", 95)

    top = database.get_top_student()

    assert top.name == "Charan"


def test_empty_top_student(database):
    assert database.get_top_student() is None


def test_get_top_student_no_marks():
    """Test getting top student when some have no marks"""
    database = StudentDatabase()
    first = database.add_student(101, "Hari", 21)
    second = database.add_student(102, "Charan", 22)

    first.add_mark("Python", 75)

    top = database.get_top_student()

    assert top.name == "Hari"


def test_get_top_student_tied():
    """Test getting top student when multiple have highest average"""
    database = StudentDatabase()
    first = database.add_student(101, "Hari", 21)
    second = database.add_student(102, "Charan", 22)

    first.add_mark("Python", 95)
    second.add_mark("Python", 95)

    top = database.get_top_student()

    assert top.calculate_average() == 95


def test_database_operations_sequence():
    """Test complex sequence of database operations"""
    database = StudentDatabase()

    database.add_student(101, "Hari", 21)
    database.add_student(102, "Charan", 22)

    database.add_marks(101, "Python", 85)
    database.add_marks(102, "Python", 75)

    database.enroll_student(101, "Python")
    database.enroll_student(102, "Java")

    database.update_student_name(101, "Hari Updated")

    student = database.find_student_by_id(101)

    assert student.name == "Hari Updated"
    assert "Python" in student.courses
    assert student.marks["Python"] == 85
