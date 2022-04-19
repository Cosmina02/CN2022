import copy
import math
import plotly.graph_objects as go
import numpy
import numpy as np


def get_indexes(A):
    maxim = float('-inf')
    n = len(A)
    p = q = 0
    for i in range(0, n):
        for j in range(0, n):
            if abs(A[i][j]) > maxim and i != j:
                maxim, p, q = abs(A[i][j]), i, j
    return p, q


def get_theta(A, p, q):
    alfa = (A[p][p] - A[q][q]) / (2 * A[p][q])
    t = 0
    if alfa >= 0:
        t = -alfa + math.sqrt(pow(alfa, 2) + 1)
    else:
        t = -alfa - math.sqrt(pow(alfa, 2) + 1)
    c = 1 / math.sqrt(1 + pow(t, 2))
    s = t / math.sqrt(1 + pow(t, 2))
    return t, c, s


def rotate(n, p, q, c, s):
    R = [[0 for _ in range(0, n)]] * n
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
    for j in range(0, n):
        if j != p and j != q:
            a[p][j] = c * a[p][j] + s * a[q][j]
            a[q][j] = (-s) * a[j][p] + c * a[q][j]
            a[j][q] = (-s) * a[j][p] + c * a[q][j]
            a[j][p] = a[p][j]
    a[p][p] = a[p][p] + t * a[p][q]
    a[q][q] = a[q][q] - t * a[p][q]
    a[p][q] = 0
    a[q][p] = 0

    return np.array(a)


def computeU(U, p, q, c, s):
    n = len(U)
    u = copy.deepcopy(U)
    for i in range(0, n):
        aux1 = u[i][p]
        u[i][p] = c * u[i][p] + s * u[i][q]
        aux2 = u[i][q]
        u[i][q] = (-s) * aux1 + c * aux2
    return np.array(u)


def jacobi_method(A):
    eps = 10 ** -15
    n = len(A)
    # print(n)
    kmax = 1000
    k = 0
    U = np.identity(n)
    p, q = get_indexes(A)
    # print("p=",p,"\nq=",q)
    t, c, s = get_theta(A, p, q)
    A_init = copy.deepcopy(A)
    evolution=[]
    evolution.append(A_init)

    while abs(A[p][q]) > eps and k < kmax:
        # R = rotate(len(A), p, q, c, s)
        A = computeA(A, t, c, s, p, q)
        evolution.append(A)
        # print("pas ",k,'\nA = ',A,'\nA_init = ', A_init)
        U = computeU(U, p, q, c, s)
        p, q = get_indexes(A)
        # print("p=", p, "\nq=", q)

        if abs(A[p][q]) > eps:
            t, c, s = get_theta(A, p, q)
        k += 1
    plot_matrix_evolution(evolution,"Jacobi algorithm matrix evolution")
    return np.array(A), np.array(U)


def eigen_sum(m1, m2):
    our_eigenvalues = m1.diagonal()
    library_eigenvalues = numpy.linalg.eigvals(np.array(m2))

    suma = 0
    for k in range(len(library_eigenvalues)):
        min = float('+inf')
        for i in range(len(our_eigenvalues)):
            if abs(our_eigenvalues[i] - library_eigenvalues[k]) < min:
                min = abs(our_eigenvalues[i] - library_eigenvalues[k])
        suma += min
    return suma


def pseudo_inversa(A):
    A = np.array(A)
    A_J = numpy.linalg.inv(A.transpose() @ A) @ A.transpose()
    print("A_J =", A_J)
    return A_J


def SVD(A):
    U, S, Vt = numpy.linalg.svd(np.array(A))
    valori_singulare = [i for i in S if i >= 0]
    valori_singulare_nenule = [i for i in S if i > 0]
    r = len(valori_singulare_nenule)

    maxim = max(valori_singulare)
    minim = min(valori_singulare_nenule)
    nr_conditionare_A = maxim / minim
    print(nr_conditionare_A)

    SI = np.zeros((len(A[0]), len(A)))

    for i in range(len(valori_singulare_nenule)):
        SI[i][i] = 1 / valori_singulare_nenule[i]

    PI_A = np.dot(np.dot(Vt.transpose(), SI), U.transpose())
    print(PI_A)

    A_J = pseudo_inversa(A)
    norma = np.linalg.norm(PI_A - A_J)
    print(norma)


def plot_matrix_evolution(evo, title):
    window_length = 1
    fig = go.Figure()
    for step in range(len(evo)):
        fig.add_trace(go.Heatmap(z=evo[step][::-1],colorscale="RdBu",zmid=0))
    fig.data[0].visible = True
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  {"title": title},
                  ],
            label=str(window_length * i))
        step["args"][0]["visible"][i] = True
        steps.append(step)

    sliders = [dict(
        active=0,
        pad={"t": 5},
        steps=steps
    )]

    fig.update_layout(sliders=sliders)

    fig.show()

if __name__ == '__main__':
    A = [[0, 0, 1], [0, 0, 1], [1, 1, 1]]
    A_final, U_final = jacobi_method(A)

    # print(A_final, '\n\n', U_final)
    eigenvalues = eigen_sum(A_final, A)

    # print(eigenvalues)

    A2 = [[0, 0, 1, 2], [0, 0, 1, 2], [1, 1, 3, 2]]
    A2 = [[2, 0], [1, 2], [0, 1]]
    SVD(A2)
