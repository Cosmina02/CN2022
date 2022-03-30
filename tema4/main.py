import copy
import time
import urllib.request
import numpy as np
import plotly.express as px
global eps


class RareMatrix:

    def __init__(self, n=None, rare_values=None, diagonal=None):
        if rare_values is None and n is None:
            rare_values = {}
            n = 0
        if rare_values is not None and n is not None and diagonal is None:
            diagonal = {}
            for i in range(0, n):
                if i in rare_values[i].keys():
                    diagonal[i] = rare_values[i][i]
        self.d = diagonal
        self.rare_values = rare_values
        self.n = n

    @classmethod
    def from_url(self, url):
        dictionary1 = {}
        index = -1
        dictionary2 = {}
        diagonal = {}
        for line in urllib.request.urlopen(url):
            line = line.decode('utf-8')
            if line.find(",") != -1:
                splitter = line.split(',')
                valoare = float(splitter[0])
                i = int(splitter[1])
                j = int(splitter[2])
                if i == j:
                    diagonal[i] = valoare
                if index == -1:
                    index = i
                elif index != i or index == n - 1:
                    dictionary1[index] = dictionary2
                    dictionary2 = {}
                    index = i
                if i in dictionary1.keys():
                    dictionary2 = dictionary1[i]
                if j in dictionary2.keys():
                    dictionary2[j] += valoare
                else:
                    dictionary2[j] = valoare
                dictionary2[j] = valoare
            else:
                if line[:-2] != '':
                    n = int(line)
        return RareMatrix(n, dictionary1, diagonal)


class ColumnVector:
    def __init__(self, n=None, values=None):
        if values is None and n is None:
            values = {}
            n = 0
        self.values = values
        self.n = n

    @classmethod
    def from_url(self, url):
        elements = []
        for line in urllib.request.urlopen(url):
            line = line.decode('utf-8')
            if line == '\r\n':
                break
            else:
                elements.append(float(line))
        return ColumnVector(len(elements), elements)


class LinearSystem:
    def __init__(self, a: RareMatrix, b: ColumnVector):
        self.a = a
        self.b = b

    def null_diagonal(self, a: RareMatrix):
        for i in range(0, a.n):
            if abs(a.d[i]) < eps:
                print("i=", i)
                return False
        return True

    def solve_jacobi(self):
        if not self.null_diagonal(self.a):
            print("The matrix is not valid,it has null elements on the diagonal")
        else:
            x_c = np.zeros(self.a.n)
            x_p = np.zeros(self.a.n)
            deltas=list()
            kmax = 10000
            k = 0
            xs=list()
            values = [0 for _ in range(0, self.a.n)]
            while True:
                x_p = copy.deepcopy(x_c)
                for i in range(0, self.a.n):
                    suma1 = 0
                    suma2 = 0
                    for j in self.a.rare_values[i].keys():
                        if j != i:
                            suma1 += self.a.rare_values[i][j] * x_p[j]
                    if k == 0:
                        val = []
                        for j in range(i + 1, self.a.n):
                            if i in self.a.rare_values[j].keys():
                                tup = (j, self.a.rare_values[j][i])
                                val.append(tup)
                                suma2 += self.a.rare_values[j][i] * x_p[j]
                        values[i] = val
                    else:
                        for val in values[i]:
                            suma2 += val[1] * x_p[val[0]]

                    x_i = (self.b.values[i] - suma1 - suma2) / self.a.d[i]
                    x_c[i] = x_i
                delta = np.linalg.norm(x_c - x_p)
                deltas.append(delta)
                xs.append(x_c)
                k += 1
                # print("k= ", k - 1, "x_p= ", x_p, "\nx_c= ", x_c)
                if delta >= eps and delta <= 10 ** 8 and k <= kmax:
                    continue
                else:
                    # print("k= ", k)
                    break
            if delta < eps:
                return x_c, deltas, k, xs
            else:
                return "Divergenta"

import plotly.graph_objs as go

def plot_matrix_evolution(evo, title):
    window_length = 1
    fig = go.Figure()
    # for step in range(len(evo)):
    #     fig.add_trace(px.histrogram(z=evo[step][::-1],colorscale="RdBu",zmid=0))
    fig = px.histogram(evo)
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
    eps = 10 ** (-15)
    # url = "https://profs.info.uaic.ro/~ancai/CN/lab/4/b_1.txt"
    # b = ColumnVector.from_url(url)
    a = RareMatrix(5, {
        0: {0: 102.5},
        1: {1: 104.88},
        2: {0: 2.5, 1: 1.05, 2: 100.0},
        3: {3: 101.3},
        4: {0: 0.73, 1: 0.33, 3: 1.5, 4: 102.23}
    })
    b = ColumnVector(5, [6.0, 7.0, 8.0, 9.0, 1.0])
    c = RareMatrix.from_url("http://profs.info.uaic.ro/~ancai/CN/lab/4/a_3.txt")
    d = ColumnVector.from_url("http://profs.info.uaic.ro/~ancai/CN/lab/4/b_3.txt")
    # ls = LinearSystem(a, b)
    start = time.time()
    ls = LinearSystem(c, d)
    # print(c.n)
    # print(c.rare_values[54320])
    x,deltas,k,xs=ls.solve_jacobi()
    # end = time.time()
    # temp = end - start
    # # print(temp)
    # hours = temp // 3600
    # temp = temp - 3600 * hours
    # minutes = temp // 60
    # seconds = temp - 60 * minutes
    # print("Execution time: '%d:%d:%d'" % (hours, minutes, seconds))
    plot_matrix_evolution(xs,"XS-uri")
