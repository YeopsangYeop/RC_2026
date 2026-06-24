class MinusError(Exception):
    def __init__(self, *args):
        message = "음수는 허용하지 않습니다"
        super().__init__(message)

def main():
    user_input = input("양의 정수 입력: ")
    try:
        number = int(user_input)
        if number < 0:
            raise MinusError
    except MinusError as e:
        print(e)
    except ValueError as e:
        print(e)
    else:
        print(f"양의정수 {number}")
    finally:
        print("프로그램 종료")

if __name__ == "__main__":
    main()
