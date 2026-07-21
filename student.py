class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age

    def display(self):
        return f"ID: {self.student_id}, " f"Name: {self.name}, " f"Age: {self.age}"
