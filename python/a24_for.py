def main():
    print(range(10))

    a = []
    for i in range(10):
        a.append(i+1)
    print(a)

    b = ["a", "b","c","d","e","f"]
    for ele in b: 
        print(ele + "원소")

    #list comprehension
    c =[i for i in range(100)]
    print(c)

    d = ["에이", "비", "씨", "디", "이", "에프"]
    for i in range(6):
        print(b[i], d[i])
    
    #pythonic, pydantic
    for b, d in zip(b, d):
        print(b, d)

if __name__ == "__main__":
    main()