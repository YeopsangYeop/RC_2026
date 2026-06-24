def test(): #함수의 실행이 매번 다른 결과를 요구할때 블럭을 여러개로 분기해서 표현 (yield로 구분)
    print("A함수가 호출 되었습니다")
    yield 0 #return 값?
    print("B함수가 호출 되었습니다")
    yield 1
    print("C함수가 호출되었습니다")

def main():
    ge = test()
    print(ge)

    ge.__next__()
    next(ge)

    for re in ge:
        print(re)

if __name__ == "__main__":
    main()