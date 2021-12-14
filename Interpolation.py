import typing
import math


class Interpolation:
    def __init__(self, function: typing.Callable, diapason: list, points_num: int) -> None:
        self.function = function
        self.n = points_num
        self.diapason = diapason
        self.x_step = (self.diapason[1] - self.diapason[0]) / (self.n - 1)

        self.FindPoints()
        self.FindYDirrerences()

        self.q = lambda x: (x - self.diapason[0]) / self.x_step
        self.t = lambda x: (x - self.diapason[1]) / self.x_step
        self.FindCForLagrange()

    def __init__(self, points: list) -> None:
        self.n = len(points)
        self.diapason = [min([p[0] for p in points]), max([p[0] for p in points])]
        self.x_step = (self.diapason[1] - self.diapason[0]) / (self.n - 1)

        self.points = points
        self.FindYDirrerences()

        self.q = lambda x: (x - self.diapason[0]) / self.x_step
        self.t = lambda x: (x - self.diapason[1]) / self.x_step
        self.FindCForLagrange()


    def FindPoints(self) -> None:
        self.points = list()
        x = self.diapason[0]
        for i in range(self.n):
            self.points.append([x + i * self.x_step, self.function(x + i * self.x_step)])
    
    def FindYDirrerences(self) -> None:
        self.y_differences = list() 
        self.y_differences.append(
            [self.points[j + 1][1] - self.points[j][1]
            for j in range(self.n - 1)]
        )
        for i in range(self.n - 2):
            self.y_differences.append(
                [self.y_differences[i][j + 1] - self.y_differences[i][j]
                for j in range(self.n - i - 2)]
            )

    def FindCForLagrange(self) -> None:
        self.c = list()
        for i in range(self.n):
            divider = 1
            for j in range(self.n):
                if i != j:
                    divider *= self.points[i][0] - self.points[j][0]
            self.c.append(
                self.points[i][1] / divider
            )
            
    def PrintFirstNewton(self) -> None:
        pass

    def PrintSecNewton() -> None:
        pass

    def PrintLagrange(self) -> None:
        formula = ''
        for i in range(self.n):
            c = str(abs(round(self.c[i], PRECISION)))
            if self.c[i] >= 0:
                formula += '+' + c
            else:
                formula += '-' + c
            for j in range(self.n):
                if i != j:
                    formula += '(x'
                    x = str(abs(round(self.points[j][0], PRECISION)))
                    if self.points[j][0] >= 0:
                        formula += '-' + x
                    else:
                        formula += '+' + x
                    formula += ')'
        print(formula)
    
    def ComputeFirstNewton(self, x: float) -> float:
        q = self.q(x)
        result = self.points[0][1]
        for i in range(1, self.n):
            frac = self.y_differences[i - 1][0]
            for j in range(i):
                frac *= q - j
                frac /= j + 1
            result += frac
        return result

    def ComputeSecNewton(self, x: float) -> float:
        t = self.t(x)
        result = self.points[self.n - 1][1]
        for i in range(1, self.n):
            frac = self.y_differences[i - 1][self.n - i - 1]
            for j in range(i):
                frac *= t + j
                frac /= j + 1
            result += frac
        return result

    def ComputeLagrange(self, x: float) -> float:
        result = 0
        for i in range(self.n):
            mult = self.c[i]
            for j in range(self.n):
                if i != j:
                    mult *= x - self.points[j][0]
            result += mult
        return result

    def PrintTable(self, points: list) -> None:
        header = MakeRow(['x', 'y(x)', 'PI(x)', '|y(x)-PI(x)|', 'PII(x)', '|y(x)-PII(x)|', 'L(x)', '|y(x)-L(x)|'])
        row = '-' * len(header)
        print('Function Interpolation Table:')
        print(row)
        print(header)
        print(row)
        for i in range(len(points)):
            values = list()
            x  = points[i]
            y = self.function(x)
            fn = self.ComputeFirstNewton(x)
            sn = self.ComputeSecNewton(x)
            l = self.ComputeLagrange(x)
            values.append(x)
            values.append(y)
            values.append(fn)
            values.append(Difference(y, fn))
            values.append(sn)
            values.append(Difference(y, sn))
            values.append(l)
            values.append(Difference(y, l))
            print(MakeRow(values))
            print(row)


def RoundList(a: list) -> list:
    b = list()
    for i in range(len(a)):
        b.append(round(a[i], PRECISION))
    return b

def Difference(a: float, b: float) -> float:
    return abs(a - b)

def MakeRow(a: list) -> str:
    row = str()
    for i in range(len(a)):
        row += '|' + StrColumn(a[i])
    row += '|'
    return row

def StrColumn(s: str) -> str:
    return '{0:^24}'.format(s)


PRECISION = 20
#
# change the function for interpolation
#
F = lambda x: 10 * math.sin(x) - math.exp((6 * x + 5) / 11)
#
# change the an array of dots
# #
my_function = Interpolation([[0.0, 1.0],
    [0.115, 0.99], [0.352, 0.95], [0.584, 0.9],
    [6.3, 0.1], [7.8, 0.05], [9.8, 0.02],
    [11.3, 0.01], [12.8, 0.005], [16.3, 0.001],
    ])
print(my_function.ComputeLagrange(1.2424))
print(my_function.ComputeFirstNewton(1.2424))
print(my_function.ComputeSecNewton(1.2424))
print('Lagrange Formula:')
my_function.PrintLagrange()
