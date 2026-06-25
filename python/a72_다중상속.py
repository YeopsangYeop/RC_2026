class Person:
    def __init__(self, value):
        self.b = value

class University:
    def __init__(self, value):
        self.a = value

    def message_credit(self):
        print("인사합니다")

class Undergraduate(Person, University):
    def __init__(self, value):
        Person.__init__(self, 2)
        University.__init__(self, 1)
        self.c = value

def main():
    kim = Undergraduate(3)
    print(kim.a, kim.b, kim.c)
    kim.message_credit()

if __name__ == "__main__":
    main()