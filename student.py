from typing import List
class Student:
    _id: int = 0

    def __init__(self, name: str, last_name: str, school_preferences: List[int]):
        self.id: int = Student._id
        Student._id += 1
        self.last_name: str = last_name
        self.name: str = name
        self.school_preferences: List[int] = school_preferences
        self._index: int = 0
        self.preference: "School" = None
        self.elu = False

    def remove_preferences(self, school_id: int):
        self.school_preferences.remove(school_id)
    
    def set_preference(self, new_pref):
        self.school_preferences = new_pref
    
    def str_compact(self):
        return f"{self.id} {self.name}"

    

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
