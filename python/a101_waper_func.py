def simple_rapper(func):
    def wrapper():
        print("func 실행 전 코드")
        func()
        print("func 실행 후 코드")
    return wrapper

@simple_rapper
def print_hello():
    print("함수 실행")

def main():
    print_hello()


if __name__ == "__main__":
    main()