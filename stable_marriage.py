import json
from typing import List, Tuple

from school import School
from student import Student


class StableMarriage:
    school_list = []
    student_list = []

    def __init__(self, file: str):
        with open(file, "r", encoding='utf-8') as f:
            data = json.load(f)

        self.school_list = [School(school['name'], school['capacity'], school["student_preferences"], {key: None for key in school["student_preferences"]}) for school in data['schools']]

        self.student_list = [Student(student['first_name'], student['last_name'], student["school_preferences"]) for student in data['students']]

    def selection_student(self) -> Tuple[List[School], List[School]]:
        iteration = 0
        # Liste des étudiants libres
        student_free = self.student_list.copy()
        student_with_no_school = []

        while student_free:
            print(iteration)
            iteration += 1
            student = student_free.pop(0)
            reject = True;
            if student.school_preferences:
                school = self.school_list[student.school_preferences.pop(0)]

                # Vérifier si l'école a de la
                capacity = (len(school.preference) - list(school.preference.values()).count(None)) < school.capacity
                if capacity and student.id in school.student_preferences:
                    # Ajouter l'étudiant à l'école
                    school.preference[student.id] = student
                    reject = False

                else:
                    for key, current_student in school.preference.items():
                        if student.id in school.student_preferences:
                            if current_student is not None:
                                # Comparer les préférences des étudiants
                                if school.student_preferences.index(key) > school.student_preferences.index(student.id):
                                    # Remplacer l'étudiant actuel par le nouvel étudiant
                                    school.preference[key] = None
                                    school.preference[student.id] = student

                                    student_free.append(current_student)
                                    reject = False;
                                    break
                if reject:
                    student_with_no_school.append(student)
            else:
                student_with_no_school.append(student)

        return (self.school_list, student_with_no_school, iteration)


    
    def selection_school(self) -> Tuple[List[School], List[School], int]:
        iteration = 0
        
        student_list = self.student_list.copy()
        school_list = self.school_list.copy()
        # Copie de la liste des écoles à traiter
        school_free: List[School] = self.school_list.copy()

        while school_free:
            iteration += 1
            school = school_free.pop(0)

            # Tant que l'école n'a pas atteint sa capacité maximale
            while self.occupied_capacity(school.preference) < school.capacity:
                if school.student_preferences:
                    # Prend le premier étudiant de la liste de préférence de l'école
                    student = student_list[school.student_preferences.pop(0)]
                    # Invite l'étudiant à rejoindre l'école
                    self.inviter(student, school, school_free)
                else:
                    # L'école n'a plus de préférences à traiter ou est pleine
                    break

        student_with_no_school += [student for student in self.student_list if student.preference is None]

        return (school_list, student_with_no_school, iteration)
            
                
    def occupied_capacity(self, dico: dict[int, Student | School]) -> int:
        # Retourne le nombre d'étudiants actuellement acceptés (non None) dans le dictionnaire de préférence
        return len(dico) - list(dico.values()).count(None)

    def inviter(self, student: Student, school: School, school_free: List[School]) -> None:
        switch_school = False
        # Si l'étudiant ne veut pas de l'école, rejeter l'invitation
        if school.id in student.school_preferences:
            # Si l'étudiant n'a pas encore d'école
            if (student.preference == None):
                switch_school = True # l'étudiant accepte l'invitation
                
            # Si l'étudiant préfère cette école à son affectation actuelle
            elif (student.school_preferences.index(student.preference.id) > student.school_preferences.index(school.id)):
                self.refuser(student, student.preference, school_free) # l'étudiant quitte son ancienne école
                switch_school = True
                
            if switch_school:
                # Affecte l'étudiant à la nouvelle école
                school.preference[student.id] = student
                student.preference = school
            

    def refuser(self, student, school, school_free):
        # Retire l'étudiant de l'école
        school.preference[student.id] = None
        # Remet l'école dans la liste des écoles libres si besoin
        if school not in school_free:
            school_free.append(school) # Attention : elle y est peut-être déjà


    
    def print_preference_table_school(self):
        col = " " * 15
        for elt in range(1, len(self.student_list)+1):
            col += f"{elt}".center(14, " ") + "|"
        print(col)

        print("-"*(15*len(self.student_list)+15))

        for elt in range(0, len(self.school_list)):
            row = f"{self.school_list[elt].name}".center(14, " ") + "#"
            for preference_student in self.school_list[elt].student_preferences:
                row += self.student_list[preference_student].name.center(14, " ") + "|"
            print(row)
            print("-"*(15*len(self.student_list)+15))


    def print_preference_table_student(self):
        col = " " * 15
        for elt in range(1, len(self.school_list)+1):
            col += f"{elt}".center(14, " ") + "|"
        print(col)

        print("-"*(15*len(self.school_list)+15))

        for elt in range(0, len(self.student_list)):
            row = f"{self.student_list[elt].name}".center(14, " ") + "#"
            for school_preference in self.student_list[elt].school_preferences:
                row += self.school_list[school_preference].name.center(14, " ") + "|"
            print(row)
            print("-"*(15*len(self.school_list)+15))


    def print_list(self, accepted_list: List[School], unaccepted_list: List[School], iteration: int) -> None:
        for elt in accepted_list:
            accepted_students = [student.name for student in elt.preference.values() if student is not None]
            print(f"{elt.name} a accepté les étudiants ({len(accepted_students)}) :", accepted_students,"\n")

        # Afficher les étudiants non affectés
        print(f"Étudiants non affectés ({len(unaccepted_list)}) :", [elt.name for elt in unaccepted_list],"\n")

        print(f"Nombre d'itérations : {iteration} sur un total de {len(self.school_list)} écoles et {len(self.student_list)} étudiants.\n")



