def main():
    A = [1, 2, 3]
    B = [4, 5, 6]
    print(A + B)
    print(A)
    A.extend(B)
    print(A)

    B.append(7)
    B.append(8)
    print(B)
    B.insert(1, 4.5)
    print(B)

if __name__ == "__main__":
    main()