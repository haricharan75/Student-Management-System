from database import StudentDatabase


def main():
    database = StudentDatabase()

    database.add_student(101, "Hari", 22)
    database.add_student(102, "Rahul", 21)
    database.add_student(103, "Priya", 20)

    print("Student Management System")
    print("-" * 30)

    for student in database.get_all_students():
        print(student.display())


if __name__ == "__main__":
    main()
