import copy

import numpy as np


def get_indexes(A):
    maxim = -1
    n = len(A)
    p = q = 0
    for i in range(0, n):
        for j in range(0, n):
            if abs(A[i][j]) > maxim and i != j:
                maxim, p, q = abs(A[i][j]), i, j
    return p, q


def get_theta(A, p, q):
    alfa = (A[p][p] - A[q][q]) / 2 * A[p][q]
    if alfa >= 0:
        t = -alfa + np.sqrt(alfa ** 2 + 1)
    else:
        t = -alfa - np.sqrt(alfa ** 2 + 1)
    c = 1 / np.sqrt(1 + t ** 2)
    s = t / np.sqrt(1 + t ** 2)
    return t, c, s


def rotate(n, p, q, c, s):
    R = [[0 for _ in range(0, n)]]*n
    for i in range(0, n):
        for j in range(0, n):
            if i == j and i != p and i != q:
                R[i][j] = 1
            elif i == j and (i == p or i == q):
                R[i][j] = c
            elif i == p and j == q:
                R[i][j] = s
            elif i == q and j == p:
                R[i][j] = -s
            else:
                R[i][j] = 0
    return np.array(R)


def check_matrix(A):
    n = len(A)
    for i in range(0, n):
        for j in range(0, n):
            if i != j and A[i][j] != 0:
                return False
    return True
def computeA(A, t, c, s, p, q):
    n = len(A)
    a = copy.deepcopy(A)
    for j in range(0,n):
        if j!=p and j!=q:
            a[p][j] = c * a[p][j] + s*a[q][j]
            a[q][j] = (-s)*a[j][p] + c* a[q][j]
            a[j][q] = (-s) * a[j][p] + c * a[q][j]
            a[j][p] = a[p][j]
    a[p][p] += t*a[p][q]
    a[q][q] -= t*a[p][q]
    a[p][q] = 0
    a[q][p] = 0

    return a


def computeU(p,q,c,s,U):
    n = len(U)
    u = copy.deepcopy(U)
    for i in range(0, n):
        aux = u[i][p]
        u[i][p] = c* u[i][p] + s* u[i][q]
        u[i][q] = (-s)*aux + c*u[i][q]
    return u

def jacobi_method(A):
    n = len(A)
    print(n)
    kmax = 1000
    k = 0
    U = np.identity(n)
    p, q = get_indexes(A)
    t, c, s = get_theta(A, p, q)
    A_init = copy.deepcopy(A)

    while not check_matrix(A) and k<kmax:
        R=rotate(len(A),p,q,c,s)
        A = computeA(A,t, c, s,p, q)
        # print("pas ",k,'\nA = ',A,'\nA_init = ', A_init)
        U = computeU(p,q,c,s,U)
        p, q = get_indexes(A)
        t, c, s = get_theta(A, p, q)
        k+=1
    return A,U

if __name__ == '__main__':
    A = [[0,0,1],[0,0,1],[1,1,1]]
    A_final, U_final= jacobi_method(A)

    # print(A_final,'\n',U_final)
