from student import Student


class Database:
    def __init__(self):
        self.students = []

    def add_student(self, student_id, name, age):
        student = Student(student_id, name, age)
        self.students.append(student)
        return student

    def get_all_students(self):
        return self.students

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None