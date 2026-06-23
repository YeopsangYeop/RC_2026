def main():
    a = {} #{}안에 값을 넣으면 dict가 아닌 set이 된다.
    b = dict()

    #원소 추가
    a["name"] = "kim"
    print(a)
    print(a["name"])

    print(a.pop("name"))
    print(a)

    a["a"] = "a"
    a["b"] = "b"
    a["c"] = "c"
    a["d"] = "d"

    for key in a:
        print(key, a[key])

if __name__ == "__main__":
    main()