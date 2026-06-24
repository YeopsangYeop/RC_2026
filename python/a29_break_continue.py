import random

def main():
    num = [random.randint(0, 100) for _ in range(100)] # _ 하나짜리는 변수를 사용하지 않을 때 사용
    print(num)

    for number in num:
        if number < 50:
            continue
        print(number, end="")
        
        if number > 80:
            break


if __name__ =="__main__":
    main()