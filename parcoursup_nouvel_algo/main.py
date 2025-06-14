from stable_marriage2 import StableMarriage
from importer import Importer
from viewcmd import ViewCmd

if __name__ == "__main__":
    # print("Starting selection process for students...".center(100, "-"))
    # school, student = Importer.importer("students.json")
    importer = Importer()
    school, student = importer.charger_fichier()
    ViewCmd.print_preference_table(school, student)
    print("".center(80, "#"))
    ViewCmd.print_preference_table(student, school)

    """ STUDENT SELECTION """
    # marriage = StableMarriage(student, school)
    # res = marriage.selection_school()
    # ViewCmd.print_list(*res)

    """ SCHOOL SELECTION """
    marriage = StableMarriage(school, student)
    res2 = marriage.selection_school()
    ViewCmd.print_list(*res2)

