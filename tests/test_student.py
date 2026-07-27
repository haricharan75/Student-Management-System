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


# NEW TESTS: Additional edge cases and boundary conditions

def test_grade_boundary_a_lower():
    """Test grade boundary at 80 for A"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 80)
    
    assert student.get_grade() == "A"


def test_grade_boundary_a_upper():
    """Test grade boundary at 89.9 for A"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 89.9)
    
    assert student.get_grade() == "A"


def test_grade_boundary_b_lower():
    """Test grade boundary at 70 for B"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 70)
    
    assert student.get_grade() == "B"


def test_grade_boundary_b_upper():
    """Test grade boundary at 79.9 for B"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 79.9)
    
    assert student.get_grade() == "B"


def test_grade_boundary_c_lower():
    """Test grade boundary at 60 for C"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 60)
    
    assert student.get_grade() == "C"


def test_grade_boundary_c_upper():
    """Test grade boundary at 69.9 for C"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 69.9)
    
    assert student.get_grade() == "C"


def test_grade_boundary_d_lower():
    """Test grade boundary at 50 for D"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 50)
    
    assert student.get_grade() == "D"


def test_grade_boundary_d_upper():
    """Test grade boundary at 59.9 for D"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 59.9)
    
    assert student.get_grade() == "D"


def test_grade_boundary_f_lower():
    """Test grade boundary just below passing (49.9)"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 49.9)
    
    assert student.get_grade() == "F"


def test_average_decimal_values():
    """Test average calculation with decimal mark values"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 85.5)
    student.add_mark("Java", 90.5)
    
    # (85.5 + 90.5) / 2 = 88.0
    assert student.calculate_average() == 88.0


def test_add_marks_decimal_boundary_zero():
    """Test adding decimal marks at zero boundary"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 0.0)
    
    assert student.marks["Python"] == 0.0


def test_add_marks_decimal_boundary_hundred():
    """Test adding decimal marks at hundred boundary"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 100.0)
    
    assert student.marks["Python"] == 100.0


def test_add_marks_very_small_negative():
    """Test that very small negative value is rejected"""
    student = Student(101, "Hari", 21)
    
    with pytest.raises(ValueError):
        student.add_mark("Python", -0.1)


def test_add_marks_just_above_hundred():
    """Test that value just above 100 is rejected"""
    student = Student(101, "Hari", 21)
    
    with pytest.raises(ValueError):
        student.add_mark("Python", 100.1)


def test_update_name_with_single_character():
    """Test updating name with single character"""
    student = Student(101, "Hari", 21)
    
    student.update_name("A")
    
    assert student.name == "A"


def test_update_name_with_special_characters():
    """Test updating name with special characters"""
    student = Student(101, "Hari", 21)
    
    student.update_name("Hari-Khan")
    
    assert student.name == "Hari-Khan"


def test_update_name_with_numbers():
    """Test updating name with numbers"""
    student = Student(101, "Hari", 21)
    
    student.update_name("Hari123")
    
    assert student.name == "Hari123"


def test_update_age_near_boundary_lower():
    """Test updating age to just above lower boundary"""
    student = Student(101, "Hari", 21)
    
    student.update_age(6)
    
    assert student.age == 6


def test_update_age_near_boundary_upper():
    """Test updating age to just below upper boundary"""
    student = Student(101, "Hari", 21)
    
    student.update_age(99)
    
    assert student.age == 99


def test_enroll_multiple_courses_many():
    """Test enrolling in many courses"""
    student = Student(101, "Hari", 21)
    
    courses = ["Python", "Java", "C++", "JavaScript", "Ruby", "Go", "Rust"]
    for course in courses:
        student.enroll_course(course)
    
    assert len(student.courses) == 7
    for course in courses:
        assert course in student.courses


def test_remove_course_after_many_enrollments():
    """Test removing course after enrolling in many"""
    student = Student(101, "Hari", 21)
    
    courses = ["Python", "Java", "C++"]
    for course in courses:
        student.enroll_course(course)
    
    student.remove_course("Java")
    
    assert len(student.courses) == 2
    assert "Java" not in student.courses
    assert "Python" in student.courses
    assert "C++" in student.courses


def test_add_marks_many_subjects():
    """Test adding marks for many subjects"""
    student = Student(101, "Hari", 21)
    
    subjects = ["Python", "Java", "C++", "Math", "Physics", "Chemistry"]
    marks_list = [90, 85, 88, 92, 87, 89]
    
    for subject, marks in zip(subjects, marks_list):
        student.add_mark(subject, marks)
    
    assert len(student.marks) == 6
    assert student.marks["Python"] == 90
    average = sum(marks_list) / len(marks_list)
    assert student.calculate_average() == average


def test_remove_mark_from_many():
    """Test removing a mark after adding many"""
    student = Student(101, "Hari", 21)
    
    student.add_mark("Python", 90)
    student.add_mark("Java", 85)
    student.add_mark("C++", 88)
    
    student.remove_mark("Java")
    
    assert len(student.marks) == 2
    assert "Java" not in student.marks
    assert "Python" in student.marks
    assert "C++" in student.marks


def test_display_with_no_courses_no_marks():
    """Test display when student has no courses or marks"""
    student = Student(101, "NoData", 21)
    
    data = student.display()
    
    assert data["Courses"] == []
    assert data["Marks"] == {}
    assert data["Average"] == 0
    assert data["Grade"] == "F"
    assert data["Passed"] is False


def test_display_with_multiple_courses_multiple_marks():
    """Test display with both courses and marks"""
    student = Student(101, "FullData", 21)
    
    student.enroll_course("Python")
    student.enroll_course("Java")
    student.add_mark("Python", 90)
    student.add_mark("Java", 85)
    
    data = student.display()
    
    assert len(data["Courses"]) == 2
    assert len(data["Marks"]) == 2
    assert data["Average"] == 87.5
    assert data["Grade"] == "A"
    assert data["Passed"] is True


def test_string_method_format():
    """Test that __str__ returns expected format"""
    student = Student(101, "Hari", 21)
    student.add_mark("Python", 75)
    
    text = str(student)
    
    assert "Student(" in text
    assert "id=101" in text
    assert "name=Hari" in text
    assert "age=21" in text
    assert "grade=B" in text


def test_passed_with_zero_average():
    """Test that student with zero average fails"""
    student = Student(101, "Hari", 21)
    
    assert student.is_passed() is False
    assert student.calculate_average() == 0


def test_passed_with_exact_fifty():
    """Test that student with exactly 50 passes"""
    student = Student(101, "Hari", 21)
    student.add_mark("Python", 50)
    
    assert student.is_passed() is True
    assert student.calculate_average() >= 50


def test_passed_with_decimal_below_fifty():
    """Test that student with 49.99 fails"""
    student = Student(101, "Hari", 21)
    student.add_mark("Python", 49.99)
    
    assert student.is_passed() is False
