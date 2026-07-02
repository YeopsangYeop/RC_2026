import numpy as np

def main():
    x = np.arange(4).reshape(2, 2)
    print(x)
    y = np.arange(3, -1, -1).reshape(2, -1)
    print(y)

    re = x > y
    print(re, type(re))

    s1 = np.where(x > y, x, y)
    print(s1)

if __name__ == "__main__":
    main()