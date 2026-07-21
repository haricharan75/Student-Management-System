from unittest.mock import patch

import app


class DummyStudent:
    def display(self):
        return {
            "Student ID": 101,
            "Name": "Hari",
            "Age": 21,
            "Courses": ["Python"],
            "Marks": {"Python": 95},
            "Average": 95,
            "Grade": "A+",
            "Passed": True,
        }


def test_display_student(capsys):
    app.display_student(DummyStudent())

    output = capsys.readouterr().out

    assert "Hari" in output
    assert "Python" in output
    assert "A+" in output


def test_menu(capsys):
    app.menu()

    output = capsys.readouterr().out

    assert "Student Management System" in output
    assert "Add Student" in output
    assert "Exit" in output


@patch("builtins.input", side_effect=["17"])
def test_main_exit(mock_input, capsys):
    app.main()

    output = capsys.readouterr().out

    assert "Exiting..." in output


@patch(
    "builtins.input",
    side_effect=["1", "101", "Hari", "21", "17"],
)
def test_add_student(mock_input, capsys):
    app.main()

    output = capsys.readouterr().out

    assert "Student added successfully." in output


# @patch(
#     "builtins.input",
#     side_effect=[
#         "1",
#         "101",
#         "Hari",
#         "21",
#         "2",
#         "17",
#     ],
# )
# def test_view_all_students(mock_input, capsys):
#     app.main()

#     output = capsys.readouterr().out

#     assert "Hari" in output


# @patch(
#     "builtins.input",
#     side_effect=[
#         "1",
#         "101",
#         "Hari",
#         "21",
#         "3",
#         "101",
#         "17",
#     ],
# )
# # def test_search_student_by_id(mock_input, capsys):
# #     app.main()

# #     output = capsys.readouterr().out

# #     assert "Hari" in output


# @patch(
#     "builtins.input",
#     side_effect=[
#         "1",
#         "101",
#         "Hari",
#         "21",
#         "4",
#         "Hari",
#         "17",
#     ],
# )
# def test_search_student_by_name(mock_input, capsys):
#     app.main()

#     output = capsys.readouterr().out

#     assert "Hari" in output


# @patch(
#     "builtins.input",
#     side_effect=[
#         "1",
#         "101",
#         "Hari",
#         "21",
#         "5",
#         "101",
#         "Charan",
#         "17",
#     ],
# )
# def test_update_name(mock_input, capsys):
#     app.main()

#     output = capsys.readouterr().out

#     assert "Student updated." in output


# @patch(
#     "builtins.input",
#     side_effect=[
#         "1",
#         "101",
#         "Hari",
#         "21",
#         "6",
#         "101",
#         "25",
#         "17",
#     ],
# )
# def test_update_age(mock_input, capsys):
#     app.main()

#     output = capsys.readouterr().out

#     assert "Age updated." in output


# @patch(
#     "builtins.input",
#     side_effect=[
#         "1",
#         "101",
#         "Hari",
#         "21",
#         "7",
#         "101",
#         "17",
#     ],
# )
# def test_delete_student(mock_input, capsys):
#     app.main()

#     output = capsys.readouterr().out

#     assert "Student deleted." in output


@patch(
    "builtins.input",
    side_effect=[
        "1",
        "101",
        "Hari",
        "21",
        "8",
        "101",
        "Python",
        "95",
        "17",
    ],
)
def test_add_marks(mock_input, capsys):
    app.main()

    output = capsys.readouterr().out

    assert "Marks added." in output


@patch(
    "builtins.input",
    side_effect=[
        "1",
        "101",
        "Hari",
        "21",
        "9",
        "101",
        "Python",
        "17",
    ],
)
def test_enroll_course(mock_input, capsys):
    app.main()

    output = capsys.readouterr().out

    assert "Course enrolled." in output


@patch(
    "builtins.input",
    side_effect=[
        "1",
        "101",
        "Hari",
        "21",
        "15",
        "17",
    ],
)
def test_count_students(mock_input, capsys):
    app.main()

    output = capsys.readouterr().out

    assert "Total Students" in output


@patch(
    "builtins.input",
    side_effect=[
        "16",
        "17",
    ],
)
def test_clear_database(mock_input, capsys):
    app.main()

    output = capsys.readouterr().out

    assert "Database cleared." in output


@patch(
    "builtins.input",
    side_effect=[
        "99",
        "17",
    ],
)
def test_invalid_choice(mock_input, capsys):
    app.main()

    output = capsys.readouterr().out

    assert "Invalid choice." in output


@patch(
    "builtins.input",
    side_effect=[
        "1",
        "abc",
        "17",
    ],
)
def test_value_error(mock_input, capsys):
    app.main()

    output = capsys.readouterr().out

    assert "Error:" in output
