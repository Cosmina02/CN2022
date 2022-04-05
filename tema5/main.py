import copy

import numpy as np


def get_indexes(A):
    maxim = 0
    n = len(A)
    p = q = 0
    for i in range(2, n):
        for j in range(1, i):
            if abs(A[i][j]) > maxim:
                maxim, p, q = abs(A[i][j]), i, j
    return p, q


def get_theta(A, p, q):
    alfa = (A[p][p] - A[q][q]) / 2 * A[p][q]
    if alfa >= 0:
        t = -alfa + np.sqrt(alfa ** 2 + 1)
    else:
        t = -alfa + np.sqrt(alfa ** 2 + 1)
    c = 1 / np.sqrt(1 + t ** 2)
    s = t / np.sqrt(1 + t ** 2)
    return t, c, s

def rotate(n,p,q,c,s):
    pass

def check_matrix(A):
    n = len(A)
    for i in range(0, n):
        for j in range(0, n):
            if i != j and A[i][j] != 0:
                return False
    return True


def jacobi_method(A):
    n = len(A)
    kmax = 10000
    k = 0
    U = np.identity(n)
    p, q = get_indexes(A)
    t, c, s = get_theta(A, p, q)
    A_init = copy.deepcopy(A)
