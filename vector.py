class Vector(tuple):
    def __new__(cls, *body):
        if not body:
            raise ValueError('')
        elif len(body) == 1:
            raise ValueError('')
        return tuple.__new__(cls, body)
    
    def __add__(self, other):
        if not isinstance(other, Vector):
            raise ValueError('Other must be a vector')
        if (len(self) != len(other)):
            raise IndexError('Vectors must have same dimmensions') 
        return Vector(*tuple(x + y for x, y in zip(self, other)))
    __radd__ = __add__

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise ValueError('Other must be a vector')
        if (len(self) != len(other)):
            raise IndexError('Vectors must have same dimmensions') 
        return Vector(*tuple(x - y for x, y in zip(self, other)))
    
    def __rsub__(self, other):
        if not isinstance(other, Vector):
            raise ValueError('Other must be a vector')
        if (len(self) != len(other)):
            raise IndexError('Vectors must have same dimmensions')
        return Vector(*tuple(y - x for x, y in zip(self, other)))

    def __mul__(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError('Other must be an int or a float')
        return Vector(*tuple(x * value for x in self))
    __rmul__ = __mul__

    def __truediv__(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError('Other must be an int or a float')
        if value == 0:
            raise ZeroDivisionError('Division by zero')
        return Vector(*tuple(x / value for x in self))