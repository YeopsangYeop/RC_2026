import numpy as np
import random, math

def main():
    x = np.random.randint(0, 10, 10).reshape(2, 5)
    print(x)

    s1 = np.sum(x)
    print(s1)
    s1 = np.mean(x)
    print(s1)
    s1 = np.max(x)
    print(s1)
    s1 = np.min(x)
    print(s1)

    s1 = np.std(x)
    print(s1)
    s1 = np.var(x)
    print(s1)
    s1 = np.cumsum(x)
    print(s1)
    s1 = np.cumprod(x)
    print(s1)

    x = [random.randint(0, 10) for _ in range(10)]
    print(x)
    print(sum(x))
    print(max(x))
    print(min(x))

    s1 = np.sort(x)
    print(s1)
    s1 = np.unique(x)
    print(s1)
    s1 = np.flatten()
    s1 = np.unionidx(x, [1, 2, 3])
    print(s1)
    s1 = np.setdiff1d(x, [1, 2, 3])
    print(s1)

if __name__ == "__main__":
    main()