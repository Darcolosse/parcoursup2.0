from typing import List, Iterator


class School:
    _id: int = 0

    def __init__(self, name: str, capacity: int, student_preferences: List[int], preference: dict[int, "Student"]) -> None:
        self.id: int = School._id
        School._id += 1
        self.name: str = name
        self.capacity: int = capacity
        self.student_preferences: List[int] = student_preferences
        self._index: int = 0
        self.preference: dict[int, "Student"] = preference
    
    def set_preference(self, new_pref: List[int]) -> None:
        self.student_preferences = new_pref
        self.preference = {key: None for key in self.student_preferences}
    
    def str_compact(self) -> str:
        return f"{self.name}  ({len(self.preference)}/{self.capacity})"

    def __str__(self) -> str:
        return f"id: {self.id}, name: {self.name}, capacity : {self.capacity}"

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if self._index < len(self.student_preferences):
            result = self.student_preferences[self._index]
            self._index += 1
            return result
        raise StopIteration