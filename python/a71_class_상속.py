class Parent:
    def __init__(self, value):
        self.value = "테스트"
        self.value2 = self.value
        print("Parent 클래스 생성자 호출")

    def test(self):
        print("Parent 클래스의 테스트 메소드")

class Child(Parent):
    def __init__(self):
        Parent.__init__(self, "자식에서 넘어간 값")
        super().__init__("자식에서 넘어간 값")
        print("Child 클래스 생성자 호출")
        self.value3 = "자식 데이터"
        
    def test(self):
        print("child 클래스의 test 메소드 입니다")

def main():
    p = Parent("Frist")
    p.test()
    print(p.value)
    print(p.value2)
    c = Child()
    c.test()
    print(c.value)
    print(c.value2)