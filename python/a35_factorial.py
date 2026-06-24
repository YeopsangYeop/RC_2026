from functools import lru_cache

def rec_fac(n: int) -> int:
    if n == 1:
        return 1
    else:
        return n * rec_fac(n-1)
    
def for_fac(n):
    out = 1
    for i in range(n):
        out *= i+1
    return out

@lru_cache(maxsize=None) #캐시메모리?
def fibonacci(n):
    if n in dictidnary[n]:
        return dictidnary[n]
    else:
        out = fibonacci(n-1) + fibonacci(n-2)
        dictidnary[n] = out
        return out
    
dictidnary = {1: 1, 2: 1}

def main():
    print(rec_fac(5))
    print(for_fac(5))
    print(fibonacci(4))

if __name__ == "__main__":
    main()