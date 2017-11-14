import sys
from unittest import TestCase

sys.path.append("../src")

from geometry import Point2D
from window2viewport import solve, generate


class TestWindow2Viewport(TestCase):
    def test_solve1(self):
        self.assertEqual(
            solve((-10, 30, 50, 80), (0, 1600, 0, 1200), Point2D(-5, 70, False)),
            Point2D(200, 800, False),
            False
        )

    def test_solve2(self):
        self.assertEqual(
            solve((-10, 30, 50, 80), (0, 1600, 0, 1200), Point2D(20, 65, False)),
            Point2D(1200, 600, False),
            False
        )

    def test_solve3(self):
        self.assertEqual(
            solve((-1, 1, -1, 1), (0, 640, 0, 480), Point2D(0.5, 0.0, False)),
            Point2D(480, 240, False),
            False
        )

    def test_generate(self):
        for _i in range(100):
            g = generate()
            self.assertTrue((lambda z: z[0] < z[1] and z[2] < z[3])(g['v']))
            self.assertTrue((lambda z: z[0] < z[1] and z[2] < z[3])(g['w']))
            p = g['p']
            self.assertTrue(g['w'][0] <= p.x <= g['w'][1])
            self.assertTrue(g['w'][2] <= p.y <= g['w'][3])