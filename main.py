from stable_marriage import StableMarriage
from importer import Importer

if __name__ == "__main__":
    # print("Starting selection process for students...".center(100, "-"))
    # school, student = Importer.importer("students.json")
    importer = Importer()
    school, student = importer.charger_fichier()

    """ STUDENT SELECTION """
    """marriage = StableMarriage(student, school)
    res = marriage.selection_student()
    marriage.print_list(*res)
    print("Finished processing students and schools.".center(100, "-"))"""

    """ SCHOOL SELECTION """
    print("Starting selection process for schools...".center(100, "-"))
    marriage = StableMarriage(student, school)
    res2 = marriage.selection_school()
    marriage.print_list(*res2)
    print("Finished processing students and schools.".center(100, "-"))

