import pytest
from unittest.mock import patch
from io import StringIO

from app import display_student, menu
from database import StudentDatabase


class TestDisplayStudent:
    """Test the display_student function"""

    def test_display_student_with_marks(self, capsys):
        """Test displaying student with marks"""
        database = StudentDatabase()
        student = database.add_student(101, "Hari", 21)
        student.add_mark("Python", 90)
        student.enroll_course("Python")

        display_student(student)

        captured = capsys.readouterr()

        assert "101" in captured.out
        assert "Hari" in captured.out
        assert "21" in captured.out
        assert "90" in captured.out
        assert "A+" in captured.out

    def test_display_student_no_marks(self, capsys):
        """Test displaying student without marks"""
        database = StudentDatabase()
        student = database.add_student(102, "Charan", 22)

        display_student(student)

        captured = capsys.readouterr()

        assert "102" in captured.out
        assert "Charan" in captured.out
        assert "F" in captured.out

    def test_display_student_no_courses(self, capsys):
        """Test displaying student with no enrolled courses"""
        database = StudentDatabase()
        student = database.add_student(103, "Test", 20)

        display_student(student)

        captured = capsys.readouterr()

        assert "None" in captured.out

    def test_display_student_multiple_courses(self, capsys):
        """Test displaying student with multiple courses"""
        database = StudentDatabase()
        student = database.add_student(104, "Multi", 20)
        student.enroll_course("Python")
        student.enroll_course("Java")

        display_student(student)

        captured = capsys.readouterr()

        assert "Python" in captured.out
        assert "Java" in captured.out

    def test_display_student_multiple_marks(self, capsys):
        """Test displaying student with multiple subject marks"""
        database = StudentDatabase()
        student = database.add_student(105, "Marks", 20)
        student.add_mark("Python", 85)
        student.add_mark("Java", 75)

        display_student(student)

        captured = capsys.readouterr()

        assert "85" in captured.out
        assert "75" in captured.out

    def test_display_student_with_zero_marks(self, capsys):
        """Test displaying student with zero marks in a subject"""
        database = StudentDatabase()
        student = database.add_student(106, "Zero", 20)
        student.add_mark("Python", 0)

        display_student(student)

        captured = capsys.readouterr()

        assert "0" in captured.out
        assert "F" in captured.out


class TestMenu:
    """Test the menu function"""

    def test_menu_displays_all_options(self, capsys):
        """Test that menu displays all 17 options"""
        menu()

        captured = capsys.readouterr()

        assert "Student Management System" in captured.out
        assert "1. Add Student" in captured.out
        assert "2. View All Students" in captured.out
        assert "3. Search Student by ID" in captured.out
        assert "4. Search Student by Name" in captured.out
        assert "5. Update Student Name" in captured.out
        assert "6. Update Student Age" in captured.out
        assert "7. Delete Student" in captured.out
        assert "8. Add Marks" in captured.out
        assert "9. Enroll Course" in captured.out
        assert "10. Show Top Student" in captured.out
        assert "11. Show Passed Students" in captured.out
        assert "12. Show Failed Students" in captured.out
        assert "13. Sort Students by Name" in captured.out
        assert "14. Sort Students by Average" in captured.out
        assert "15. Count Students" in captured.out
        assert "16. Clear Database" in captured.out
        assert "17. Exit" in captured.out


class TestMainMenuOperations:
    """Test the main function menu operations"""

    @patch("builtins.input")
    def test_add_student_operation(self, mock_input, capsys):
        """Test add student menu operation"""
        mock_input.side_effect = ["1", "101", "TestStudent", "21", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student added successfully." in captured.out

    @patch("builtins.input")
    def test_duplicate_student_error_handling(self, mock_input, capsys):
        """Test duplicate student ID error handling"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "1", "101", "Charan", "22", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    @patch("builtins.input")
    def test_view_all_students_empty(self, mock_input, capsys):
        """Test viewing all students when database is empty"""
        mock_input.side_effect = ["2", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "No students found." in captured.out

    @patch("builtins.input")
    def test_search_student_by_id_found(self, mock_input, capsys):
        """Test searching for student by ID - found"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "3", "101", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "101" in captured.out

    @patch("builtins.input")
    def test_search_student_by_id_not_found(self, mock_input, capsys):
        """Test searching for student by ID - not found"""
        mock_input.side_effect = ["3", "999", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student not found." in captured.out

    @patch("builtins.input")
    def test_search_student_by_name_found(self, mock_input, capsys):
        """Test searching for student by name - found"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "4", "Hari", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Hari" in captured.out

    @patch("builtins.input")
    def test_search_student_by_name_not_found(self, mock_input, capsys):
        """Test searching for student by name - not found"""
        mock_input.side_effect = ["4", "NonExistent", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student not found." in captured.out

    @patch("builtins.input")
    def test_update_student_name(self, mock_input, capsys):
        """Test updating student name"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "5", "101", "UpdatedName", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student updated." in captured.out

    @patch("builtins.input")
    def test_update_non_existent_student_name(self, mock_input, capsys):
        """Test updating name for non-existent student"""
        mock_input.side_effect = ["5", "999", "NewName", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student not found." in captured.out

    @patch("builtins.input")
    def test_update_student_age(self, mock_input, capsys):
        """Test updating student age"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "6", "101", "25", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Age updated." in captured.out

    @patch("builtins.input")
    def test_update_non_existent_student_age(self, mock_input, capsys):
        """Test updating age for non-existent student"""
        mock_input.side_effect = ["6", "999", "25", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student not found." in captured.out

    @patch("builtins.input")
    def test_delete_student(self, mock_input, capsys):
        """Test deleting student"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "7", "101", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student deleted." in captured.out

    @patch("builtins.input")
    def test_delete_non_existent_student(self, mock_input, capsys):
        """Test deleting non-existent student"""
        mock_input.side_effect = ["7", "999", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student not found." in captured.out

    @patch("builtins.input")
    def test_add_marks(self, mock_input, capsys):
        """Test adding marks to student"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "8", "101", "Python", "95", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Marks added." in captured.out

    @patch("builtins.input")
    def test_add_marks_non_existent_student(self, mock_input, capsys):
        """Test adding marks to non-existent student"""
        mock_input.side_effect = ["8", "999", "Python", "95", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student not found." in captured.out

    @patch("builtins.input")
    def test_enroll_course(self, mock_input, capsys):
        """Test enrolling student in course"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "9", "101", "Python", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Course enrolled." in captured.out

    @patch("builtins.input")
    def test_enroll_non_existent_student(self, mock_input, capsys):
        """Test enrolling non-existent student in course"""
        mock_input.side_effect = ["9", "999", "Python", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student not found." in captured.out

    @patch("builtins.input")
    def test_show_top_student(self, mock_input, capsys):
        """Test showing top student"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "1", "102", "Charan", "22",
            "8", "101", "Python", "75",
            "8", "102", "Python", "95",
            "10", "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Charan" in captured.out

    @patch("builtins.input")
    def test_show_top_student_empty(self, mock_input, capsys):
        """Test showing top student when no students"""
        mock_input.side_effect = ["10", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "No students available." in captured.out

    @patch("builtins.input")
    def test_show_passed_students(self, mock_input, capsys):
        """Test showing passed students"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "8", "101", "Python", "80",
            "11", "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Hari" in captured.out

    @patch("builtins.input")
    def test_show_no_passed_students(self, mock_input, capsys):
        """Test showing passed students when none exist"""
        mock_input.side_effect = ["11", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "No passed students." in captured.out

    @patch("builtins.input")
    def test_show_failed_students(self, mock_input, capsys):
        """Test showing failed students"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "8", "101", "Python", "30",
            "12", "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Hari" in captured.out

    @patch("builtins.input")
    def test_show_no_failed_students(self, mock_input, capsys):
        """Test showing failed students when none exist"""
        mock_input.side_effect = ["12", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "No failed students." in captured.out

    @patch("builtins.input")
    def test_sort_students_by_name(self, mock_input, capsys):
        """Test sorting students by name"""
        mock_input.side_effect = [
            "1", "102", "Zara", "20",
            "1", "101", "Hari", "21",
            "13", "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Students sorted by name." in captured.out

    @patch("builtins.input")
    def test_sort_students_by_average(self, mock_input, capsys):
        """Test sorting students by average"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "1", "102", "Charan", "22",
            "8", "101", "Python", "70",
            "8", "102", "Python", "95",
            "14", "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Students sorted by average." in captured.out

    @patch("builtins.input")
    def test_count_students(self, mock_input, capsys):
        """Test counting students"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "1", "102", "Charan", "22",
            "15", "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Total Students: 2" in captured.out

    @patch("builtins.input")
    def test_clear_database(self, mock_input, capsys):
        """Test clearing database"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "16", "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Database cleared." in captured.out

    @patch("builtins.input")
    def test_invalid_choice(self, mock_input, capsys):
        """Test invalid menu choice"""
        mock_input.side_effect = ["99", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Invalid choice." in captured.out

    @patch("builtins.input")
    def test_invalid_age_input_error_handling(self, mock_input, capsys):
        """Test error handling for invalid age"""
        mock_input.side_effect = ["1", "101", "Hari", "2", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    @patch("builtins.input")
    def test_invalid_marks_error_handling(self, mock_input, capsys):
        """Test error handling for invalid marks"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "8", "101", "Python", "150", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    @patch("builtins.input")
    def test_non_integer_student_id(self, mock_input, capsys):
        """Test error handling for non-integer student ID"""
        mock_input.side_effect = ["1", "abc", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    # NEW TESTS: Input Type Errors and Edge Cases

    @patch("builtins.input")
    def test_invalid_age_input_non_integer_during_update(self, mock_input, capsys):
        """Test non-integer age input during update operation (choice 6)"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "6", "101", "abc", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    @patch("builtins.input")
    def test_invalid_marks_input_non_float(self, mock_input, capsys):
        """Test non-float marks input during add marks operation (choice 8)"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "8", "101", "Python", "abc", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    @patch("builtins.input")
    def test_invalid_student_id_during_search_by_id(self, mock_input, capsys):
        """Test non-integer student ID during search by ID (choice 3)"""
        mock_input.side_effect = ["3", "abc", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    @patch("builtins.input")
    def test_invalid_student_id_during_update_name(self, mock_input, capsys):
        """Test non-integer student ID during update name (choice 5)"""
        mock_input.side_effect = ["5", "abc", "NewName", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    @patch("builtins.input")
    def test_invalid_student_id_during_update_age(self, mock_input, capsys):
        """Test non-integer student ID during update age (choice 6)"""
        mock_input.side_effect = ["6", "abc", "25", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    @patch("builtins.input")
    def test_invalid_student_id_during_delete(self, mock_input, capsys):
        """Test non-integer student ID during delete (choice 7)"""
        mock_input.side_effect = ["7", "abc", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    @patch("builtins.input")
    def test_invalid_student_id_during_add_marks(self, mock_input, capsys):
        """Test non-integer student ID during add marks (choice 8)"""
        mock_input.side_effect = ["8", "abc", "Python", "95", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    @patch("builtins.input")
    def test_invalid_student_id_during_enroll_course(self, mock_input, capsys):
        """Test non-integer student ID during enroll course (choice 9)"""
        mock_input.side_effect = ["9", "abc", "Python", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out

    @patch("builtins.input")
    def test_invalid_age_during_update_below_boundary(self, mock_input, capsys):
        """Test age below boundary (< 5) during update (choice 6)"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "6", "101", "4", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out
        assert "Invalid age" in captured.out

    @patch("builtins.input")
    def test_invalid_age_during_update_above_boundary(self, mock_input, capsys):
        """Test age above boundary (> 100) during update (choice 6)"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "6", "101", "101", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out
        assert "Invalid age" in captured.out

    @patch("builtins.input")
    def test_invalid_marks_below_boundary_during_add(self, mock_input, capsys):
        """Test marks below boundary (< 0) during add marks (choice 8)"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "8", "101", "Python", "-1", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out
        assert "between 0 and 100" in captured.out

    @patch("builtins.input")
    def test_invalid_marks_above_boundary_during_add(self, mock_input, capsys):
        """Test marks above boundary (> 100) during add marks (choice 8)"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "8", "101", "Python", "101", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out
        assert "between 0 and 100" in captured.out

    @patch("builtins.input")
    def test_invalid_name_empty_during_update(self, mock_input, capsys):
        """Test empty name during update (choice 5)"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "5", "101", "", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out
        assert "Name cannot be empty" in captured.out

    @patch("builtins.input")
    def test_invalid_name_whitespace_during_update(self, mock_input, capsys):
        """Test whitespace-only name during update (choice 5)"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "5", "101", "   ", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out
        assert "Name cannot be empty" in captured.out

    @patch("builtins.input")
    def test_error_message_contains_validation_detail(self, mock_input, capsys):
        """Test that error message contains specific validation error details"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "8", "101", "Python", "150", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        # Verify error message contains both "Error:" and the specific validation message
        assert "Error:" in captured.out
        assert "100" in captured.out or "between" in captured.out.lower()

    @patch("builtins.input")
    def test_duplicate_student_error_message_detail(self, mock_input, capsys):
        """Test that duplicate student error shows appropriate message"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "1", "101", "Charan", "25", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Error:" in captured.out
        assert "already exists" in captured.out.lower()

    @patch("builtins.input")
    def test_view_all_students_with_data(self, mock_input, capsys):
        """Test viewing all students with multiple students"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "1", "102", "Charan", "22",
            "2", "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Hari" in captured.out
        assert "Charan" in captured.out

    @patch("builtins.input")
    def test_search_student_by_name_case_insensitive(self, mock_input, capsys):
        """Test searching by name is case-insensitive"""
        mock_input.side_effect = ["1", "101", "Hari", "21", "4", "HARI", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "101" in captured.out

    @patch("builtins.input")
    def test_marks_boundary_lower_valid(self, mock_input, capsys):
        """Test adding marks at lower boundary (0)"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "8", "101", "Python", "0",
            "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Marks added." in captured.out

    @patch("builtins.input")
    def test_marks_boundary_upper_valid(self, mock_input, capsys):
        """Test adding marks at upper boundary (100)"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "8", "101", "Python", "100",
            "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Marks added." in captured.out

    @patch("builtins.input")
    def test_age_boundary_lower_valid(self, mock_input, capsys):
        """Test updating age at lower boundary (5)"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "6", "101", "5",
            "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Age updated." in captured.out

    @patch("builtins.input")
    def test_age_boundary_upper_valid(self, mock_input, capsys):
        """Test updating age at upper boundary (100)"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "6", "101", "100",
            "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Age updated." in captured.out

    @patch("builtins.input")
    def test_create_student_with_boundary_age(self, mock_input, capsys):
        """Test creating student with age at boundaries"""
        mock_input.side_effect = ["1", "201", "Teen", "5", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student added successfully." in captured.out

    @patch("builtins.input")
    def test_marks_decimal_values(self, mock_input, capsys):
        """Test adding marks with decimal values"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "8", "101", "Python", "95.5",
            "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Marks added." in captured.out

    @patch("builtins.input")
    def test_count_students_empty_database(self, mock_input, capsys):
        """Test counting students in empty database"""
        mock_input.side_effect = ["15", "17"]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Total Students: 0" in captured.out

    @patch("builtins.input")
    def test_multiple_operations_sequence(self, mock_input, capsys):
        """Test sequence of add, search, update, and delete operations"""
        mock_input.side_effect = [
            "1", "101", "Hari", "21",
            "3", "101",
            "5", "101", "UpdatedHari",
            "3", "101",
            "7", "101",
            "17"
        ]

        from app import main

        main()

        captured = capsys.readouterr()

        assert "Student added successfully." in captured.out
        assert "Student updated." in captured.out
        assert "Student deleted." in captured.out
