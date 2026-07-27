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


# NEW TESTS: Additional edge cases and boundary conditions

def test_add_marks_with_invalid_marks_zero_boundary(database):
    """Test adding valid marks at zero boundary"""
    database.add_student(101, "Hari", 21)
    
    result = database.add_marks(101, "Python", 0)
    
    assert result is True
    assert database.find_student_by_id(101).marks["Python"] == 0


def test_add_marks_with_invalid_marks_hundred_boundary(database):
    """Test adding valid marks at hundred boundary"""
    database.add_student(101, "Hari", 21)
    
    result = database.add_marks(101, "Python", 100)
    
    assert result is True
    assert database.find_student_by_id(101).marks["Python"] == 100


def test_add_marks_with_negative_marks(database):
    """Test adding negative marks raises error"""
    database.add_student(101, "Hari", 21)
    
    with pytest.raises(ValueError):
        database.add_marks(101, "Python", -1)


def test_add_marks_with_over_hundred(database):
    """Test adding marks over 100 raises error"""
    database.add_student(101, "Hari", 21)
    
    with pytest.raises(ValueError):
        database.add_marks(101, "Python", 101)


def test_update_student_name_with_invalid_empty(database):
    """Test updating name with empty string raises error"""
    database.add_student(101, "Hari", 21)
    
    with pytest.raises(ValueError):
        database.update_student_name(101, "")


def test_update_student_name_with_whitespace(database):
    """Test updating name with whitespace raises error"""
    database.add_student(101, "Hari", 21)
    
    with pytest.raises(ValueError):
        database.update_student_name(101, "   ")


def test_update_student_age_with_invalid_low(database):
    """Test updating age below boundary raises error"""
    database.add_student(101, "Hari", 21)
    
    with pytest.raises(ValueError):
        database.update_student_age(101, 4)


def test_update_student_age_with_invalid_high(database):
    """Test updating age above boundary raises error"""
    database.add_student(101, "Hari", 21)
    
    with pytest.raises(ValueError):
        database.update_student_age(101, 101)


def test_update_student_age_boundary_valid_low(database):
    """Test updating age at lower valid boundary"""
    database.add_student(101, "Hari", 21)
    
    result = database.update_student_age(101, 5)
    
    assert result is True
    assert database.find_student_by_id(101).age == 5


def test_update_student_age_boundary_valid_high(database):
    """Test updating age at upper valid boundary"""
    database.add_student(101, "Hari", 21)
    
    result = database.update_student_age(101, 100)
    
    assert result is True
    assert database.find_student_by_id(101).age == 100


def test_find_student_by_name_uppercase(database):
    """Test finding student with uppercase name input"""
    database.add_student(101, "Hari", 21)
    
    students = database.find_student_by_name("HARI")
    
    assert len(students) == 1


def test_find_student_by_name_mixed_case(database):
    """Test finding student with mixed case name input"""
    database.add_student(101, "Hari", 21)
    
    students = database.find_student_by_name("HaRi")
    
    assert len(students) == 1


def test_enroll_duplicate_course(database):
    """Test enrolling same course twice doesn't duplicate"""
    database.add_student(101, "Hari", 21)
    
    database.enroll_student(101, "Python")
    database.enroll_student(101, "Python")
    
    student = database.find_student_by_id(101)
    
    assert student.courses.count("Python") == 1


def test_add_marks_overwrite_existing(database):
    """Test adding marks for same subject overwrites previous"""
    database.add_student(101, "Hari", 21)
    
    database.add_marks(101, "Python", 80)
    database.add_marks(101, "Python", 90)
    
    student = database.find_student_by_id(101)
    
    assert student.marks["Python"] == 90
    assert len(student.marks) == 1


def test_sort_by_average_descending_order(database):
    """Test sorting by average is in descending order"""
    s1 = database.add_student(101, "First", 21)
    s2 = database.add_student(102, "Second", 22)
    s3 = database.add_student(103, "Third", 23)
    
    s1.add_mark("Test", 60)
    s2.add_mark("Test", 80)
    s3.add_mark("Test", 95)
    
    database.sort_by_average()
    
    students = database.get_all_students()
    
    assert students[0].calculate_average() == 95
    assert students[1].calculate_average() == 80
    assert students[2].calculate_average() == 60


def test_get_top_student_single_student(database):
    """Test getting top student when only one exists"""
    database.add_student(101, "Solo", 21)
    
    top = database.get_top_student()
    
    assert top.student_id == 101


def test_get_passed_students_boundary_fifty(database):
    """Test getting passed students includes boundary (50)"""
    student = database.add_student(101, "Hari", 21)
    student.add_mark("Test", 50)
    
    passed = database.get_passed_students()
    
    assert len(passed) == 1


def test_get_failed_students_below_fifty(database):
    """Test getting failed students below boundary (49.9)"""
    student = database.add_student(101, "Hari", 21)
    student.add_mark("Test", 49.9)
    
    failed = database.get_failed_students()
    
    assert len(failed) == 1


def test_clear_database_multiple_times(database):
    """Test clearing database multiple times"""
    database.add_student(101, "Hari", 21)
    database.add_student(102, "Charan", 22)
    
    database.clear_database()
    assert database.count_students() == 0
    
    database.add_student(201, "New", 25)
    database.clear_database()
    
    assert database.count_students() == 0


def test_add_student_with_invalid_age(database):
    """Test adding student with invalid age raises error"""
    with pytest.raises(ValueError):
        database.add_student(101, "Hari", 3)


def test_add_student_with_invalid_age_high(database):
    """Test adding student with age > 100 raises error"""
    with pytest.raises(ValueError):
        database.add_student(101, "Hari", 101)


def test_add_student_with_empty_name(database):
    """Test adding student with empty name raises error"""
    with pytest.raises(ValueError):
        database.add_student(101, "", 21)


def test_add_student_with_whitespace_name(database):
    """Test adding student with whitespace-only name raises error"""
    with pytest.raises(ValueError):
        database.add_student(101, "   ", 21)


def test_multiple_failed_students_all_retrieved(database):
    """Test retrieving multiple failed students"""
    s1 = database.add_student(101, "First", 21)
    s2 = database.add_student(102, "Second", 22)
    s3 = database.add_student(103, "Third", 23)
    
    s1.add_mark("Test", 30)
    s2.add_mark("Test", 40)
    s3.add_mark("Test", 60)
    
    failed = database.get_failed_students()
    
    assert len(failed) == 2


def test_multiple_passed_students_all_retrieved(database):
    """Test retrieving multiple passed students"""
    s1 = database.add_student(101, "First", 21)
    s2 = database.add_student(102, "Second", 22)
    s3 = database.add_student(103, "Third", 23)
    
    s1.add_mark("Test", 60)
    s2.add_mark("Test", 75)
    s3.add_mark("Test", 30)
    
    passed = database.get_passed_students()
    
    assert len(passed) == 2


def test_sort_by_name_empty_database(database):
    """Test sorting by name on empty database"""
    database.sort_by_name()
    
    assert database.count_students() == 0


def test_sort_by_average_empty_database(database):
    """Test sorting by average on empty database"""
    database.sort_by_average()
    
    assert database.count_students() == 0


def test_get_all_students_returns_list(database):
    """Test that get_all_students returns a list type"""
    result = database.get_all_students()
    
    assert isinstance(result, list)


def test_duplicate_student_with_different_age(database):
    """Test duplicate ID with different age still raises error"""
    database.add_student(101, "Hari", 21)
    
    with pytest.raises(ValueError):
        database.add_student(101, "Hari", 25)
