# values[x]->valoarea lui x
# values[x][y]->f(x)
import random
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def newton_form(x_values, y_values, x):
    n = len(x_values)
    divided_diff = [[0 for _ in range(n)] for _ in range(n)]
    for row in range(n):
        divided_diff[row][0] = y_values[row]
    for i in range(1, n):
        for j in range(n - i):
            a = divided_diff[j + 1][i - 1] - divided_diff[j][i - 1]
            b = x_values[j + i] - x_values[j]
            divided_diff[j][i] = a / b
    rez = divided_diff[0][0]
    print("div_diff", divided_diff)
    for i in range(1, n):
        rez += get_lagrange_value(x_values, x, i) * divided_diff[0][i]
    return rez


def get_lagrange_value(x_values, x, k):
    t = 1
    for i in range(k):
        t = t * (x - x_values[i])
    return t


def get_lagrange_interpolation(x_values, y_values):
    new_x_values = []
    new_y_values = []
    minim = x_values[0]
    maxim = x_values[len(x_values) - 1]
    print("max=", max)
    for i in np.arange(minim, maxim, 0.1):
        new_x_values.append(i)
        new_y_values.append(newton_form(x_values, y_values, i))
    new_x_values.append(maxim)
    new_y_values.append(newton_form(x_values, y_values, maxim))

    return new_x_values, new_y_values


# f(x) = x^2 - 12x + 30
def generate_input1():
    minim = 1
    maxim = 5
    n = 20
    x_values = []
    x_values.append(minim)
    for i in range(n - 2):
        if minim + 0.2 > maxim:
            x_values.append(random.uniform(minim, maxim))
        else:
            x_values.append(random.uniform(minim, minim + 0.2))
            minim += 0.2
    x_values.append(maxim)
    x_values.sort()
    y_values = []
    for i in x_values:
        val = i * i - 12 * i + 30
        y_values.append(val)
    return x_values, y_values


# f(x) = sin(x) - cos(x)
def generate_input2():
    minim = 0
    maxim = 1.5
    n = 20
    x_values = []
    x_values.append(minim)
    for i in range(n - 2):
        if minim + 0.2 > maxim:
            x_values.append(random.uniform(minim, maxim))
        else:
            x_values.append(random.uniform(minim, minim + 0.2))
            minim += 0.2
    x_values.append(maxim)
    x_values.sort()
    y_values = []
    for i in x_values:
        val = np.sin(i) - np.cos(i)
        y_values.append(val)
    return x_values, y_values


# 2x^3 - 3x + 15
def generate_input3():
    minim = 0
    maxim = 1.5
    n = 20
    x_values = []
    x_values.append(minim)
    for i in range(n - 2):
        if minim + 0.2 > maxim:
            x_values.append(random.uniform(minim, maxim))
        else:
            x_values.append(random.uniform(minim, minim + 0.2))
            minim += 0.2
    x_values.append(maxim)
    x_values.sort()
    y_values = []
    for i in x_values:
        val = 2 * (x ** 3) - 3 * x + 15
        y_values.append(val)
    return x_values, y_values


def get_sum_b(x, p):
    s = 0
    for i in range(0, len(x)):
        s += x[i] ** p
    return s


def get_sum_y(x, y, p):
    s = 0
    for i in range(0, len(x)):
        s += (x[i] ** p) * y[i]
    return s


def least_square_poly_interpolation(x, y, m):
    # se face sistemul ala(prima data cu 1...pana la cat ii dam noi sa fie de mare)
    # apoi rezolvam Ba=f,unde a este necunoscuta
    # apoi dupa ce il avem pe a facem polinomul cu schema horner :)
    n = len(x)

    B = [[0 for i in range(0, m + 1)] for _ in range(0, m + 1)]
    for i in range(0, m + 1):
        for j in range(0, m + 1):
            B[i][j] = get_sum_b(x, i + j)
    B = np.array(B)

    Y = [0 for _ in range(0, m + 1)]
    for i in range(0, m + 1):
        Y[i] = [get_sum_y(x, y, i)]
    Y = np.array(Y)

    B_t = np.transpose(B)
    aux1 = np.dot(B_t, B)
    aux2 = np.dot(B_t, Y)

    res = np.linalg.solve(aux1, aux2)
    res = [i for i in res]
    res.reverse()
    res = [res[i][0] for i in range(len(res))]

    return res


def horner(p, n, x):
    res = 0
    for i in range(0, n):
        res = res * x + p[i]
    return res


def get_lsp_aprox(x, y, p):
    # tre sa facem pt grafic de la p=1 pana la cat ii dam noi si sa calculam pt toate
    # valorilea alea new_x,new_y ca sa facem slider
    p_m = least_square_poly_interpolation(x, y, p)

    new_x = []
    new_y = []
    n = len(x)
    minim = x[0]
    maxim = x[len(x) - 1]

    for i in np.arange(minim, maxim, 0.1):
        new_x.append(i)
        new_y.append(horner(p_m, len(p_m), i))
    new_x.append(maxim)
    new_y.append(horner(p_m, len(p_m), maxim))

    return new_x, new_y


def plot_aprox(x_values, y_values, new_x, new_y,title):
    if "Lagrange" in title:
        title1 = 'lagrange-aprox'
    else:
        title1 = 'lsp-aprox'

    df1 = pd.DataFrame(dict(
        old_x=x_values,
        old_y=y_values,
    ))
    df2 = pd.DataFrame(dict(new_x=new_x,
                            new_y=new_y))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1["old_x"], y=df1["old_y"], name='initial points', mode='markers'))
    fig.add_trace(go.Scatter(x=df1["old_x"], y=df1["old_y"], name="Function", mode="lines"))
    fig.add_trace(go.Scatter(x=df2["new_x"], y=df2["new_y"], name=title1, mode="lines"))
    fig.update_layout(
        title=title
    )

    fig.show()


if __name__ == '__main__':
    x_values, y_values = generate_input1()
    new_x, new_y = get_lagrange_interpolation(x_values, y_values)
    plot_aprox(x_values, y_values, new_x, new_y, 'Lagrange aproximation')
    x, y = get_lsp_aprox(x_values, y_values, 2)
    print("x=", x, "\ny=", y)
    plot_aprox(x_values, y_values, x, y, 'Lsp aprox')
