import sys
from stable_marriage import StableMarriage
from importer import Importer
from interface_graphique import Window

def tkinterView():
    app = Window()
    app.page_import_student()
    app.run()

def terminalView():
    importer = Importer()
    school, student = importer.charger_fichier()
    marriage = StableMarriage(student, school)

    """ STUDENT SELECTION """
    print("Starting selection process for students...".center(100, "-"))
    #marriage = StableMarriage(student, school)
    res = marriage.selection_student()
    marriage.print_list(*res)
    print("Finished processing students and schools.".center(100, "-"))

    """ SCHOOL SELECTION """
    print("Starting selection process for schools...".center(100, "-"))
    #marriage = StableMarriage(student, school)
    res2 = marriage.selection_school()
    marriage.print_list(*res2)
    print("Finished processing students and schools.".center(100, "-"))


if __name__ == "__main__":
    if "-i" in sys.argv:
        tkinterView()
    else:
        terminalView()



