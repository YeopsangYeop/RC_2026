import time

def main():
    i = int()
    while i < 10:
        print(str(i) + "번째 실행중")
        i += 1

    try:
        while True:
            print('무한루프', end = " ", flush = True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("키보드 인터럽트 발생")

    list_test = list("kim sang yeop")
    print(list_test)
    while "s" in list_test:
        list_test.remove("s")
    print(list_test)


if __name__ == "__main__":
    main()