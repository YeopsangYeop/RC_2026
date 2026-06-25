from pathlib import Path

def create_student(name, korean, math, english, science):
    return {"name" : name, "korean" : korean, "math" : math, "english" : english, "science" : science}

def student_score_sum(student):
    return (student["korean"] + student["math"] + student["english"] + student["science"])

def student_score_avg(student):
    return student_score_sum(student) / 4

def student_to_string(student):
    total = student_score_sum(student)
    avg = student_score_avg(student)
    print(f"{student['name']}\t/ {total}\t/ {avg:.2f}")

def main():
    student_path = Path(__file__).parent.parent / "data" / "student_info.data"
    students = []
    with open(student_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, korean, math, english, science = line.split()
            student = create_student(name, int(korean), int(math), int(english), int(science))
            students.append(student)

    print("이름 / 총점 / 평균")
    for student in students:
        student_to_string(student)

if __name__ == "__main__":
    main()