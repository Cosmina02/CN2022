import urllib.request
import numpy as np

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
                elif index != i or index == n-1:
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
            if a.d[i] < eps:
                return False
        return True

    def solve_jacobi(self):
        if not self.null_diagonal(self.a):
            print("The matrix is not valid,it has null elements on the diagonal")
        else:
            x = []
            x_c = np.zeros(self.a.n)
            x_p = np.zeros(self.a.n)
            kmax = 10000
            k = 0
            while True:
                x_p = x_c
                for i in range(0, self.a.n):
                    suma1 = 0
                    suma2 = 0
                    for j in range(0, self.a.n):
                        if j < i and j in self.a.rare_values[i].keys():
                            suma1 +=  self.a.rare_values[i][j] * x_p[j]
                        if j > i and j in self.a.rare_values.keys() and i in self.a.rare_values[j].keys():
                            suma2 +=  self.a.rare_values[j][i] * x_p[j]
                    x_i = (self.b.values[i] - suma1 - suma2) / self.a.d[i]
                    x_c[i] = x_i
                delta = np.linalg.norm(x_c - x_p)
                k += 1
                if (delta >= eps or k == 1) and delta <= 10 ** 8 and k <= kmax:
                    continue
                else:
                    print("aici ",delta)
                    print("aici ", delta >= eps)
                    print("aici ", eps)
                    break
            if delta < eps:
                return x_c
            else:
                return "Divergenta"
        # print("work in progress")


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
    c = RareMatrix.from_url("http://profs.info.uaic.ro/~ancai/CN/lab/4/a_1.txt")
    d = ColumnVector.from_url("http://profs.info.uaic.ro/~ancai/CN/lab/4/b_1.txt")
    ls = LinearSystem(c, d)
    # print(c.n)
    # print(c.rare_values[54320])
    print(ls.solve_jacobi())
