from math import exp


class DiscreteFunction:
    def __init__(self, a, h, ys):
        self.a = a
        self.b = a + h*(len(ys)-1)
        self.h = h
        self.points = []

        for i in range(len(ys)):
            self.points.append((a + i*h, ys[i]))

    def __str__(self):
        return ' '.join(map(str, self.points))

    def get_points(self):
        return self.points

    def get_last_y(self):
        return self.points[-1][1]

    def raw_format(self):
        return '\n'.join([str(y) for x, y in self.points])


def main():
    output_handle = open('output.txt', 'w')

    a = 0
    b = 5
    h = 0.1
    f1 = lambda x, y, z: z
    f2 = lambda x, y, z: y + 3 + 1.5*x*x*(x-1)
    g = lambda mu: f(output_handle, mu, f1, f2, a, b, h)

    bisect_a = -100
    bisect_b = 100
    mu_res = bisect_method(g, bisect_a, bisect_b)

    y_func, _ = cauchy_method(f1, f2, a, b, h, 3, mu_res)

    print_value(output_handle, 'mu* = ' + str(mu_res))
    print_value(output_handle, 'y(x, mu*) = \n' + y_func.raw_format())
    # print_solution(output_handle, a, b, h)


def f(output_handle, mu, f1, f2, a, b, h):
    y_func, z_func = cauchy_method(f1, f2, a, b, h, 3, mu)

    print_value(output_handle, y_func)
    print_value(output_handle, z_func)

    # y'(b) + y(b) - ...
    result = z_func.get_last_y() + y_func.get_last_y() - 2 * exp(5) + 301.5

    print_value(output_handle, result)
    print_value(output_handle, '')

    return result


def print_value(output_handle, value):
    print(str(value))
    output_handle.write(str(value) + '\n')


def print_solution(output_handle, a, b, h):
    x = a

    while x < b or close(x, b):
        y = solution(x)

        result = str(y)
        print(result)
        output_handle.write(result + '\n')

        x += h


def solution(x):
    return exp(x) + 2*exp(-x) - 1.5*x*x*x + 1.5*x*x - 9*x


def bisect_method(function, a, b):
    if function(a) == 0:
        return a

    if function(b) == 0:
        return b

    eps = 1e-8
    ab2 = (b - a) / 2
    c = a + ab2
    f_c = function(c)

    while abs(f_c) > eps:
        if sign(function(a)) != sign(f_c):
            b = c
        else:
            a = c

        ab2 /= 2
        c = a + ab2
        f_c = function(c)

    return (a + b) / 2


def sign(x):
    if x == 0:
        return 0

    if x < 0:
        return -1

    if x > 0:
        return 1


def cauchy_method(f1, f2, a, b, h, y0, z0):
    xn = a
    yn = y0
    zn = z0
    ys = [y0]
    zs = [z0]

    while xn < b - h or close(xn, b - h):
        yn_temp = yn + h/2*f1(xn, yn, zn)
        zn_temp = zn + h/2*f2(xn, yn, zn)

        xnp1 = xn + h
        ynp1 = yn + h*f1(xn + h/2, yn_temp, zn_temp)
        znp1 = zn + h*f2(xn + h/2, yn_temp, zn_temp)

        ys.append(ynp1)
        zs.append(znp1)

        xn = xnp1
        yn = ynp1
        zn = znp1

    return DiscreteFunction(a, h, ys), DiscreteFunction(a, h, zs)


def test():
    f1 = lambda x, y, z: z
    f2 = lambda x, y, z: y + 3 + 1.5*x*x*(x-1)
    a = 0
    b = 5
    h = 0.1
    y_func, z_func = cauchy_method(f1, f2, a, b, h, 3, 0)
    assert len(y_func.points) == (b - a)/h + 1
    assert len(z_func.points) == (b - a)/h + 1

    actual = bisect_method(lambda x: x, -1, 1)
    assert close(actual, 0)

    actual = bisect_method(solution, 0, 1)
    assert close(actual, 0.326289)

    actual = bisect_method(solution, 5, 6)
    assert close(actual, 5.572782)


def close(a, b):
    return abs(a - b) < 1e-6


if __name__ == "__main__":
    test()
    main()
