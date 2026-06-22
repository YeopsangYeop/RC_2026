class A_test:
    def __repr__(self):
        return "A_test class instance"
    
class B_test:
    pass

def main():
    print(12345)
    print(123, "kim", "sang", "yeop")
    print(3.1415)
    
    print("this", "is", "a", "string", sep = "_", end = " ")
    print("this", "is", "a", "string", sep = "-")

    a = A_test()
    print(a)
    b = B_test()
    print(b)

if __name__ == "__main__":
    main()