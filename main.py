from stable_marriage import StableMarriage

if __name__ == "__main__":

    print("Starting selection process for schools...".center(100, "-"))
    # Réinitialiser les listes en recréant l'objet StableMarriage
    marriage = StableMarriage("students.json")
    res2 = marriage.selection_student()
    marriage.print_list(*res2)
    print("Finished processing students and schools.".center(100, "-"))
