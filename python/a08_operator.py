class Add_test:
    def __add__(self, other):
        return "더하기 연산자 오버라이딩"

def main():
    print(2**4)
    print(2**64)
    print(18/4)
    print(type(18/3))
    print(18//3)
    print(type(18//3))
    print(14%3)

    a = Add_test()
    b = Add_test()
    print(a + b)
    print(a + 123) #타입이 다른 경우지만 오류가 발생하지 않음
    print("abcd" + 5) #에러발생
    c = 5
    #print(c++) C에선 가능하지만 파이썬에선 불가능(증감 연산자가 정의되어 있지 않음)

if __name__ == "__main__":
    main()