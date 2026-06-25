import json
from pathlib import Path

def main():
    student_path = Path(__file__).parent.parent / "data" / "student_info.json"
    with open(student_path, "r", encoding='utf-8') as f:
        students = json.load(f)

    print("이름 / 총점 / 평균")
    for student in students:
        score_sum = (student["korean"] + student["math"] + student["english"] + student["science"])
        score_avg = score_sum / 4
        print(f"총점: {score_sum} / 평균: {score_avg}")
    


if __name__ == "__main__":
    main()