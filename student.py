class Student:
    _id = 1

    def __init__(self, first_name: str, last_name: str, school_preferences: list):
        self.id = Student._id
        Student._id += 1
        self.last_name = last_name
        self.first_name = first_name
        self.school_preferences = school_preferences

    def __str__(self):
        return f"id: {self.id}, name: {self.last_name}, first name: {self.first_name}"
