import pytest

from student import Student


def test_student_creation():
    student = Student(101, "Hari", 21)

    assert student.student_id == 101
    assert student.name == "Hari"
    assert student.age == 21
    assert student.courses == []
    assert student.marks == {}


def test_update_name():
    student = Student(101, "Hari", 21)

    student.update_name("Charan")

    assert student.name == "Charan"


def test_update_name_invalid():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_name("")


def test_update_name_whitespace_only():
    """Test that whitespace-only names are rejected"""
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_name("   ")


def test_update_age():
    student = Student(101, "Hari", 21)

    student.update_age(25)

    assert student.age == 25


def test_update_age_invalid():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_age(2)


def test_update_age_boundary_lower():
    """Test age at lower boundary (5)"""
    student = Student(101, "Hari", 21)

    student.update_age(5)

    assert student.age == 5


def test_update_age_boundary_lower_invalid():
    """Test age below lower boundary (4)"""
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_age(4)


def test_update_age_boundary_upper():
    """Test age at upper boundary (100)"""
    student = Student(101, "Hari", 21)

    student.update_age(100)

    assert student.age == 100


def test_update_age_boundary_upper_invalid():
    """Test age above upper boundary (101)"""
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_age(101)


def test_enroll_course():
    student = Student(101, "Hari", 21)

    student.enroll_course("Python")

    assert "Python" in student.courses


def test_enroll_duplicate_course():
    """Test that duplicate courses are not added"""
    student = Student(101, "Hari", 21)

    student.enroll_course("Python")
    student.enroll_course("Python")

    assert student.courses.count("Python") == 1


def test_enroll_multiple_courses():
    """Test enrolling in multiple different courses"""
    student = Student(101, "Hari", 21)

    student.enroll_course("Python")
    student.enroll_course("Java")
    student.enroll_course("C++")

    assert len(student.courses) == 3
    assert "Python" in student.courses
    assert "Java" in student.courses
    assert "C++" in student.courses


def test_remove_course():
    student = Student(101, "Hari", 21)

    student.enroll_course("Python")
    student.remove_course("Python")

    assert "Python" not in student.courses


def test_remove_non_existent_course():
    """Test removing a course that was never enrolled"""
    student = Student(101, "Hari", 21)

    student.remove_course("Python")

    assert "Python" not in student.courses


def test_add_marks():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 95)

    assert student.marks["Python"] == 95


def test_add_marks_boundary_lower():
    """Test adding marks at lower boundary (0)"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 0)

    assert student.marks["Python"] == 0


def test_add_marks_boundary_upper():
    """Test adding marks at upper boundary (100)"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 100)

    assert student.marks["Python"] == 100


def test_invalid_marks_negative():
    """Test that negative marks are rejected"""
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.add_mark("Python", -1)


def test_invalid_marks_over_100():
    """Test that marks over 100 are rejected"""
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.add_mark("Python", 120)


def test_add_marks_multiple_subjects():
    """Test adding marks for multiple subjects"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 90)
    student.add_mark("Java", 85)
    student.add_mark("C++", 88)

    assert len(student.marks) == 3
    assert student.marks["Python"] == 90


def test_add_marks_overwrite():
    """Test that re-adding marks for same subject overwrites previous value"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 90)
    student.add_mark("Python", 95)

    assert student.marks["Python"] == 95
    assert len(student.marks) == 1


def test_remove_marks():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 90)
    student.remove_mark("Python")

    assert "Python" not in student.marks


def test_remove_non_existent_mark():
    """Test removing marks for a subject that has no marks"""
    student = Student(101, "Hari", 21)

    student.remove_mark("Python")

    assert "Python" not in student.marks


def test_average():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 80)
    student.add_mark("Java", 90)

    assert student.calculate_average() == 85


def test_average_no_marks():
    """Test that average is 0 when no marks added"""
    student = Student(101, "Hari", 21)

    assert student.calculate_average() == 0


def test_average_single_mark():
    """Test average calculation with single mark"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 75)

    assert student.calculate_average() == 75


def test_average_multiple_marks():
    """Test average with multiple marks"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 80)
    student.add_mark("Java", 90)
    student.add_mark("C++", 85)

    assert student.calculate_average() == 85


def test_grade_a_plus():
    """Test grade A+ (>= 90)"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 90)
    student.add_mark("Java", 90)

    assert student.get_grade() == "A+"


def test_grade_a():
    """Test grade A (80-89)"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 80)
    student.add_mark("Java", 85)

    assert student.get_grade() == "A"


def test_grade_b():
    """Test grade B (70-79)"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 75)

    assert student.get_grade() == "B"


def test_grade_c():
    """Test grade C (60-69)"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 65)

    assert student.get_grade() == "C"


def test_grade_d():
    """Test grade D (50-59)"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 55)

    assert student.get_grade() == "D"


def test_grade_f():
    """Test grade F (< 50)"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 45)

    assert student.get_grade() == "F"


def test_grade_boundary_a_plus():
    """Test grade boundary at 90 for A+"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 89.9)

    assert student.get_grade() == "A"


def test_grade_no_marks():
    """Test grade with no marks (average 0)"""
    student = Student(101, "Hari", 21)

    assert student.get_grade() == "F"


def test_passed():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 80)

    assert student.is_passed() is True


def test_failed():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 20)

    assert student.is_passed() is False


def test_passed_boundary():
    """Test passing at exact boundary (50)"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 50)

    assert student.is_passed() is True


def test_failed_boundary():
    """Test failing just below boundary (49.9)"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 49.9)

    assert student.is_passed() is False


def test_passed_no_marks():
    """Test that student with no marks fails"""
    student = Student(101, "Hari", 21)

    assert student.is_passed() is False


def test_display():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 90)

    data = student.display()

    assert data["Student ID"] == 101
    assert data["Name"] == "Hari"
    assert data["Grade"] == "A+"


def test_display_contains_all_keys():
    """Test that display contains all expected keys"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 80)
    student.enroll_course("Python")

    data = student.display()

    assert "Student ID" in data
    assert "Name" in data
    assert "Age" in data
    assert "Courses" in data
    assert "Marks" in data
    assert "Average" in data
    assert "Grade" in data
    assert "Passed" in data


def test_display_average_rounded():
    """Test that average in display is rounded to 2 decimal places"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 85)
    student.add_mark("Java", 86)
    student.add_mark("C++", 87)

    data = student.display()

    assert data["Average"] == 86.0


def test_string_method():
    student = Student(101, "Hari", 21)

    text = str(student)

    assert "Hari" in text
    assert "101" in text


def test_string_method_contains_grade():
    """Test that __str__ includes the grade"""
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 95)

    text = str(student)

    assert "A+" in text
