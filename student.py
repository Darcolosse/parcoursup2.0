class Student:
    _id = 0

    def __init__(self, name: str, last_name: str, school_preferences: list):
        self.id = Student._id
        Student._id += 1
        self.last_name = last_name
        self.name = name
        self.school_preferences = school_preferences
        self._index = 0
        self.preference = ""
        self.elu = False

    def remove_preferences(self, school_id: int):
        self.school_preferences.remove(school_id)

    def __str__(self):
        return f"id: {self.id}, name: {self.last_name}, first name: {self.name}"

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.school_preferences):
            result = self.school_preferences[self._index]
            self._index += 1
            return result
        raise StopIteration
