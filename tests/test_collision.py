from fractions import Fraction
from unittest import TestCase

from collision import Point2D, Vector2D, solve, generate


class TestCollision(TestCase):
    def test_solve1(self):
        p = Point2D(4, 2)
        p1 = Point2D(3, 8)
        p2 = Point2D(7, 6)
        v = Vector2D(1, 3)
        sol = solve(p, p1, p2, v)
        expected = (
            Fraction(11, 7),
            Point2D(Fraction(39, 7), Fraction(47, 7)),
            Vector2D(Fraction(-9, 5), Fraction(-13, 5))
        )
        self.assertTrue(sol['does_hit'], 'should hit')
        self.assertEqual(sol['t_hit'], expected[0],
                         "t_hit should be {0} but is {1}".format(expected[0], sol['t_hit']))
        self.assertEqual(sol['p_hit'], expected[1],
                         "p_hit should be {0} but is {1}".format(expected[1], sol['p_hit']))
        self.assertEqual(sol['reflection'], expected[2],
                         "reflection should be {0} but is {1}".format(expected[2], sol['reflection']))

    def test_solve2(self):
        p = Point2D(1, -1)
        p1 = Point2D(-5, -5)
        p2 = Point2D(5, 5)
        v = Vector2D(1, -1)
        sol = solve(p, p1, p2, v)
        self.assertFalse(sol['does_hit'], 'should not hit')

    def test_solve3(self):
        p = Point2D(12, 0)
        p1 = Point2D(11, 1)
        p2 = Point2D(11, -1)
        v = Vector2D(-1, -1)
        sol = solve(p, p1, p2, v)
        expected = (
            Fraction(1),
            Point2D(11, -1),
            Vector2D(1, -1)
        )
        self.assertTrue(sol['does_hit'], 'should hit')
        self.assertEqual(sol['t_hit'], expected[0],
                         "t_hit should be {0} but is {1}".format(expected[0], sol['t_hit']))
        self.assertEqual(sol['p_hit'], expected[1],
                         "p_hit should be {0} but is {1}".format(expected[1], sol['p_hit']))
        self.assertEqual(sol['reflection'], expected[2],
                         "reflection should be {0} but is {1}".format(expected[2], sol['reflection']))

    def test_solve4(self):
        p = Point2D(6, 13)
        p1 = Point2D(-4, 10)
        p2 = Point2D(5, -2)
        v = Vector2D(-2, -7)
        sol = solve(p, p1, p2, v)
        expected = (
            Fraction(49, 29),
            Point2D(Fraction(76, 29), Fraction(34, 29)),
            Vector2D(Fraction(182, 25), Fraction(-1, 25))
        )
        self.assertTrue(sol['does_hit'], 'should hit')
        self.assertEqual(sol['t_hit'], expected[0],
                         "t_hit should be {0} but is {1}".format(expected[0], sol['t_hit']))
        self.assertEqual(sol['p_hit'], expected[1],
                         "p_hit should be {0} but is {1}".format(expected[1], sol['p_hit']))
        self.assertEqual(sol['reflection'], expected[2],
                         "reflection should be {0} but is {1}".format(expected[2], sol['reflection']))

    def test_solve5(self):
        p = Point2D(6, -3)
        p1 = Point2D(-10, -4)
        p2 = Point2D(4, -5)
        v = Vector2D(-5, -5)
        sol = solve(p, p1, p2, v)
        expected = (
            Fraction(2, 5),
            Point2D(4, -5),
            Vector2D(Fraction(-835, 197), Fraction(1115, 197))
        )
        self.assertTrue(sol['does_hit'], 'should hit')
        self.assertEqual(sol['t_hit'], expected[0],
                         "t_hit should be {0} but is {1}".format(expected[0], sol['t_hit']))
        self.assertEqual(sol['p_hit'], expected[1],
                         "p_hit should be {0} but is {1}".format(expected[1], sol['p_hit']))
        self.assertEqual(sol['reflection'], expected[2],
                         "reflection should be {0} but is {1}".format(expected[2], sol['reflection']))

    def test_generate1(self):
        for i in range(250):
            g = generate(Point2D(-25, -25), Point2D(25, 25))
            p = g['pnt']
            p1 = g['pnt1']
            p2 = g['pnt2']
            v = g['vec']
            self.assertNotEqual(p1, p2, "Line is a point")
            self.assertNotEqual(p1.x, p2.x, "Simple line (x)")
            self.assertNotEqual(p1.y, p2.y, "Simple line (y)")
            self.assertTrue(solve(p, p1, p2, v)['does_hit'])