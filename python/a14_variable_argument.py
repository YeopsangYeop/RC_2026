import random

def sum_all(*value):
    sum = 0
    print(type(value))
    for i in value:
        sum += i
    
    avr = sum/len(value)
    return sum, avr

def main():
    a = [random.randint(0, 100) for _ in range(100)]
    s, b = sum_all(*a)
    print(f"합계는 {s}, 평균은 {b}")

if __name__ == "__main__":
    main()
