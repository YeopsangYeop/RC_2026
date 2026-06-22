def main():
    str1 = "abc"
    str2 = "this is format test: {}".format(10) #중괄호 안에 10이 들어감
    print(str1)
    print(str2)

    str3 = "this is format test: {2}, {1}, {0}".format(10, 20, 30) #중괄호 안의 숫자는 format 함수의 인덱스 번호로, 0부터 시작. 2는 30 1은 20, 0은 10이 들어감
    print(str3)
    
    str4 = "this is format test: {2:d}, {1:5d}, {0:05d}".format(10, 20, 30) #d는 정수형, 5d는 5자리의 정수형, 05d는 5자리의 정수형인데 빈칸을 0으로 채움. 2는 30 1은 20, 0은 10이 들어감
    print(str4)

    str5 = "this is format test: {2:+.2f}, {1:+5.2f}, {0:+05.2f}".format(10.1263, -20.4213, -30) 
    #f는 실수형, .2f는 소수점 둘째자리까지의 실수형, +는 양수는 +로 음수는 -로 표시, 5.2f는 5자리의 실수형인데 소수점 둘째자리까지 표시, 05.2f는 5자리의 실수형인데 소수점 둘째자리까지 표시하고 빈칸을 0으로 채움. 2는 -30 1은 -20.4213, 0은 10.1263이 들어감
    print(str5)

    str6 = 10.126
    print(f"this is fstring test: {str6:+10.2f}") #fstring은 문자열 앞에 f를 붙여서 사용하는 문자열 포매팅 방법. 중괄호 안에 변수나 표현식을 넣어서 사용할 수 있음. +는 양수는 +로 음수는 -로 표시, 10.2f는 10자리의 실수형인데 소수점 둘째자리까지 표시

if __name__ == "__main__":
    main()