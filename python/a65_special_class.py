from pathlib import Path

class Student:
    def __init__(self, name, korean, math, english, science):
        self.name = name
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science

    def student_score_sum(self):
        return self.korean + self.math + self.english + self.science

    def student_score_avg(self):
        return self.student_score_sum() / 4

    def __str__(self):
        total = self.student_score_sum()
        avg = self.student_score_avg()
        return f"{self.name}\t/ {total}\t/ {avg:.2f}"
    
    def __eq__(self, value):
        if isinstance(value, Student):
            return self.student_score_sum() == value.student_score_sum()
        else:
            return ValueError
        
    def __ne__(self, value):
        if isinstance(value, Student):
            return self.student_score_sum() != value.student_score_sum()
        else:
            return ValueError
        
    def __ge__(self, value):
        if isinstance(value, Student):
            return self.student_score_sum() >= value.student_score_sum()
        else:
            return ValueError
        
    def __lt__(self, value):
        if isinstance(value, Student):
            return self.student_score_sum() < value.student_score_sum()
        else:
            return ValueError
        
    def __le__(self, value):
        if isinstance(value, Student):
            return self.student_score_sum() <= value.student_score_sum()
        else:
            return ValueError

def main():
    student_path = Path(__file__).parent.parent / "data" / "student_info.data"
    students = []
    with open(student_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, korean, math, english, science = line.split()
            student = Student(name, int(korean), int(math), int(english), int(science))
            students.append(student)

    print(students[0].name)
    print(students[1].korean)
    print(students[2].science)

    print("이름 / 총점 / 평균")
    for student in students:
        print(student)

    if students[6] == students[8]:
        print("총합이 같다")
    else:
        print("총합이 다르다")

    print(students[0])

if __name__ == "__main__":
    main()