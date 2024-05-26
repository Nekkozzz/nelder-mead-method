from functools import reduce
from vector import Vector
import math as m


def weight_center(*points: list[Vector]) -> Vector:
    xc = reduce(lambda x, y: x + y, points) / len(points)
    return xc

def reflection(xh: Vector, xc: Vector, alpha: float = 1) -> Vector:
    xr = (1 + alpha) * xc - alpha * xh
    return xr

def contraction(xh: Vector, xc: Vector, beta: float = 0.5) -> Vector:
    xs = (1 - beta) * xc + beta * xh
    return xs

def expansion(xr: Vector, xc: Vector, gamma: float = 2) -> Vector:
    xe = (1 - gamma) * xc + gamma * xr
    return xe

def homothety(simplex: list[Vector], xl: Vector) -> list[Vector]:
    return [xl + (x - xl) / 2 for x in simplex]

def closure(simplex: list[Vector], eps: float):
    if all(v == simplex[0] for v in simplex):
        return True
    xc = weight_center(*simplex)
    for x in simplex:
        if m.dist(x, xc) > eps:
            return False
    return True