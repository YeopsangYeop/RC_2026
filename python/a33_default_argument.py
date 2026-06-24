def print_n_times(value, n = 2, *sum):
    sum_ = 0

    for i in range(n):
        print(value)

    for i in sum:
        sum_ += i

    return sum_

def main():
    print(print_n_times("안녕하세요", 5, 10))
    

if __name__ == "__main__":
    main()