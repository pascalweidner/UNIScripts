import numpy as np
import sympy as sp
import random
from sympy import Matrix, symbols, linsolve, S


def generate_lgs(m, n, allow_unsolvable=False, force_case=None):
    max_attempts = 50
    attempt = 0

    while attempt < max_attempts:
        attempt += 1

        A_numeric = np.random.randint(-10, 11, size=(m, n))  # generates random matrix

        # forces the matrix to not having 0 rows
        for i in range(m):
            if np.all(A_numeric[i] == 0):
                A_numeric[i, np.random.randint(0, n)] = random.choice([-1, 1]) * np.random.randint(1, 11)

        A = Matrix(A_numeric)

        rank_A = A.rank()

        if force_case == "none":
            b_numeric = np.random.randint(-10, 11, size=(m, 1))
            b = Matrix(b_numeric)

            if m > n:
                if m >= 2:
                    i, j = np.random.choice(range(m), 2, replace=False)
                    factor = np.random.randint(1, 5)
                    for k in range(n):
                        A_numeric[i, k] = factor * A_numeric[j, k]
                    b_numeric[i, 0] = factor * b_numeric[j, 0] + np.random.randint(1, 5)
                    A = Matrix(A_numeric)
                    b = Matrix(b_numeric)

        elif force_case == "unique":
            if n == m:
                while Matrix(A_numeric).rank() < n:
                    A_numeric = np.random.randint(-10, 11, size=(n, n))
                A = Matrix(A_numeric)

                x_numeric = np.random.randint(-5, 6, size=(n, 1))
                b_numeric = A_numeric @ x_numeric
                b = Matrix(b_numeric)
            else:
                x_numeric = np.random.randint(-5, 6, size=(n, 1))
                b_numeric = A_numeric @ x_numeric
                b = Matrix(b_numeric)

        elif force_case == "infinite":
            if m < n:
                x_numeric = np.random.randint(-5, 6, size=(n, 1))
                b_numeric = A_numeric @ x_numeric
                b = Matrix(b_numeric)
            else:
                rank_target = min(m, n) - 1
                if rank_target > 0:
                    for i in range(1, min(m, rank_target + 1)):
                        factor = np.random.randint(1, 5)
                        A_numeric[i] = factor * A_numeric[0]

                    A = Matrix(A_numeric)

                    x_numeric = np.random.randint(-5, 6, size=(n, 1))
                    b_numeric = A_numeric @ x_numeric
                    b = Matrix(b_numeric)
                else:
                    b_numeric = np.zeros((m, 1))
                    b = Matrix(b_numeric)
        else:
            b_numeric = np.random.randint(-10, 11, size=(m, 1))

        A = Matrix(A_numeric)
        b = Matrix(b_numeric)

        augmented = A.row_join(b)
        rref, pivots = augmented.rref()

        rank_A = A.rank()
        rank_augmented = augmented.rank()
        if rank_A < rank_augmented:
            case = "none"  # Keine Lösung
        elif rank_A == rank_augmented:
            if rank_A == n:
                case = "unique"
            else:
                case = "infinite"
        else:
            case = "unknown"

        if force_case is not None and case != force_case:
            continue

        if not allow_unsolvable and case == "none":
            continue

        x_symbols = symbols(f'x1:{n + 1}')
        solution = linsolve((A, b), x_symbols)

        formatted_solution = format_solution(solution, x_symbols, case)

        return A, b, formatted_solution, case

    # Falls wir nach max_attempts noch keine passende Lösung gefunden haben
    raise ValueError(f"Konnte kein passendes LGS erzeugen nach {max_attempts} Versuchen.")


def format_solution(solution, x_symbols, case):
    if case == "none":
        return "Keine Lösung"

    elif case == "unique":
        solution_list = list(solution)[0]
        return {x_symbols[i]: solution_list[i] for i in range(len(x_symbols))}

    elif case == "infinite":
        if len(solution) == 0:
            return "Leere Lösungsmenge"

        free_vars = []
        solution_form = {}

        if isinstance(solution, sp.sets.sets.FiniteSet):
            return {x_symbols[i]: list(solution)[0][i] for i in range(len(x_symbols))}
        else:
            free_symbols = list(solution.free_symbols)

            for i, var in enumerate(x_symbols):
                if var in free_symbols:
                    free_vars.append(var)
                    solution_form[var] = var  # Freie Variable
                else:
                    try:
                        expr = solution.subs([(s, 0) for s in free_symbols if s != var])
                        for sym in free_symbols:
                            if sym != var:
                                coeff = solution.diff(sym)
                                if coeff != 0:
                                    expr += coeff * sym
                        solution_form[var] = expr
                    except:
                        solution_form[var] = "Komplexer Ausdruck"

        return {
            "freie_variablen": free_vars,
            "loesung": solution_form
        }

    return "Unbekannter Fall"


def display_lgs(A, b, solution, case):
    print("Lineares Gleichungssystem (A|b):")
    augmented = A.row_join(b)
    print(augmented)
    input()
    print("\nFall:", case)


    if case == "none":
        print("Keine Lösung vorhanden.")
    elif case == "unique":
        print("\nEindeutige Lösung:")
        for var, val in solution.items():
            print(f"{var} = {val}")
    elif case == "infinite":
        print("\nUnendlich viele Lösungen:")
        if isinstance(solution, dict) and "freie_variablen" in solution:
            print("Freie Variablen:", ", ".join(str(var) for var in solution["freie_variablen"]))
            print("Lösungsform:")
            for var, expr in solution["loesung"].items():
                print(f"{var} = {expr}")
        else:
            for var in solution:
                print(f"{var} = {solution[var]}")

    print("\n" + "-" * 50 + "\n")


def generate_lgs_exercise(m, n, allow_unsolvable=False, force_case=None):
    """Generiert ein LGS-Übungsproblem."""
    A, b, solution, case = generate_lgs(m, n, allow_unsolvable, force_case)

    print(f"Übungsaufgabe: Löse das folgende LGS mit {m} Gleichungen und {n} Unbekannten:")
    display_lgs(A, b, solution, case)

    return A, b, solution, case


if __name__ == "__main__":
    print("LGS-Generator und -Löser\n")

    while True:
        print("\nInteraktiver Modus (Eingabe von 'q' zum Beenden)")
        user_input = input("Anzahl der Gleichungen (m): ")
        if user_input.lower() == 'q':
            break
        m = int(user_input)

        user_input = input("Anzahl der Unbekannten (n): ")
        if user_input.lower() == 'q':
            break
        n = int(user_input)

        force_case_input = input("Fall erzwingen (none/unique/infinite/random): ")
        if force_case_input.lower() == 'q':
            break

        force_case = None if force_case_input.lower() == 'random' else force_case_input.lower()
        allow_unsolvable = force_case == "none" or input("Unlösbare Systeme zulassen? (j/n): ").lower() == 'j'

        try:
            generate_lgs_exercise(m, n, allow_unsolvable, force_case)
        except ValueError as e:
            print(f"Fehler: {e}")
