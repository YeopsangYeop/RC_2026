def main():
    str = input("상품명을 입력하세요: ")
    num = input("가격을 입력하세요: ")
    try:
        num = int(num)
    except ValueError:
        print("입력한 값이 숫자가 아닙니다.")
        return
    
    h = input("할인률 입력하세요: ")
    try:
        h = int(h)
    except ValueError:
        print("입력한 값이 숫자가 아닙니다.")
        return
    
    Hnum = num * h / 100
    Fnum = num - Hnum
    print(f"상품명: {str}, 가격: {num}, 할인률: {h}%, 할인금액: {Hnum}, 최종가격: {Fnum}")


if __name__ == "__main__":
    main()