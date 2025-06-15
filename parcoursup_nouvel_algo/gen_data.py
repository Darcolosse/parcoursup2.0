import random
import json

student_number = 500
school_number = 5

students = []
schools = []

for elt in range(student_number):
    num_preferences = random.randint(1, school_number)
    preferences = random.sample(range(school_number), num_preferences)
    students.append({
        "name": f"student{elt}",
        "capacity": 1,
        "preferences": preferences,
    })

for elt in range(school_number):
    num_preferences = random.randint(1, student_number)
    preferences = random.sample(range(student_number), num_preferences)
    schools.append({
        "name": f"school{elt}",
        "capacity": random.randint(1, 100),
        "preferences": preferences,
    })

data = {
    "students": students,
    "schools": schools
}

with open("data.json", "w") as f:
    json.dump(data, f)
