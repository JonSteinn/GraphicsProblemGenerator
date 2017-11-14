import sys
from unittest import TestCase

sys.path.append("../src")

from clipping import solve, generate
from geometry import Point2D


class TestClipping(TestCase):
    def test_solve_1(self):
        s1 = solve((-200, 200, -100, 100), Point2D(-200, -150, False), Point2D(300, 100, False))
        s2 = solve((-200, 200, -100, 100), Point2D(300, 100, False), Point2D(-200, -150, False))
        self.assertEqual(s1['result'], 'trivial accept')
        self.assertEqual(s2['result'], 'trivial accept')
        self.assertEqual(s1['steps'], 3)
        self.assertEqual(s2['steps'], 3)

    def test_solve_2(self):
        s1 = solve((200, 600, 100, 400), Point2D(0, 50, False), Point2D(500, 450, False))
        s2 = solve((200, 600, 100, 400), Point2D(500, 450, False), Point2D(0, 50, False))
        self.assertEqual(s1['result'], 'trivial accept')
        self.assertEqual(s2['result'], 'trivial accept')
        self.assertEqual(s1['steps'], 3)
        self.assertEqual(s2['steps'], 3)

    def test_solve_3(self):
        s1 = solve((200, 600, 100, 400), Point2D(700, 150, False), Point2D(500, 0, False))
        s2 = solve((200, 600, 100, 400), Point2D(500, 0, False), Point2D(700, 150, False))
        self.assertEqual(s1['result'], 'trivial reject')
        self.assertEqual(s2['result'], 'trivial reject')
        self.assertEqual(s1['steps'], 2)
        self.assertEqual(s2['steps'], 2)

    def test_solve_4(self):
        s1 = solve((200, 600, 100, 400), Point2D(240, 480, False), Point2D(140, 300, False))
        s2 = solve((200, 600, 100, 400), Point2D(140, 300, False), Point2D(240, 480, False))
        self.assertEqual(s1['result'], 'trivial reject')
        self.assertEqual(s2['result'], 'trivial reject')
        self.assertEqual(s1['steps'], 2)
        self.assertEqual(s2['steps'], 2)

    def test_generate(self):
        for _i in range(100):
            g = generate()
            s = solve(g['win'], g['p1'], g['p2'])
            self.assertTrue(s['steps'] > 1)