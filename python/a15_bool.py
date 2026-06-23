def main():
    print(10 == 20)
    print(10 != 20)
    print(10 < 100)
    print(100 >= 100)
    print(type(True)) #type of True is bool class
    print(type(False))

    print(not False)
    print(True and False)
    print(True or False)

    a = int(input("Enter a number: "))
    if(a > 100):
        print("a is greater than 100", type(a))
    print("a is less than or equal to 100", type(a))

if __name__ == "__main__":
    main()