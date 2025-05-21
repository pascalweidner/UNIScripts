import random
from fractions import Fraction


def generate_complex():
    real = random.randint(-10, 10)
    imag = random.randint(-10, 10)
    return complex(real, imag)


def generate_addition():
    a = generate_complex()
    b = generate_complex()
    question = f"({a}) + ({b})"
    answer = a + b
    return question, answer


def generate_subtraction():
    a = generate_complex()
    b = generate_complex()
    question = f"({a}) - ({b})"
    answer = a - b
    return question, answer


def generate_multiplication():
    a = generate_complex()
    b = generate_complex()
    question = f"({a}) * ({b})"
    answer = a * b
    return question, answer


def complex_to_fraction(c):
    real_frac = Fraction(c.real).limit_denominator()
    imag_frac = Fraction(c.imag).limit_denominator()

    if imag_frac == 0:
        return f"{real_frac}"
    if real_frac == 0:
        return f"({imag_frac}j)"

    sign = '+' if imag_frac >= 0 else ''
    return f"({real_frac}{sign}{imag_frac}j)"


def generate_division():
    a = generate_complex()
    b = generate_complex()
    question = f"({a}) / ({b})"
    answer = a / b
    answer_frac = complex_to_fraction(answer)
    return question, answer_frac


def generate_conjugation():
    a = generate_complex()
    question = f"conj({a})"
    answer = a.conjugate()
    return question, answer


def generate_task():
    operations = [
        generate_addition,
        generate_subtraction,
        generate_division,
        generate_multiplication,
        generate_conjugation
    ]

    question, answer = operations[random.randint(0, len(operations) - 1)]()

    print(question)
    input()
    print(answer)


def train():
    while True:
        print("==========New task=========")
        generate_task()
        if input() == "q":
            break


def main():
    train()


if __name__ == "__main__":
    main()
