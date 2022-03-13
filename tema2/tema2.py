import numpy as np


def substitution_method(A, b, n):
    if A[0][0] == 0:
        raise ValueError("The matrix is singular")
    else:
        x = list(0 for j in range(0, n))
        x[n-1] = b[n-1]/A[n-1][n-1]
        for i in range(n-2, -1, -1):
            suma = 0
            for j in range(i+1, n):
                suma = suma + A[i][j]*x[j]
            v = b[i]-suma
            x[i] = v/A[i][i]

        return x


if __name__ == '__main__':
    n = 5
    A = np.random.randint(low=1, high=100, size=n * n).reshape(n, n)
    A = np.triu(A)
    b = np.random.randint(low=1, high=100, size=n)
    print("A= ",A)
    print("b=",b)
    x = substitution_method(A, b, n)

    diff = A @ x - b
    print("diff= ", diff)
