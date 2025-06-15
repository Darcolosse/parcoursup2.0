from stable_marriage2 import StableMarriage
from importer import Importer
from viewcmd import ViewCmd

if __name__ == "__main__":
    # print("Starting selection process for students...".center(100, "-"))
    # school, student = Importer.importer("students.json")
    importer = Importer()
    school, student = importer.charger_fichier()
    ViewCmd.print_preference_table("ECOLES", school, student)
    print()
    ViewCmd.print_preference_table("ETUDIANTS", student, school)

    """ STUDENT SELECTION """
    print("  STUDENT SELECTION  ")
    marriage = StableMarriage(student, school)
    res = marriage.selection_student()
    ViewCmd.print_list(res[2], res[1], res[-1])

    """ SCHOOL SELECTION """
    print("  SCHOOL SELECTION  ")
    marriage = StableMarriage(student, school)
    res2 = marriage.selection_school()
    ViewCmd.print_list(res2[0], res2[1], res2[-1])


