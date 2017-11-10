import sys
from unittest import TestCase

sys.path.append("../src")

from geometry import Point2D


class TestGeometry(TestCase):
    def test_inside_triangle1(self):
        self.assertTrue(
            Point2D(0, 0, False).inside_triangle(
                Point2D(0, 10, False),
                Point2D(-1, -1, False),
                Point2D(1, -1, False)
            )
        )

    def test_inside_triangle2(self):
        self.assertTrue(
            Point2D(1.5, -1, False).inside_triangle(
                Point2D(5, 2, False),
                Point2D(6, 1, False),
                Point2D(-2, -3, False)
            )
        )

    def test_inside_triangle3(self):
        # Close call
        self.assertFalse(
            Point2D(-3.621, 7.222, False).inside_triangle(
                Point2D(0, 0, False),
                Point2D(-7.5, 8.5, False),
                Point2D(3, 5, False)
            )
        )