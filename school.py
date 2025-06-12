class School:
    _id = 0

    def __init__(self, name:str, capacity:int, student_preferences: list, preference:dict):
        self.id = School._id
        School._id += 1
        self.name = name
        self.capacity = capacity
        self.student_preferences = student_preferences
        self._index = 0
        self.preference = preference

    def __str__(self):
        return f"id: {self.id}, name: {self.name}, capacity : {self.capacity}"

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.student_preferences):
            result = self.student_preferences[self._index]
            self._index += 1
            return result
        raise StopIteration