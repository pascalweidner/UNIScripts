import numpy as np
from random import randint


def generate_matrices():
    case = randint(0, 100)

    # for a 5% chance an unsolvable task is created
    if case < 5:
        m = randint(2, 6)
        n = randint(2, 6)
        k = randint(2, 6)

        # makes sure that the dimensions differ
        while n == k:
            k = randint(2, 6)

        l = randint(2, 6)
        A1 = np.random.randint(-5, 5, size=(m, n))
        A2 = np.random.randint(-5, 5, size=(k, l))
    else:
        m = randint(2, 6)
        n = randint(2, 6)
        k = randint(2, 6)
        A1 = np.random.randint(-5, 5, size=(m, n))
        A2 = np.random.randint(-5, 5, size=(n, k))

    return A1, A2


def generate_tasks():
    while True:
        A1, A2 = generate_matrices()
        print("=============New task===============")
        print(A1)
        print()
        print(A2)
        input()
        print("=============Solution===============")
        print(A1 @ A2)
        q = input()
        if q == "q":
            break


def main():
    generate_tasks()


if __name__ == "__main__":
    main()
