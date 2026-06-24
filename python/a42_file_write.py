from pathlib import Path

def main():
    f = open(Path(__file__).parent / "text.txt", "w")
    f.write("안녕하세요")
    f.close()

    with open(Path(__file__).parent.parent / "data" / "text.txt", "w", encoding="utf-8") as f:
        f.write("안녕하세요")

if __name__ == "__main__":
    main()