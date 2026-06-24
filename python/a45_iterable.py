from _collections_abc import Iterable

class SimpleeIter:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

def main():
    iter = SimpleeIter(0, 10)
    print(isinstance(iter, Iterable))
    for v in iter:
        print(v)


if __name__ == "__main__":
    main()