from unittest import TestCase

import sys
sys.path.append("../src")

from geometry import Point3D, Vector3D
from lighting import Color, solve, generate


class TestLighting(TestCase):
    def test_solve1(self):
        s = solve(
            v_pos=Point3D(1, 4, 3),
            v_normal=Vector3D(0, 0, -1),
            c_pos=Point3D(-1, -1, 5),
            l_pos=Point3D(3, 8, -2),
            g_a=Color(0, 0, 0),
            l_a=Color(0.3, 0.7, 0.6),
            l_d=Color(0.3, 0.7, 0.6),
            l_s=Color(0.3, 0.7, 0.6),
            m_a=Color(0.3, 0.1, 0.2),
            m_d=Color(0.6, 0.2, 0.4),
            m_s=Color(1, 1, 1),
            shine=10
        )
        expected = Color(
            r=0.401311078649987,
            g=0.587692838949990,
            b=0.653179438199983
        )

        self.assertAlmostEqual(s.r, expected.r, delta=1E-5, msg='r')
        self.assertAlmostEqual(s.g, expected.g, delta=1E-5, msg='g')
        self.assertAlmostEqual(s.b, expected.b, delta=1E-5, msg='b')

    def test_solve2(self):
        s = solve(
            v_pos=Point3D(4, 4, 3),
            v_normal=Vector3D(0, 1, 0),
            c_pos=Point3D(4, 6, 5),
            l_pos=Point3D(5, 8, -1),
            g_a=Color(0.3, 0.2, 0.4),
            l_a=Color(0, 0, 0),
            l_d=Color(0.5, 0.3, 0.7),
            l_s=Color(0.3, 0.8, 0.7),
            m_a=Color(0.4, 0.2, 0.3),
            m_d=Color(0.4, 0.7, 0.2),
            m_s=Color(0.6, 0.6, 0.6),
            shine=13
        )
        expected = Color(
            r=0.336555752545358,
            g=0.392341571751585,
            b=0.397835285490389
        )

        self.assertAlmostEqual(s.r, expected.r, delta=1E-5, msg='r')
        self.assertAlmostEqual(s.g, expected.g, delta=1E-5, msg='g')
        self.assertAlmostEqual(s.b, expected.b, delta=1E-5, msg='b')

    def test_solve3(self):
        s = solve(
            v_pos=Point3D(0, 1, 1),
            v_normal=Vector3D(1, -1, 3),
            c_pos=Point3D(-3, 3, 4),
            l_pos=Point3D(3, -2, 2),
            l_a=Color(0, 0, 0),
            l_d=Color(0.5, 0.3, 0.7),
            l_s=Color(0.3, 0.8, 0.7),
            g_a=Color(0.3, 0.2, 0.4),
            m_a=Color(0.4, 0.7, 0.3),
            m_d=Color(0.4, 0.7, 0.2),
            m_s=Color(0.6, 0.6, 0.6),
            shine=21
        )
        expected = Color(
            r=0.3067022520099555,
            g=0.4365837630415202,
            b=0.3522745356466035
        )

        self.assertAlmostEqual(s.r, expected.r, delta=1E-5, msg='r')
        self.assertAlmostEqual(s.g, expected.g, delta=1E-5, msg='g')
        self.assertAlmostEqual(s.b, expected.b, delta=1E-5, msg='b')

    def test_generate(self):
        for _i in range(100):
            g = generate()
            self.assertFalse(g['v_pos'] == g['c_pos'])
            self.assertFalse(g['v_pos'] == g['l_pos'])
            self.assertFalse(g['c_pos'] == g['l_pos'])