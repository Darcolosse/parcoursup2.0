"""
Project Name: Parcoursup 2.0
Description: This project is an implementation of the stable marriage algorithm,
designed to simulate an admission system similar to Parcoursup.

Authors:
- Author @Darcolosse
- Author @Alexis-Wamster
"""

import sys
from stable_marriage2 import StableMarriage
from importer import Importer
from interface_graphique import Window
from viewcmd import ViewCmd

def tkinterView():
    app = Window()
    app.page_import_student()
    app.run()

def terminalView():
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


if __name__ == "__main__":
    if "-i" in sys.argv:
        tkinterView()
    else:
        terminalView()

