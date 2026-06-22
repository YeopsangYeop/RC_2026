def main():
    var = input("숫자 입력: ")
    print(var, type(var)) #input() 함수는 항상 문자열을 반환하기 때문에 var의 타입은 str입니다.

    try:
        print(int(var) + 100)
    except ValueError:
        print("입력한 값이 숫자가 아닙니다.")

    var = int(var)
    print(var, type(var))

if __name__ == "__main__":
    main()