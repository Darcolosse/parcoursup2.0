from typing import List, Iterator


class Student:
    _id: int = 0

    def __init__(self, name: str, last_name: str, school_preferences: List[int]) -> None:
        self.id: int = Student._id
        Student._id += 1
        self.last_name: str = last_name
        self.name: str = name
        self.school_preferences: List[int] = school_preferences
        self._index: int = 0
        self.preference: "School" = None
        self.elu = False

    def remove_preferences(self, school_id: int) -> None:
        self.school_preferences.remove(school_id)
    
    def set_preference(self, new_pref) -> None:
        self.school_preferences = new_pref
    
    def str_compact(self) -> str:
        return f"{self.id} {self.name}"

    def __str__(self) -> str:
        return f"id: {self.id}, name: {self.last_name}, first name: {self.name}"

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if self._index < len(self.school_preferences):
            result = self.school_preferences[self._index]
            self._index += 1
            return result
        raise StopIteration
