import random

def main():
    hanguls = list("김이박최전엽")
    hanguls2 = list("가나다라마바사아자차카")
    for _ in range(100):
        name = random.choice(hanguls) + str().join(random.choices(hanguls, k=2))
        print(name)

    mu = 3
    sigma = 5
    print(random.gauss(mu, sigma))
    random.normalvariate(mu, sigma)

if __name__ == "__main__":
    main()