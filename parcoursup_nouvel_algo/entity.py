from typing import List


class Entity:
    _id_student:int = 0
    _id_school:int = 0

    def __init__(self, name: str, capacity: int, preferences: list[int], is_student: bool) -> None:
        """
        Initializes an Entity with a name, capacity, preferences, and whether it is a student or a school.
        This constructor sets the ID based on whether the entity is a student or a school, initializes the name, capacity,

        Args:
            name (str): The name of the entity.
            capacity (int): The maximum number of preferences the entity can have.
            preferences (list[int]): A list of preferred entities' IDs.
            is_student (bool): Whether the entity is a student (True) or a school (False).
        """
        
        # Initialize the ID based on whether the entity is a student or a school
        if is_student:
            self.id: int = Entity._id_student
            Entity._id_student += 1
        else:
            self.id: int = Entity._id_school
            Entity._id_school += 1
        
        # Set the name, capacity, preferences and initialize wish
        self.name: str = name
        self.capacity: int = capacity
        self.preferences: dict[int, Entity] = {key: None for key in preferences}
        self.is_student: bool = is_student
        self.wish: List[Entity] = []

        self._index: int = 0
    
    def set_preference(self, preferences: list[int]) -> None:
        self.preferences: dict[int, Entity] = {key: None for key in preferences}


    def initialise_wishes(self, dict_object_wish : dict[int, "Entity"]) -> None:
        """
        Initializes the wish dictionary with entities from the provided list that match the keys in the preference dictionary.
        This method populates the wish dictionary with entities that are present in the list of wishes and match the keys in the preference dictionary.
        This allows the entity to have a list of preferred entities that it can interact with, based on its preferences.

        Args:
            list_object_wish (List[Entity]): A list of entities that the current entity wishes to interact with.
        """
        # Initialize the wish dictionary with preferences
        self.wish = []
        for key in self.preferences.keys():
            if key in list(dict_object_wish.keys()):
                self.wish.append(dict_object_wish[key])
                
                
    
    @staticmethod
    def initialise_preference(list_object_to_initialise : List["Entity"], list_object_wish : List["Entity"]) -> None:
        # Create a dictionary of wishes
        dict_object_wish = {wish.id: wish for wish in list_object_wish}
        
        for object in list_object_to_initialise:
            object.wish = []
            for key in object.preferences.keys():
                if key in list(dict_object_wish.keys()):
                    object.wish.append(dict_object_wish[key])

    def compare(self, a: "Entity", b: "Entity") -> bool:
        return self.wish.index(a) > self.wish.index(b)

    def get_capacity(self) -> int:
        return len(self.preferences) - list(self.preferences.values()).count(None)

    def get_preference(self) -> List[int]:
        """
        Returns the keys of the preference dictionary.
        This method retrieves the keys from the preference dictionary, which represent the IDs of the preferred entities.

        Returns:
            list[int]: A list of the IDs of the preferred entities.
        """
        return list(self.preferences.keys())
    
    def is_full(self) -> bool:
        """
        Check if the entity has reached its capacity based on the number of non-None preferences.
        This method counts the number of preferences that are not None and compares it to the entity's capacity.

        Returns:
            bool: True if the entity is full, False otherwise.
        """
        return (len(self.preferences) - list(self.preferences.values()).count(None)) >= self.capacity
    
    def str_compact(self) -> str:
        """
        Returns a compact string representation of the entity.
        This includes the name, current number of preferences, and capacity.
        
        Returns:
            str: A string in the format "name (current_preferences/capacity)".
        """
        return f"{self.name}  ({len(self.preferences)}/{self.capacity})"

    def __str__(self) -> str:
        """
        Returns a string representation of the entity.

        Returns:
            str: A string in the format "id: {id}, name: {name}, capacity: {capacity}".
        """
        return f"id: {self.id}, name: {self.name}, capacity : {self.capacity}"
    
    def __repr__(self):
        """
        Returns a detailed string representation of the entity, including its ID, name, capacity,
        preferences, and whether it is a student.

        Returns:
            str: A detailed string representation of the entity.
        """
        #return f"Entity(id={self.id}, name='{self.name}', capacity={self.capacity}, preferences={self.get_preference()}, is_student={self.is_student})"
        return f"Entity({self.name} : {self.id})"

    def __iter__(self) -> "Entity":
        """
        Returns an iterator for the entity, allowing iteration over its preferences.
        This method allows the entity to be used in a for-loop or any context that requires an iterator.

        Returns:
            Entity: The entity itself, allowing iteration over its preferences.
        """
        return self

    def __next__(self) -> "Entity":
        """
        Returns the next preference in the entity's list of preferences.
        If there are no more preferences, it raises StopIteration.

        Returns:
            Entity: The next preference in the entity's list of preferences.

        Raises:
            StopIteration: If there are no more preferences.
        """
        if self._index < len(self.wish):
            result = self.wish[self._index]
            self._index += 1
            return result
        raise StopIteration

    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.id == other.id and self.name == other.name and self.capacity == other.capacity
        return False