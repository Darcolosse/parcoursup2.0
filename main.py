from stable_marriage import StableMarriage


if __name__ == "__main__":
    print("Starting selection process for students...".center(100, "-"))

    marriage = StableMarriage("students.json")
    """res = marriage.selection_student()
    marriage.print_list(res[0], res[1], res[2])"""
    print("Finished processing students and schools.".center(100, "-"))
    print()
    print()
    print()
    print("Starting selection process for schools...".center(100, "-"))
    res2 = marriage.selection_school()
    marriage.print_list(res2[0], res2[1], res2[2])
    print("Finished processing students and schools.".center(100, "-"))
    
    

