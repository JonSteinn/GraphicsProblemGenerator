from fractions import Fraction
from math import sqrt


class Mat4:
    def __init__(self):
        self.mat = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

    def get_row(self, row):
        """
        :type row: int
        """
        return self.mat[row]

    def set_element(self, row, col, elem):
        """
        :type row: int
        :type col: int
        :type elem: float or int
        """
        self.mat[row][col] = elem

    def get_element(self, row, col):
        """
        :type row: int
        :type col: int
        """
        return self.mat[row][col]

    def __str__(self):
        return '\n'.join([','.join(map(str, self.mat[i])) for i in range(4)])


class Point3D:
    def __init__(self, x, y, z):
        """
        :type x: int or float
        :type y: int or float
        :type z: int or float
        """
        self.x = x
        self.y = y
        self.z = z

    def vector_to(self, other):
        """
        :type other: Point3D
        """
        return Vector3D(other.x - self.x, other.y - self.y, other.z - self.z)

    def move_by(self, vec):
        """
        :type vec: Vector3D
        """
        return Point3D(self.x + vec.x, self.y + vec.y, self.z + vec.z)

    def to_vector(self):
        return Vector3D(self.x, self.y, self.z)

    def __str__(self):
        return "({0},{1},{2})".format(self.x, self.y, self.z)

    def __eq__(self, other):
        """
        :type other: Point3D
        """
        return self.x == other.x and self.y == other.y and self.z == other.z


class Vector3D:
    @staticmethod
    def cross_product(u, v):
        """
        :type u: Vector3D
        :type v: Vector3D
        """
        return Vector3D(
            u.y * v.z - u.z * v.y,
            u.z * v.x - u.x * v.z,
            u.x * v.y - u.y * v.x
        )

    def __init__(self, x, y, z):
        """
        :type x: int or float
        :type y: int or float
        :type z: int or float
        """
        self.x = x
        self.y = y
        self.z = z

    def dot_product(self, other):
        """
        :type other: Vector2D
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def dot_self(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def scaled(self, s):
        return Vector3D(self.x * s, self.y * s, self.z * s)

    def length(self):
        return sqrt(self.dot_self())

    def normalize(self):
        l = self.length()
        self.x /= l
        self.y /= l
        self.z /= l

    def __sub__(self, other):
        """
        :type other: Vector3D
        """
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        """
        :type other: Vector3D
        """
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return "[{0},{1},{2}]".format(self.x, self.y, self.z)

    def __eq__(self, other):
        """
        :type other: Vector3D
        """
        return self.x == other.x and self.y == other.y and self.z == other.z


def to_fraction(x):
    if type(x) == Fraction:
        return x
    return Fraction(x)


class Point2D:
    def __init__(self, x, y, frac=True):
        """
        :type x: Fraction or int or float
        :type y: Fraction or int or float
        """
        if frac:
            self.x = to_fraction(x)
            self.y = to_fraction(y)
        else:
            self.x = x
            self.y = y

    def as_vector(self):
        return Vector2D(self.x, self.y)

    def vector_to(self, other):
        """
        :type other: Point2D
        """
        return Vector2D(other.x - self.x, other.y - self.y)

    def slope_to(self, other):
        """
        :type other: Point2D
        """
        return (self.y - other.y) / (self.x - other.x)

    def move_by(self, vec):
        """
        :type vec: Vector2D
        """
        return Point2D(self.x + vec.x, self.y + vec.y)

    def inside_triangle(self, p1, p2, p3):
        """
        :type p1: Point2D
        :type p2: Point2D
        :type p3: Point2D
        """
        v = self.as_vector()
        v0 = p1.as_vector()
        v1 = p1.vector_to(p2)
        v2 = p1.vector_to(p3)
        denominator = v1.det(v2)
        if denominator == 0:
            return False
        a = (v.det(v2) - v0.det(v2)) / denominator
        b = -(v.det(v1) - v0.det(v1)) / denominator
        return 0 < a < 1 and 0 < b < 1 and a + b < 1

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def __eq__(self, other):
        """
        :type other: Point2D
        """
        return self.x == other.x and self.y == other.y


class Vector2D:
    def __init__(self, x, y, frac=True):
        """
        :type x: Fraction or int or float
        :type y: Fraction or int or float
        """
        if frac:
            self.x = to_fraction(x)
            self.y = to_fraction(y)
        else:
            self.x = x
            self.y = y

    def dot_product(self, other):
        """
        :type other: Vector2D
        """
        return self.x * other.x + self.y * other.y

    def normal(self):
        return Vector2D(-self.y, self.x)

    def dot_self(self):
        return self.x ** 2 + self.y ** 2

    def scaled(self, s):
        return Vector2D(self.x * s, self.y * s)

    def det(self, other):
        """
        :type other: Vector2D
        """
        return self.x * other.y - self.y * other.x

    def __sub__(self, other):
        """
        :type other: Vector2D
        """
        return Vector2D(self.x - other.x, self.y - other.y)

    def __str__(self):
        return "[{0},{1}]".format(self.x, self.y)

    def __eq__(self, other):
        """
        :type other: Vector2D
        """
        return self.x == other.x and self.y == other.y