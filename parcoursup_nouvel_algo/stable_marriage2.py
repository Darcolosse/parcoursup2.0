import copy
from typing import List, Tuple
from entity import Entity
from viewcmd import ViewCmd

class StableMarriage:
    school_list: List[Entity] = []
    student_list: List[Entity] = []

    def __init__(self, student_list: List[Entity], school_list: List[Entity]) -> None:
        self.school_list = school_list
        self.student_list = student_list

    @staticmethod
    def initialise_preference(list_object_to_initialise : List[Entity], list_object_wish : List[Entity]) -> None:
        # Create a dictionary of wishes
        dict_object_wish = {wish.id: wish for wish in list_object_wish}
        
        for object in list_object_to_initialise:
            object.wish = []
            for key in object.preferences.keys():
                if key in list(dict_object_wish.keys()):
                    object.wish.append(dict_object_wish[key])

    def selection_student(self):
        return StableMarriage.stable_matching(
                copy.deepcopy(self.student_list),
                copy.deepcopy(self.school_list)
            )

    def selection_school(self):
        return StableMarriage.stable_matching(
                copy.deepcopy(self.school_list),
                copy.deepcopy(self.student_list),    
            )

    @staticmethod
    def stable_matching(courtier_list : List[Entity], courted_list : List[Entity]) -> Tuple[List[Entity], List[Entity], int]:
        iteration = 0

        courtier_list = copy.deepcopy(courtier_list)
        courted_list = copy.deepcopy(courted_list)

        dict_object_wish = {wish.id: wish for wish in courtier_list}
        [courted.initialise_wishes(dict_object_wish) for courted in courted_list]
        
        dict_object_wish = {wish.id: wish for wish in courted_list}
        [courtier.initialise_wishes(dict_object_wish) for courtier in courtier_list]


        # Récupération de tous les courtisans
        courtier_free: list[Entity] = [courtier for courtier in courtier_list]

        cur_courtier_free = courtier_free.copy()


        while cur_courtier_free:
            iteration += 1
            courtier = cur_courtier_free.pop(0)
            courted = courtier.wish.pop(0)


            StableMarriage.invite(courtier, courted, cur_courtier_free)

        courtier_with_no_courted = [courtier for courtier in courtier_list if courtier.preferences is None]

        return (courted_list, courtier_with_no_courted, iteration)

    @staticmethod
    def invite(courtier: Entity, courted: Entity, courtier_free: List[Entity]) -> None:
        #print(f"invitation de {courtier.name} à {courted.name}")

        if courtier in courted.wish:
            #print(f"    Mon courtisant {courtier.name} à {courtier.preferences}")
            #print(f"    Mon courtisant {courtier.name} est accepté par {courted.name}")
            if not courted.is_full():
                #print("        VENEZ J'AI DE LA PLACE ".center(20, "#"))
                StableMarriage.accept(courtier, courted)
                #print("        ", courtier.preferences)

            else:
                for key_id, current_courtier in reversed(courted.preferences.items()):
                    if current_courtier is not None:
                        #print(f"        {current_courtier.__repr__()} VS {courtier.__repr__()}")
                        if courted.compare(current_courtier, courtier):
                            StableMarriage.refuse(current_courtier, courted, courtier_free)
                            StableMarriage.accept(courtier, courted)
                            #print(f"        {courtier.name} a été accepté par {courted.name}")

                            break
                        else:
                            courtier_free.append(courtier)

    @staticmethod
    def refuse(courtier: Entity, courted: Entity, courtier_free: List[Entity]) -> None:
        courted.preferences[courtier.id] = None
        courtier.preferences[courtier.id] = None

        if courtier not in courtier_free:
            courtier_free.append(courtier)

    @staticmethod
    def accept(courtier: Entity, courted: Entity) -> None:
        courted.preferences[courted.id] = courtier
        courtier.preferences[courtier.id] = courted
