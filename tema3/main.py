import urllib.request  # the lib that handles the url stuff


class RareMatrix:

    def __init__(self, rare_values=None, n=None):
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
        for key_i in self.rare_values.keys():
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

    def __pow__(self, power, modulo=None):
        new_dict = {}
        for i in self.rare_values.keys():
            print(i)
            element2={}
            for col in range(0, self.n):
                s = 0
                for j in self.rare_values.keys():
                    if col in self.rare_values[j] and col in self.rare_values[i].keys() and i in self.rare_values[col].keys():
                        s += self.rare_values[i][col] * self.rare_values[col][i]
                element2[col] = s
            new_dict[i]=element2
        return RareMatrix(new_dict,self.n)

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
                    print(n)

        return RareMatrix(dictionary1, n)


if __name__ == '__main__':
    urls = {
        "a": "https://profs.info.uaic.ro/~ancai/CN/lab/3/a.txt",
        "b": "https://profs.info.uaic.ro/~ancai/CN/lab/3/b.txt",
        "a_plus_b": "https://profs.info.uaic.ro/~ancai/CN/lab/3/a_plus_b.txt",
        "a_ori_a": "https://profs.info.uaic.ro/~ancai/CN/lab/3/a_ori_a.txt"
    }
    a = RareMatrix.from_url(urls["a"])
    # b = RareMatrix.from_url(urls["b"])
    # a_plus_b = RareMatrix.from_url(urls["a_plus_b"])
    a_ori_a = RareMatrix.from_url(urls["a_ori_a"])
    c = a ** 2
    print(c==a_ori_a)
    # print(c == a_plus_b)
    # print(c.rare_values[100])
    # print(a.rare_values[0])
    # print("type(a)= ",type(a)," type(b)= ",type(b)," type(c)= ",type(c))
