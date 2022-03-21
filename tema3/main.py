import urllib.request  # the lib that handles the url stuff


class RareMatrix(object):
    rare_values = {}
    @classmethod
    def from_url(self,url):
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
        self.rare_values = dictionary1
        return self.rare_values

if __name__ == '__main__':
    urls = {
        "a": "https://profs.info.uaic.ro/~ancai/CN/lab/3/a.txt",
        "b": "https://profs.info.uaic.ro/~ancai/CN/lab/3/b.txt",
        "a_plus_b": "https://profs.info.uaic.ro/~ancai/CN/lab/3/a_plus_b.txt",
        "a_ori_a": "https://profs.info.uaic.ro/~ancai/CN/lab/3/a_ori_a.txt"
    }
    # a = RareMatrix.from_url(urls["a"])
    b = RareMatrix.from_url(urls["b"])
    # a_plus_b = RareMatrix.from_url(urls["a_plus_b"])
    # a_ori_a = RareMatrix.from_url(urls["a_ori_a"])
    print(b)