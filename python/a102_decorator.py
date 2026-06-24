from functools import wraps

def simple_rapper(value):
    def simple_rapper_inner(func):
        @wraps(func)
        def wrapper(*args, **kargs):
            print(f"func 실행 전 코드{value}")
            func(*args, **kargs)
            print("func 실행 후 코드")
        return wrapper
    return simple_rapper_inner

@simple_rapper("hello")
def print_hello(n, v):
    for _ in range(n):
        print(v)

def main():
    print_hello(3, "hi")
    print(print_hello.__name__)


if __name__ == "__main__":
    main()