class School:
    _id = 1

    def __init__(self, name:str, capacity:int, student_preferences: list):
        self.id = School._id
        School._id += 1
        self.name = name
        self.capacity = capacity
        self.student_preferences = student_preferences

    def __str__(self):
        return f"id: {self.id}, name: {self.name}, capacity : {self.capacity}"

    def __iter__(self):
            return self

    def __next__(self):
        if self.current < self.id:
            self.current += 1
            return self.current
        else:
            raise StopIteration