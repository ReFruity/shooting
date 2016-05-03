from math import exp

from numpy import arange


def main():
    input_handle = open('input.txt', 'r')
    output_handle = open('output.txt', 'w')

    h = 0.1
    x = 0

    while x <= 5:
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

    ab = b - a
    eps = 1e-8

    while b - a > eps:
        ab /= 2
        c = a + ab

        if sign(function(a)) != sign(function(c)):
            b = c
        else:
            a = c

    return (a + b)/2


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
    result = [(a, y0)]

    while xn < b - h or close(xn, b - h):
        yn_temp = yn + h/2*f1(xn, yn, zn)
        zn_temp = zn + h/2*f2(xn, yn, zn)

        xnp1 = xn + h
        ynp1 = yn + h*f1(xn + h/2, yn_temp, zn_temp)
        znp1 = zn + h*f2(xn + h/2, yn_temp, zn_temp)

        result.append((xnp1, ynp1))

        xn = xnp1
        yn = ynp1
        zn = znp1

    return result


def test():
    f1 = lambda x, y, z: z
    f2 = lambda x, y, z: y + 3 + 1.5*x*x*(x-1)
    a = 0
    b = 5
    h = 0.1
    actual = cauchy_method(f1, f2, a, b, h, 3, 1)
    actual_ys = [y for (x, y) in actual]
    assert len(actual) == (b - a)/h + 1
    expected_ys = [solution(x) for x in arange(a, b + h, h)]
    assert list_distance(actual_ys, expected_ys) <= 1

    actual = bisect_method(lambda x: x, -1, 1)
    assert close(actual, 0)

    actual = bisect_method(solution, 0, 1)
    assert close(actual, 0.326289)

    actual = bisect_method(solution, 5, 6)
    assert close(actual, 5.57278)


def list_distance(list1, list2):
    result = 0

    for i in range(min(len(list1), len(list2))):
        result += abs(list1[i] - list2[i])

    return result


def close(a, b):
    return abs(a - b) < 1e-6


if __name__ == "__main__":
    test()
    main()
