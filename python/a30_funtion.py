def print_hello(a: int, value: str) -> str: #매개변수와 리턴값에 힌트를 줄 수 있음
    for i in range(a):
        print("안녕하세요", value, i+1)
    return "실행 완료"

def main():
    re = print_hello(3, "김상엽")
    print(re)

if __name__ == "__main__":
    main()