from sympy import Matrix, symbols, linsolve
import numpy as np

def generate_infinite_solution_lgs(m, n, max_rank=None):
    """
    Generate an m x n system with infinite solutions and clean integers.
    """
    assert m < n or max_rank is not None, "Use a wide matrix or reduce rank manually."

    while True:
        A_numeric = np.random.randint(-2, 5, size=(m, n))  # Small integers

        # Reduce rank artificially, if needed
        if max_rank is not None:
            U, S, Vt = np.linalg.svd(A_numeric, full_matrices=False)
            S[max_rank:] = 1  # force lower rank
            A_numeric = (U @ np.diag(S) @ Vt).round().astype(int)

        rank = np.linalg.matrix_rank(A_numeric)
        if rank < n:  # not full column rank → infinite solutions possible
            break

    # Choose a clean solution vector with integers
    x_true = np.random.randint(-3, 4, size=(n, 1))

    # Generate a compatible RHS
    b_numeric = A_numeric @ x_true

    A = Matrix(A_numeric)
    b = Matrix(b_numeric)
    x_symbols = symbols(f'x1:{n + 1}')
    solution = linsolve((A, b), x_symbols)

    return A, b, solution, Matrix(x_true)

if __name__ == "__main__":
    A, b, solution, x_true = generate_infinite_solution_lgs(m=3, n=5, max_rank=2)
    print("A =")
    print(A)
    print("\nb =")
    print(b)
    print("\nKnown solution (used to generate b):")
    print(x_true)
    print("\nSymbolic solution:")
    print(solution)
