import numpy
import numpy as np


def get_u():
    t = 1
    v = 0
    while t > 0:
        t = t/10
        v = t
        if t > 0:
            if 1.0 + v > 1.0:
                u = t
    return u
    # print("u =", u)


def addition():
    u = get_u()
    a = 1.0
    b = u / 10
    c = u / 10
    print((a + b) + c, a + (b + c))


def numere_inmultite_non_asociative():
    u = get_u()
    a = 1.1
    b = u/10
    c = u/10
    return a, b, c


def sin_aprox():
    a = [
      1805490264.690988571178600370234394843221,
      -164384678.227499837726129612587952660511,
      3664210.647581261810227924465160827365,
      -28904.140246461781357223741935980097,
      76.568981088717405810132543523682
    ]
    b = [
      2298821602.638922662086487520330827251172,
      27037050.118894436776624866648235591988,
      155791.388546947693206469423979505671,
      540.567501261284024767779280700089,
      1.0
    ]
    interval = list(np.arange(-1.0, 1.1, 0.1))
    for x in interval:
        p_x = a[0] + pow(x, 2)*(a[1] + pow(x, 2)*(a[2] + pow(x, 2)*(a[3] + pow(x, 2)*a[4])))
        q_x = b[0] + pow(x, 2)*(b[1] + pow(x, 2)*(b[2] + pow(x, 2)*(b[3] + pow(x, 2)*b[4])))
        sin = x * (p_x/q_x)
        print(f"calculat de noi:->sin({(1/4)*numpy.pi*x}) = {sin}")
        print(f"calculat de numpy.sin:->sin({(1/4)*numpy.pi*x}) = {numpy.sin((1/4)*numpy.pi*x)}")
        print(f"modulul diferentei dintre cele 2 valori: {numpy.absolute(sin-numpy.sin((1/4)*numpy.pi*x))}\n")

    # return a, b


def cos_aprox():
    a = [
      1090157078.174871420428849017262549038606,
      -321324810.993150712401352959397648541681,
      12787876.849523878944051885325593878177,
      -150026.206045948110568310887166405972,
      538.333564203182661664319151379451,
    ]

    b = [
    1090157078.174871420428867295670039506886,
    14907035.776643879767410969509628406502,
    101855.811943661368302608146695082218,
    429.772865107391823245671264489311,
    1.0,
    ]
    interval = list(np.arange(-1.0, 1.1, 0.1))
    for x in interval:
        p_x = a[0] + pow(x, 2) * (a[1] + pow(x, 2) * (a[2] + pow(x, 2) * (a[3] + pow(x, 2) * a[4])))
        q_x = b[0] + pow(x, 2) * (b[1] + pow(x, 2) * (b[2] + pow(x, 2) * (b[3] + pow(x, 2) * b[4])))
        cos = p_x / q_x
        print(f"calculat de noi:->cos({(1 / 4) * numpy.pi * x}) = {cos}")
        print(f"calculat de numpy.cos:->cos({(1 / 4) * numpy.pi * x}) = {numpy.cos((1 / 4) * numpy.pi * x)}")
        print(f"modulul diferentei dintre cele 2 valori: {numpy.absolute(cos - numpy.cos((1 / 4) * numpy.pi * x))}\n")

    # return a, b


def ln_aprox():
    a = [
    75.151856149910794642732375452928,
    -134.730399688659339844586721162914,
    74.201101420634257326499008275515,
    -12.777143401490740103758406454323,
    0.332579601824389206151063529971,
    ]

    b = [
    37.575928074955397321366156007781,
    -79.890509202648135695909995521310,
    56.215534829542094277143417404711,
    -14.516971195056682948719125661717,
    1.0
    ]
    interval = list(np.arange(1/numpy.sqrt(2), numpy.sqrt(2), 0.1))
    for x in interval:
        z = (x-1)/(x+1)
        print(f"z = {z}")
        p_x = a[0] + pow(z, 2) * (a[1] + pow(z, 2) * (a[2] + pow(z, 2) * (a[3] + pow(z, 2) * a[4])))
        q_x = b[0] + pow(z, 2) * (b[1] + pow(z, 2) * (b[2] + pow(z, 2) * (b[3] + pow(z, 2) * b[4])))
        ln = z * (p_x / q_x)
        print(f"calculat de noi:->ln({x}) = {ln}")
        print(f"calculat de numpy.log:->ln({x}) = {numpy.log(numpy.exp(x))}")
        print(f"modulul diferentei dintre cele 2 valori: {numpy.absolute(ln - numpy.log(numpy.exp(x)))}\n")

    # return a, b


if __name__ == '__main__':
    # u = get_u()
    # print(u)
    # addition()
    # a,b,c = numere_inmultite_non_asociative()
    # sin_aprox()
    # cos_aprox()
    ln_aprox()

