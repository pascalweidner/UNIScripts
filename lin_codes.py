import random


def generate_random_data():
    return [random.randint(0, 1) for _ in range(4)]


def hamming74_encode(data):
    if len(data) != 4:
        raise ValueError("Only 4 bit data")

    d1, d2, d3, d4 = data

    p1 = d1 ^ d2 ^ d3
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d3

    return [d1, d2, d3, d4, p1, p2, p3]


def introduce_error(codeword, error_probability=0.8):
    if random.random() < error_probability:
        pos = random.randint(0, 6)
        codeword[pos] ^= 1

    return codeword


def training_round():
    print("===========New word============")
    data = generate_random_data()
    encoded = hamming74_encode(data)
    transmitted = introduce_error(encoded[:])
    print("c'=" + str(transmitted))

    if input() == "q":
        exit(0)

    print("c=" + str(encoded))
    print("x=" + str(data))
    input()


def main():
    while True:
        training_round()


if __name__ == "__main__":
    main()




