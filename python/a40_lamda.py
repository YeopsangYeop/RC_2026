def power(item):
    return item * item

def under_3(item):
    return item < 3

def main():
    li = [1, 2, 3, 4, 5]
    output = map(power, li)
    print(list(output))

    output = map(lambda x: x * x, li)

    output1 = filter(under_3, li)
    print(list(output1))

    output1 = filter(lambda x: x<3, li)
    print(list(output1))

if __name__ == "__main__":
    main()