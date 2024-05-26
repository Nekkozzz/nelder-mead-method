import unittest
from vector import Vector
from method import nelder_mead_method
import math as m

class TestNelderMeadMethod(unittest.TestCase):
    def test_quadratic_function(self):
        def f(X):
            x1, x2 = X
            return (x1-2) ** 2 + (x2-3) ** 2
        
        simplex = [
            Vector(-1, -2),
            Vector(3, 0),
            Vector(2, 1)
        ]
        eps = 1e-5
        
        for xl, *_ in nelder_mead_method(f, simplex): ...
        answer = Vector(2, 3)
        self.assertTrue(m.dist(xl, answer) < eps)

    def test_biquadratic_function(self):
        def f(X):
            x1, x2 = X
            return x1**4 + x2**4
        
        simplex = [
            Vector(5, -2),
            Vector(-1, 2),
            Vector(2, 1)
        ]
        eps = 1e-5
        
        for xl, *_ in nelder_mead_method(f, simplex): ...
        answer = Vector(0, 0)
        self.assertTrue(m.dist(xl, answer) < eps)

    def test_rosenbrock_function(self):
        def f(X):
            x1, x2 = X
            return 100 * (x2-x1**2) ** 2 + (1-x1)**2
        
        simplex = [
            Vector(5, -2),
            Vector(-1, 2),
            Vector(2, 1)
        ]
        eps = 1e-5
        
        for xl, *_ in nelder_mead_method(f, simplex): ...
        answer = Vector(1, 1)
        self.assertTrue(m.dist(xl, answer) < eps)

    def test_michalewicz_function_near_minimum(self):
        def f(X):
            x1, x2 = X
            return -(m.sin(x1) * m.sin(x1**2/m.pi) ** 20 + m.sin(x2) * m.sin(2*x2**2/m.pi) ** 20)
        
        simplex = [
            Vector(2, 2),
            Vector(1, 2),
            Vector(2, 1)
        ]
        eps = 1e-5

        for xl, *_ in nelder_mead_method(f, simplex): ...
        answer = Vector(2.2029, 1.5708)
        self.assertTrue(m.dist(xl, answer) < eps)

    def test_michalewicz_function_in_local_minimum(self):
        def f(X):
            x1, x2 = X
            return -(m.sin(x1) * m.sin(x1**2/m.pi) ** 20 + m.sin(x2) * m.sin(2*x2**2/m.pi) ** 20)
        
        simplex = [
            Vector(-10, 10),
            Vector(10, 11),
            Vector(0, 12)
        ]
        eps = 1e-4

        for xl, *_ in nelder_mead_method(f, simplex): ...
        global_minimum = Vector(2.2029, 1.5708)
        local_minimum = Vector(2.2029, 11.9527)
        self.assertFalse(m.dist(xl, global_minimum) < eps)
        self.assertTrue(m.dist(xl, local_minimum) < eps) 

    def test_rastrigin_function(self):
        # много локальных минимумов
        def f(X):
            x1, x2 = X
            return 20 + (x1**2 - 10*m.cos(2*m.pi*x1)) + (x2**2 - 10*m.cos(2*m.pi*x2))
        
        simplex = [
            Vector(5.12, 5.12),
            Vector(-5.12, -5.12),
            Vector(5.12, -5.12),
            Vector(-5.12, 5.12)
        ]
        eps = 1e-5

        for xl, *_ in nelder_mead_method(f, simplex): ...
        answer = Vector(0, 0)
        self.assertFalse(m.dist(xl, answer) < eps)

    def test_simplex_is_straight_line(self):
        # если точки будут образовывать треугольник с очень маленькой площадью,
        # это может привести к вырождению симплекса и затруднить работу метода
        def f1(X):
            x1, x2 = X
            return (x1-2) ** 2 + (x2-3) ** 2
        
        simplex = [
            Vector(-10, 10),
            Vector(10, 10),
            Vector(0, 10)
        ]
        eps = 1e-5

        for xl, *_ in nelder_mead_method(f1, simplex): ...
        answer = Vector(2, 3)
        self.assertFalse(m.dist(xl, answer) < eps)

if __name__ == '__main__':
    unittest.main()