from unittest import TestCase

from geometry import Point2D
from rasterization import solve


class TestRasterization(TestCase):
    def test_solve1(self):
        s = solve(
            p=Point2D(8, 8, frac=False),
            p1=Point2D(3, 12, frac=False),
            v1=(14, 14, 14),
            p2=Point2D(11, 10, frac=False),
            v2=(19, 19, 19),
            p3=Point2D(9, 6, frac=False),
            v3=(11, 11, 11),
        )
        expected = (13.0, 13.0, 13.0)
        self.assertAlmostEqual(expected[0], s[0])
        self.assertAlmostEqual(expected[1], s[1])
        self.assertAlmostEqual(expected[2], s[2])

    def test_solve2(self):
        s = solve(
            p=Point2D(9, 5, frac=False),
            p1=Point2D(8, 3, frac=False),
            v1=(0.2, 0.2, 0.2),
            p2=Point2D(6, 7, frac=False),
            v2=(0.5, 0.5, 0.5),
            p3=Point2D(14, 9, frac=False),
            v3=(0.8, 0.8, 0.8),
        )
        expected = (23/60, 23/60, 23/60)
        self.assertAlmostEqual(expected[0], s[0])
        self.assertAlmostEqual(expected[1], s[1])
        self.assertAlmostEqual(expected[2], s[2])