import numpy as np


def substitution_method(A, b, n):
    if A[0][0] == 0:
        raise ValueError("The matrix is singular")
    else:
        x = list(0 for j in range(0, n))
        x[n - 1] = b[n - 1] / A[n - 1][n - 1]
        for i in range(n - 2, -1, -1):
            suma = 0
            for j in range(i + 1, n):
                suma = suma + A[i][j] * x[j]
            v = b[i] - suma
            x[i] = v / A[i][i]

        return x


def search_pivot(matrix, column, n):
    max = 0
    index = 0
    for i in range(column, n):
        if max < abs(matrix[i][column]):
            max = abs(matrix[i][column])
            index = i
    return index


def interschimba_linii(A, b, l, index):
    A[[l, index]] = A[[index, l]]
    aux = b[index]
    b[index] = b[l]
    b[l] = aux
    return A, b


def gauss_algorithm(A, b, n):
    l = 0
    index = search_pivot(A, l, n)
    A, b = interschimba_linii(A, b, l, index)
    b_prim = b
    a_prim = A
    eps = 10 ** (-6)
    while l < n - 1 and abs(a_prim[l][l]) > eps:
        for i in range(l + 1, n):
            f = a_prim[i][l] / a_prim[l][l]
            for j in range(l + 1, n):
                a_prim[i][j] = a_prim[i][j] - f * a_prim[l][j]
            b_prim[i] = b_prim[i] - f * b_prim[l]
            a_prim[i][l] = 0
        l += 1
        index = search_pivot(a_prim, l, n)
        a_prim, b_prim = interschimba_linii(a_prim, b_prim, l, index)
        # print("A = ", A)

    if A[l][l] == 0:
        print("matrice singulara")
    else:
        x = substitution_method(a_prim, b_prim, n)
        diff = a_prim @ x - b_prim
        for o in diff:
            if int(o) != 0:
                print("Solutie gresita")
            else:
                return a_prim, b_prim


def get_column(matrix, i):
    return [row[i] for row in matrix]


def get_inv(A):
    n = len(A[0])
    I = np.eye(n)
    eps = 10 ** (-6)
    aug_A = np.c_[A, I]

    l = 0
    pivot = search_pivot(aug_A, l, n)
    if pivot != l:
        aug_A[[l, pivot]] = aug_A[[pivot, l]]
    while l < n - 1 and abs(aug_A[l][l] > eps):
        for i in range(l + 1, n):
            aug_A[i][l] = aug_A[i][l] / aug_A[l][l]
            for j in range(l + 1, 2 * n):
                aug_A[i][j] = aug_A[i][j] - aug_A[i][l] * aug_A[l][j]
        l = l + 1
        pivot = search_pivot(aug_A, l, n)
        if pivot != l:
            aug_A[[l, pivot]] = aug_A[[pivot, l]]

    R = np.zeros((n, n))
    I_t = np.zeros((n, n))
    for i in range(0, n):
        R[i] = aug_A[i][:n]
    for i in range(0, n):
        I_t[i] = aug_A[i][n:]

    inversa = np.zeros((n , n))
    # print("inversa: ",inversa)
    for i in range(n):
        b = get_column(I_t, i)
        a_res, b_res = gauss_algorithm(R, b, n)
        x = substitution_method(a_res, b_res, n)
        print("x= ",x)
        for j in range(n):
            inversa[j][i] = x[j]
    # print(inversa)
    # print("op: ", inversa @ A)
    return inversa


if __name__ == '__main__':
    n = 3
    A = np.random.randint(low=1, high=100, size=n * n).reshape(n, n)
    # A = np.triu(A)
    b = np.random.randint(low=1, high=100, size=n)
    print("A = ", A)
    # print("b =", b)
    # x = substitution_method(A, b, n)
    #
    # diff = A @ x - b
    # for i , o in enumerate(diff):
    #     diff[i] = int(o)

    # print("diff= ", diff)

    # gauss_algorithm(A, b, n)
    get_inv(A)
    # print("operatia curului; ",inversa @ A)
