import pickle
import random
from pathlib import Path

def main():
    li = {random.random(0, 100) for _ in range(1000)}
    pickle_path = Path(__file__).parent / "random_list_pickle"
    with pickle_path.open("wb") as f:
        pickle.dump(li, f)
    print("피클 파일 생성 완료")

if __name__ == "__main__":
    main()