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
            for key in object.preference.keys():
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
        
        print("courtier list :", courtier_list)
        print("courted list :", courted_list)
        
        dict_object_wish = {wish.id: wish for wish in courtier_list}
        [courted.initialise_wishes(dict_object_wish) for courted in courted_list]
        
        dict_object_wish = {wish.id: wish for wish in courted_list}
        [courtier.initialise_wishes(dict_object_wish) for courtier in courtier_list]
        
        # Récupération de toutes les écoles
        courted_free: list[Entity] = [courted for courted in courted_list]
        while courted_free:
            cur_courted_free = copy.deepcopy(courted_free)
            iteration += 1
            print(len(courted_free), "courted free at iteration", iteration )
            while cur_courted_free:
                courted = cur_courted_free.pop(0)
                print("Courted free:", courted.name)
                
                
                
            courted_free = copy.deepcopy(cur_courted_free)
        courtier_with_no_courted = [courtier for courtier in courtier_list if courtier.preference is None]

        return (courted_list, courtier_with_no_courted, iteration)

    @staticmethod
    def invite(courtier: Entity, courted: Entity, courted_free: List[Entity]) -> None:        
        if courted in courtier.wish:
            if courtier.is_full() == False:
                courtier.preference[courted.id] = courted
                courted.preference[courtier.id] = courtier
            else:
                preference_decroissant = reversed(list(courtier.preference.items()))
                for key, current_school in preference_decroissant:
                    if current_school is not None:
                        if key in courtier.wish:
                            if courtier.wish.index(key) > courtier.wish.index(courted.id):
                                StableMarriage.refuse(courtier, current_school, courted_free)
                                courtier.preference[courted.id] = courted
                                print("   switcher")
                                break

    @staticmethod
    def refuse(courtier: Entity, courted: Entity, courted_free: List[Entity]) -> None:
        courted.preference[courtier.id] = None
        if courted not in courted_free:
            courted_free.append(courted)
