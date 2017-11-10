from unittest import TestCase

import sys
sys.path.append("../src")

from bezier import solve
from geometry import Point3D


class TestBezier(TestCase):
    def test_solve(self):
        s = solve([
            Point3D(15, 5, 2),
            Point3D(10, 2, 2),
            Point3D(5, 7, 2),
            Point3D(0, 0, 2)
        ], 0.75)

        expected = Point3D(15/4, 53/16, 2)

        self.assertAlmostEqual(s.x, expected.x, delta=1E-5)
        self.assertAlmostEqual(s.y, expected.y, delta=1E-5)
        self.assertAlmostEqual(s.z, expected.z, delta=1E-5)
