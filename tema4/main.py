import copy
import time
import urllib.request
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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

    @classmethod
    def from_url(self, url_a, url_b):
        a = RareMatrix.from_url(url_a)
        b = ColumnVector.from_url(url_b)
        return LinearSystem(a, b)

    def null_diagonal(self, a: RareMatrix):
        for i in range(0, a.n):
            if abs(a.d[i]) < eps:
                print("i=", i)
                return False
        return True

    def solve_jacobi(self):
        eps = 10 ** (-15)
        if not self.null_diagonal(self.a):
            print("The matrix is not valid,it has null elements on the diagonal")
        else:
            x_c = np.zeros(self.a.n)
            x_p = np.zeros(self.a.n)
            deltas = list()
            kmax = 10000
            k = 0
            xs = list()
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
                print("k= ", k - 1, "x_p= ", x_p, "\nx_c= ", x_c)
                if delta >= eps and delta <= 10 ** 8 and k <= kmax:
                    continue
                else:
                    # print("k= ", k)
                    break
            if delta < eps:
                return x_c, deltas, k, xs
            else:
                return "Divergenta",deltas,k,xs


def plot_report(x, deltas, k, xs):
    # if x == "Divergenta":
    #     return "Divergenta"
    x1 = [i for i in range(0, k)]
    y = deltas
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("delta_x evolution over iterations", "x distribution")
    )
    fig.add_trace(go.Scatter(x=x1, y=y), row=1, col=1)

    fig.update_xaxes(title_text="iteration", row=1, col=1)
    fig.update_yaxes(title_text="delta_x", row=2, col=1)

    window_length = 1
    for step in range(len(xs)):
        fig.add_trace(go.Histogram(x=xs[step],xbins=dict(
        start=-10000,
        end=55000,
        size=100
    )), row=2, col=1)
    fig.data[0].visible = True
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}, ],
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
    ls = LinearSystem.from_url(
        "http://profs.info.uaic.ro/~ancai/CN/lab/4/a_1.txt",
        "http://profs.info.uaic.ro/~ancai/CN/lab/4/b_1.txt"
    )
    print(f"Dimensiunea sistemului este {ls.a.n}")
    start = time.time()
    x, deltas, k, xs = ls.solve_jacobi()
    plot_report(x, deltas, k, xs)

    end = time.time()
    temp = end - start
    hours = temp // 3600
    temp = temp - 3600 * hours
    minutes = temp // 60
    seconds = temp - 60 * minutes
    print("Execution time: '%d:%d:%d'" % (hours, minutes, seconds))

    # ls = LinearSystem.from_url(
    #     "http://profs.info.uaic.ro/~ancai/CN/lab/4/a_2.txt",
    #     "http://profs.info.uaic.ro/~ancai/CN/lab/4/b_2.txt"
    # )
    # print(f"Dimensiunea sistemului este {ls.a.n}")
    # x, deltas, k, xs = ls.solve_jacobi()
    # print("Gata")
    # plot_report(x, deltas, k, xs)

    # ls = LinearSystem.from_url(
    #     "http://profs.info.uaic.ro/~ancai/CN/lab/4/a_3.txt",
    #     "http://profs.info.uaic.ro/~ancai/CN/lab/4/b_3.txt"
    # )
    # print(f"Dimensiunea sistemului este {ls.a.n}")
    # x, deltas, k, xs = ls.solve_jacobi()
    # plot_report(x, deltas, k, xs)
    #
    # ls = LinearSystem.from_url(
    #     "http://profs.info.uaic.ro/~ancai/CN/lab/4/a_4.txt",
    #     "http://profs.info.uaic.ro/~ancai/CN/lab/4/b_4.txt"
    # )
    # print(f"Dimensiunea sistemului este {ls.a.n}")
    # x, deltas, k, xs = ls.solve_jacobi()
    # plot_report(x, deltas, k, xs)

    # ls = LinearSystem.from_url(
    #     "http://profs.info.uaic.ro/~ancai/CN/lab/4/a_5.txt",
    #     "http://profs.info.uaic.ro/~ancai/CN/lab/4/b_5.txt"
    # )
    # print(f"Dimensiunea sistemului este {ls.a.n}")
    # x, deltas, k, xs = ls.solve_jacobi()
    # plot_report(x, deltas, k, xs)
    # print(x)
