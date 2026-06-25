import math

class Circle:
    def __init__(self, radius):
        self.__radius = radius

    def get_circumference(self):
        return 2*math.pi*self.__radius
    
    def get_area(self):
        return math.pi * (self.__radius) ** 2

    @property
    def radius(self):
        return self.__radius
    
    @radius.setter
    def radius(self, value):
        self.__radius = value

class Rectangle(Circle):
    def __init__(self, radius):
        super().__init__(5)
        self.__radius = radius

def main():
    c = Circle(5)
    r = Rectangle(6)
    print(r.__dict__)
    #__변수는 overriding을 방지하는 맹글링 기능이다 private

    print(f"원의 둘레: {c.get_circumference()}, 원의 넓이: {c.get_area()}")

    print(c.radius)
    c.radius = 10
    print(c.radius) 

if __name__ == "__main__":
    main()