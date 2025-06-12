from typing import List


class School:
    _id = 0

    def __init__(self, name: str, capacity: int, student_preferences: List[int], preference: dict[int, "Student"]):
        self.id: int = School._id
        School._id += 1
        self.name: str = name
        self.capacity: int = capacity
        self.student_preferences: List[int] = student_preferences
        self._index: int = 0
        self.preference: dict[int, "Student"] = preference

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