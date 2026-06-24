import time

def main():
    print(time.asctime())
    print(time.time())
    print(time.clock_gettime_ns(1))

    ptime = time.time()
    cnt = int()
    while time.time() < ptime + 5:
        cnt += 1
    print(f"이 컴퓨터는 5초동안 {cnt} 카운트가 진행되었습니다")

if __name__=="__main__":
    main()