from pathlib import Path

class Student:
    count = int()

    def __init__(self, name, korean, math, english, science):
        #인스턴스 변수는 init 에서 생성한다(규칙은 아님)
        #밑에 함수 부분에 구현할 수 있지만 함수가 실행이 되어야 변수가 생성되기 때문에
        self.name = name
        self.korean = korean
        self.math = math
        self.english = english
        self.science = science
        Student.count += 1
        print(f"{Student.count} 번째 학생 생성")

    def student_score_sum(self):
        return self.korean + self.math + self.english + self.science

    def student_score_avg(self):
        return self.student_score_sum() / 4

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
            student = Student(name, int(korean), int(math), int(english), int(science))
            students.append(student)
    return students

def main():
    students = load_student_data()

    print(students[0].name)
    print(students[1].korean)
    print(students[2].science)

    print(f"현재 생성된 총 학생수: {Student.count}")
    #클래스 변수를 쓸때 객체에 접근해서 쓸 수 있다
    print(f"현재 생성된 총 학생수: {students[0].count}")
    #하지만 클래스 변수는 클래스에 접근해서 사용하는게 옳바르다

    print("이름 / 총점 / 평균")
    for student in students:
        Student.student_to_string(student)

if __name__ == "__main__":
    main()