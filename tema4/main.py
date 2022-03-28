import urllib.request


class RareMatrix:

    def __init__(self, n=None, rare_values=None):
        if rare_values is None and n is None:
            rare_values = {}
            n = 0
        self.rare_values = rare_values
        self.n = n

    def __add__(self, other):
        # un dict copie cu val din self
        # daca exista cheile in b le adunam,daca nu ramane asa
        # daca exista i in b dar nu si j adaugam la dict de i cheia j din b
        # apoi adaugam i urile din b care nu exista in a
        addition = self.rare_values
        for key_i in addition.keys():
            exists = False
            for key_j in addition[key_i].keys():
                if key_i in other.rare_values.keys():
                    if key_j in other.rare_values[key_i].keys():
                        addition[key_i][key_j] += other.rare_values[key_i][key_j]
                    else:
                        exists = True
            if exists is True:
                values_i = other.rare_values[key_i]
                for some_key in values_i:
                    if some_key not in addition[key_i].keys():
                        addition[key_i][some_key] = values_i[some_key]
        for key_i in other.rare_values.keys():
            if key_i not in addition.keys():
                addition[key_i] = other.rare_values
        return RareMatrix(addition)

    def __eq__(self, other):
        if len(self.rare_values.keys()) == len(other.rare_values.keys()):
            for key_i in self.rare_values.keys():
                if len(self.rare_values[key_i]) == len(other.rare_values[key_i]):
                    for key_j in self.rare_values[key_i].keys():
                        if key_i in other.rare_values.keys():
                            if key_j in other.rare_values[key_i].keys():
                                if self.rare_values[key_i][key_j] != other.rare_values[key_i][key_j]:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    return True
                else:
                    return False
        else:
            return False

    def getColumn(self, col):
        dict = {}
        for i in self.rare_values.keys():
            if col in self.rare_values[i].keys():
                dict[i] = self.rare_values[i][col]
        return dict

    def getTranspusa(self):
        dict = {}
        for i in range(0, self.n):
            temp = self.getColumn(i)
            if temp != {}:
                dict[i] = temp
        return dict

    def __pow__(self, power, modulo=None):
        new_dict = {}
        transpusa = self.getTranspusa()
        for i in self.rare_values.keys():  # itereaza prin cheile i
            print(i)
            element2 = {}
            for col in range(0, self.n):
                s = 0
                for k in range(0, self.n):
                    if k in transpusa[col].keys() and k in self.rare_values[i].keys():
                        s = s + self.rare_values[i][k] * transpusa[col][k]
                if s != 0:
                    element2[col] = s
                    new_dict[i] = element2
        return RareMatrix(new_dict, self.n)

    @classmethod
    def from_url(self, url):
        dictionary1 = {}
        index = -1
        dictionary2 = {}
        for line in urllib.request.urlopen(url):
            line = line.decode('utf-8')
            if line.find(",") != -1:
                splitter = line.split(',')
                valoare = float(splitter[0])
                i = int(splitter[1])
                j = int(splitter[2])
                if index == -1:
                    index = i
                elif index != i:
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
        return RareMatrix(n, dictionary1)


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
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def solve_jacobi(self):
        print("work in progress")

if __name__ == '__main__':
    url = "https://profs.info.uaic.ro/~ancai/CN/lab/4/b_1.txt"
    b = ColumnVector.from_url(url)
