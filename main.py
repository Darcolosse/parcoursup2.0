from stable_marriage import StableMarriage

marriage = StableMarriage("students.json")

marriage.print_preference_table_school()

print()
print()
print()

marriage.print_preference_table_student()



print()
print()
print()


marriage.selection()

