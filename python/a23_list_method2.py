import datetime

def main():
    ptime = datetime.datetime.now()
    a = [0,1,2,3,4,5,6]
    b = ["a", "b", "c", "d", "e", "f", ptime]
    
    del a[0] 
    del b[2]
    print(a)
    print(b)

    del ptime
    for i in b:
        print(type(i), i)

    print(b.pop())
    print(b)

    a.remove(3)
    print(a)

if __name__ == "__main__":
    main()