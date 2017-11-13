import sys
from unittest import TestCase

sys.path.append("../src")

from geometry import Point2D
from rasterization import solve, lerp, generate


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

    def test_solve3(self):
        s = solve(
            p=Point2D(8, 5, False),
            p1=Point2D(7, 3, False),
            v1=(4, 4, 4),
            p2=Point2D(5, 7, False),
            v2=(12, 12, 12),
            p3=Point2D(13, 9, False),
            v3=(7, 7, 7)
        )
        expected = (6.0, 6.0, 6.0)
        self.assertAlmostEqual(expected[0], s[0])
        self.assertAlmostEqual(expected[1], s[1])
        self.assertAlmostEqual(expected[2], s[2])

    def test_generate(self):
        for _i in range(100):
            g = generate()
            x = {g['p1'].x, g['p2'].x, g['p3'].x}
            y = {g['p1'].y, g['p2'].y, g['p3'].y}
            self.assertEqual(len(x), 3)
            self.assertEqual(len(y), 3)
            self.assertTrue(g['p'].inside_triangle(g['p1'], g['p2'], g['p3']))

    def test_lerp(self):
        self.assertAlmostEqual(lerp(5, 10, 0.5), 7.5, delta=1E-6)
        self.assertAlmostEqual(lerp(2151.123, -9123.124, 0.123), 764.390619, delta=1E-6)
