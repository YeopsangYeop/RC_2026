from pathlib import Path

class Student:
    count = int()
    students =[]

    def __init__(self, name, korean, math, english, science):
        self.name = name
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science
        Student.count += 1
        Student.students.append(self)
        print(f"{Student.count} 번째 학생 생성")

    def student_score_sum(self):
        return self.korean + self.math + self.english + self.science

    def student_score_avg(self):
        return self.student_score_sum() / 4
    
    @classmethod
    def print(cls):
        print(f"현재 생성된 총 학생수 {Student.count}")
        print()
        print("----------------------학생목록-----------------------")
        print("이름 / 총점 / 평균")
        for student in cls.students:
            print(student)
        print("--------------------------------------------------------")

    def student_to_string(self):
        total = self.student_score_sum()
        avg = self.student_score_avg()
        print(f"{self.name}\t/ {total}\t/ {avg:.2f}")

def load_student_data():
    student_path = Path(__file__).parent.parent / "data" / "student_info.data"
    students = []
    with open(student_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, korean, math, english, science = line.split()
            Student(name, int(korean), int(math), int(english), int(science))

def main():
    students = load_student_data()
    Student.print()

if __name__ == "__main__":
    main()