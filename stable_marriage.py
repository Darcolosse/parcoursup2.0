import json

from school import School
from student import Student


class StableMarriage:
    school_list = []
    student_list = []

    def __init__(self, file: str):
        with open(file) as f:
            data = json.load(f)
        self.school_list = [School(school['name'], school['capacity'], school["student_preferences"]) for school in data['schools']]
        self.student_list = [Student(student['first_name'], student['last_name'],student["school_preferences"]) for student in data['students']]


    def print_preference_table(self):
        # En-tête du tableau
        header = "Students | " + " | ".join(school.name for school in self.school_list)
        print(header)
        print("-" * len(header))

        # Lignes du tableau
        for student in self.student_list:
            # Commencez par le nom de l'étudiant
            row = f"{student.first_name.ljust(10)}"  # Ajustez la largeur selon le besoin

            # Ajoutez les préférences de l'étudiant
            for i, school in enumerate(self.school_list):
                # Vérifiez si l'étudiant a une préférence pour cette école
                if i < len(student.school_preferences):
                    # Ajoutez la préférence avec un espacement approprié
                    row += f" | {str(student.school_preferences[i]).center(15)}"
                else:
                    # Ajoutez un espace vide si aucune préférence n'est définie
                    row += " | " + "".center(15)

            print(row)
