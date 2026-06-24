#함수 안에서 만든 내부 함수가 바깥 함수의 변수를 기억하는 구조

def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter

def main():
    a = make_counter()
    print(type(a)) #main에 a 객체가 남아있다
    print(a())
    print(a())
    b = make_counter()
    print(a())
    print(b())
    print(b())

if __name__ == "__main__":
    main()