import unittest
from vector import Vector
from operators import *

class TestVector(unittest.TestCase):
    def test_addition(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        result = v1 + v2
        self.assertEqual(result, Vector(5, 7, 9))

    def test_subtraction(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, 5, 6)
        result = v1 - v2
        self.assertEqual(result, Vector(-3, -3, -3))

    def test_multiplication(self):
        v1 = Vector(1, 2, 3)
        scalar = 2
        result = v1 * scalar
        self.assertEqual(result, Vector(2, 4, 6))

    def test_division(self):
        v1 = Vector(2, 4, 6)
        divisor = 2
        result = v1 / divisor
        self.assertEqual(result, Vector(1, 2, 3))

    def test_zero_division(self):
        v1 = Vector(1, 2, 3)
        divisor = 0
        with self.assertRaises(ZeroDivisionError):
            result = v1 / divisor

    def test_with_different_dimension(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(1, 2)
        with self.assertRaises(IndexError):
            result = v1 + v2

    def test_invalid_operation(self):
        v1 = Vector(1, 2, 3)
        with self.assertRaises(ValueError):
            result = v1 + 5

class TestOperator(unittest.TestCase):
    def test_weight_center(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        v3 = Vector(5, 6)
        xc = weight_center(v1, v2, v3)
        self.assertEqual(xc, Vector(3, 4))

    def test_reflection(self):
        v1 = Vector(1, 2)
        v2 = Vector(5, 6)
        xc = weight_center(v1, v2)
        xs = reflection(v1, xc)
        self.assertEqual(xs, Vector(5, 6))
    
    def test_contraction(self):
        v1 = Vector(1, 2)
        v2 = Vector(5, 6)
        xc = weight_center(v1, v2)
        xs = contraction(v1, xc)
        self.assertEqual(xs, Vector(2, 3))

    def test_expansion(self):
        v1 = Vector(1, 2)
        v2 = Vector(5, 6)
        xr = reflection(v1, v2)
        xc = weight_center(v1, v2)
        xe = expansion(xr, xc)
        self.assertEqual(xe, Vector(15, 16))

    def test_homothety(self):
        simplex = [Vector(1, 2), Vector(3, 4), Vector(5, 6)]
        xl = Vector(0, 0)
        result = homothety(simplex, xl)
        self.assertEqual(result, [Vector(0.5, 1), Vector(1.5, 2), Vector(2.5, 3)])

    def test_homothety_2(self):
        simplex = [Vector(1, 2), Vector(1, 2), Vector(5, 6)]
        xl = Vector(5, 9)
        result = homothety(simplex, xl)
        self.assertEqual(result, [Vector(3, 5.5), Vector(3, 5.5), Vector(5, 7.5)])

    def test_homothety_3(self):
        simplex = [Vector(1, 2), Vector(-1, -2), Vector(5, 6)]
        xl = Vector(5, 9)
        result = homothety(simplex, xl)
        self.assertEqual(result, [Vector(3, 5.5), Vector(2, 3.5), Vector(5, 7.5)])

    def test_closure(self):
        simplex = [Vector(1, 2), Vector(-1, -2), Vector(5, 6)]
        eps = 5.3
        self.assertTrue(closure(simplex, eps))

    def test_not_closure(self):
        simplex = [Vector(1, 2), Vector(-1, -2), Vector(5, 6)]
        eps = 1.0
        self.assertFalse(closure(simplex, eps))

if __name__ == '__main__':
    unittest.main()