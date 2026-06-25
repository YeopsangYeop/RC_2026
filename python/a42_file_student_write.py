from pathlib import Path

def main():

    with open(Path(__file__).parent.parent / "data" / "student_info.data", "a", encoding="utf-8") as f:
        f.write("\n김상엽 10 20 30 40")
        f.close()

if __name__ == "__main__":
    main() 