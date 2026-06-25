class Test:
    def __init__(self, name):
        self.name = name
        print(f"{self.name} 생성")

    def __del__(self):
        print(f"{self.name} 파괴")

def main():
    a = Test("A")
    b = Test("B")
    c = Test("C")
    print(a, b, c)

    del c #c를 동적으로 삭제

if __name__ == "__main__":
    main()