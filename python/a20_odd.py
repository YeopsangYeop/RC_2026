def main():
    num = int(input("정수 입력: "))

    if(num % 2 == 0): #0이면 False, 1이면 True
        print(f"{num}은 짝수입니다")
    else:
        print(f"{num}은 홀수입니다")


if __name__ == "__main__":
    main()