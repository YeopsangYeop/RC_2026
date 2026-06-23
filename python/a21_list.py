import datetime

def main():
    list_a = []
    list_b = list()

    print(type(list_a))
    print(type(list_b))

    ptime = datetime.datetime.now()
    list_a = [1,2,3.3,"kim",ptime, True]

    for i in list_a:
        print(i, type(i))

    list_a[1] = 100
    print(list_a[1])

    list_c = [[1, 2, 3],[4, 5, 6],[7, 8, 9]]
    print(list_c[1][1])

if __name__ == "__main__":
    main()