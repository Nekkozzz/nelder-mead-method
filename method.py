from vector import Vector
from operators import *


def f(X: Vector) -> float:
    x1, x2 = X
    return x1 ** 2 + x1 * x2 + x2 ** 2 - 6 * x1 - 9 * x2

def nelder_mead_method(f, simplex: list[Vector], n: int = 0):
    k = 0
    
    while k < n:
        k += 1
        simplex.sort(key=lambda x: f(x))
        xh, xg, xl = simplex[-1], simplex[-2], simplex[0]

        xc = weight_center(*[x for x in simplex if x != xh])

        xr = reflection(xh, xc)

        if f(xr) < f(xl):
            xe = expansion(xr, xc)
            if f(xe) < f(xr):
                xh = xe
                simplex[-1] = xe
            elif f(xr) < f(xe):
                xh = xr
                simplex[-1] = xr
            continue
        
        if f(xl) < f(xr) < f(xg):
            xh = xr
            xh = xr
            simplex[-1] = xr
            continue

        if f(xg) < f(xr) < f(xh):
            xr, xh = xh, xr
            simplex[-1] = xr

        xs = contraction(xh, xc)

        if f(xs) < f(xh):
            xh = xs
            simplex[-1] = xs
            continue
        elif f(xs) > f(xh):
            simplex = homothety(simplex, xl)

    return xl

if __name__ == '__main__':
    n = 10
    simplex = [
        Vector(0, 0),
        Vector(1, 0),
        Vector(0, 1),
    ]
    x = nelder_mead_method(f, simplex, 10)
    print(x, f(x))