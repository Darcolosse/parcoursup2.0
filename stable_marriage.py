import json
from typing import List

from school import School
from student import Student


class StableMarriage:
    school_list = []
    student_list = []

    def __init__(self, file: str):
        with open(file, "r", encoding='utf-8') as f:
            data = json.load(f)
        self.school_list = [School(school['name'], school['capacity'], school["student_preferences"], {key: None for key in school["student_preferences"]}) for school in data['schools']]

        self.student_list = [Student(student['first_name'], student['last_name'],student["school_preferences"]) for student in data['students']]


    def selection_student(self):
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

    # Afficher les résultats
        for school in self.school_list:
            accepted_students = [student.name for student in school.preference.values() if student is not None]
            print(f"{school.name} a accepté les étudiants: {accepted_students}")

        # Afficher les étudiants non affectés
        print("Étudiants non affectés :", [student.name for student in student_with_no_school])





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



