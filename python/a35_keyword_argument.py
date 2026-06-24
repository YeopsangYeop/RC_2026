def print_n_times(n, *args, abc = "abc", defg = "defg", **keyargs):
    #positional, default, variable-length, keyword, variable-length-keyword //매개변수 순서
    for i in range(n):
        print(args)
    print(abc, defg)
    print(type(keyargs), keyargs) #dictionary가 찍힌다

def main():
    print_n_times(3, "kim", "sang", "yeop", "is", "student")
    print_n_times(3, "test", defg = "마지막 문자", abc = "첫 문자")

if __name__ == "__main__":
    main()