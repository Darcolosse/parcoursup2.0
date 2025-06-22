"""
Project Name: Parcoursup 2.0
Description: This project is an implementation of the stable marriage algorithm,
designed to simulate an admission system similar to Parcoursup.

Authors:
- Author GOUES Corentin
- Author WAMSTER Alexis
"""

from typing import List
from entity import Entity # type: ignore


class ViewCmd:

    def __init__(self):
        print("Ne fait rien")

    @staticmethod
    def print_preference_table(title: str, school_list: List[Entity], student_list: List[Entity]):
        
        # ANSI color codes
        CYAN = "\033[96m"
        YELLOW = "\033[93m"
        RESET = "\033[0m"

        print("".center(75, "#"))
        print(f" TABLEAU DES PRÉFÉRENCES DES {title} ".center(75, "#"))
        print("".center(75, "#"))

        col = " " * 14 +"#"
        for elt in range(1, len(student_list)+1):
            col += f"{YELLOW}{elt}{RESET}".center(14 + len(CYAN) + len(RESET), " ") + "|"
        print(col)

        print("-"*(15*len(student_list)+15))

        for elt in range(0, len(school_list)):
            row = f"{CYAN}{school_list[elt].name}{RESET}".center(14 + len(CYAN) + len(RESET), " ") + "#"
            for preference_student in list(school_list[elt].preferences.keys()):
                row += f"{YELLOW}{student_list[preference_student].name}{RESET}".center(14 + len(CYAN) + len(RESET), " ") + "|"
            print(row)
            print("-"*(15*len(student_list)+15))


    @staticmethod
    def print_list(accepted_list: List[Entity], unaccepted_list: List[Entity], iteration: int) -> None:
        # ANSI color codes
        GREEN = "\033[92m"
        RED = "\033[91m"
        CYAN = "\033[96m"
        YELLOW = "\033[93m"
        RESET = "\033[0m"
        print()
        print("Résultat de la selection : \n")

        for elt in accepted_list:
            accepted_students = [f"{student.name}" for student in elt.preferences.values() if student is not None]
            print(f"{CYAN}{elt.name}{RESET} a accepté {GREEN}({len(accepted_students)}/{elt.capacity}){RESET} :", f"{YELLOW}{accepted_students}{RESET}")

        # Afficher les étudiants non affectés
        print(f"{RED}Étudiants non affectés ({len(unaccepted_list)}){RESET} :", f"{YELLOW}{[elt.name for elt in unaccepted_list]}{RESET}\n")

        print(f"{CYAN}Nombre d'itérations : {iteration}.{RESET}\n")