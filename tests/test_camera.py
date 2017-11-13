from math import sqrt, tan, pi
from unittest import TestCase

import sys

sys.path.append("../src")

from camera import solve, generate
from geometry import Point3D, Vector3D


class TestCamera(TestCase):
    def test_solve1(self):
        d = 1E-5
        s = solve(
            eye=Point3D(0, 8, 4),
            look=Point3D(0, 3, -1),
            up=Vector3D(0, 0, -1),
            fov=75,
            aspect_ratio=16 / 9,
            near=3,
            far=25
        )
        n = s['n']
        u = s['u']
        v = s['v']
        vm = s['view_mat']
        pm = s['projection_mat']

        expected = (
            #u
            (
                1.0,
                0,
                0
            ),
            #v
            (
                0,
                sqrt(2) / 2,
                -sqrt(2) / 2
            ),
            #n
            (
                0,
                sqrt(2) / 2,
                sqrt(2) / 2
            ),
            #vm
            {
                (0, 0): 1,
                (0, 1): 0,
                (0, 2): 0,
                (0, 3): 0,

                (1, 0): 0,
                (1, 1): sqrt(2)/2,
                (1, 2): -sqrt(2)/2,
                (1, 3): -2*sqrt(2),

                (2, 0): 0,
                (2, 1): sqrt(2)/2,
                (2, 2): sqrt(2)/2,
                (2, 3): -6*sqrt(2),

                (3, 0): 0,
                (3, 1): 0,
                (3, 2): 0,
                (3, 3): 1,
            },
            #pm
            {
                (0, 0): 9 / (16 * (sqrt(6) + sqrt(3) - sqrt(2) - 2)),
                (0, 1): 0,
                (0, 2): 0,
                (0, 3): 0,

                (1, 0): 0,
                (1, 1): 1 / (sqrt(6) + sqrt(3) - sqrt(2) - 2),
                (1, 2): 0,
                (1, 3): 0,

                (2, 0): 0,
                (2, 1): 0,
                (2, 2): -14 / 11,
                (2, 3): -75 / 11,

                (3, 0): 0,
                (3, 1): 0,
                (3, 2): -1,
                (3, 3): 0,
            }
        )

        # U
        self.assertAlmostEqual(u.x, expected[0][0], delta=d)
        self.assertAlmostEqual(u.y, expected[0][1], delta=d)
        self.assertAlmostEqual(u.z, expected[0][2], delta=d)

        # V
        self.assertAlmostEqual(v.x, expected[1][0], delta=d)
        self.assertAlmostEqual(v.y, expected[1][1], delta=d)
        self.assertAlmostEqual(v.z, expected[1][2], delta=d)

        # N
        self.assertAlmostEqual(n.x, expected[2][0], delta=d)
        self.assertAlmostEqual(n.y, expected[2][1], delta=d)
        self.assertAlmostEqual(n.z, expected[2][2], delta=d)

        # View matrix
        for vm_kv in expected[3].items():
            self.assertAlmostEqual(vm.get_element(*vm_kv[0]), vm_kv[1], delta=d)

        # Projection matrix
        for pm_kv in expected[4].items():
            self.assertAlmostEqual(pm.get_element(*pm_kv[0]), pm_kv[1], delta=d)

    def test_solve2(self):
        d = 1E-5
        s = solve(
            eye=Point3D(-29, -18, -93),
            look=Point3D(70, -76, -10),
            up=Vector3D(26, -10, -38),
            fov=74,
            aspect_ratio=7/4,
            near=8,
            far=23
        )
        n = s['n']
        u = s['u']
        v = s['v']
        vm = s['view_mat']
        pm = s['projection_mat']

        expected = (
            #u
            (
                0.45471427033982176,
                0.8872473567606278,
                0.07763414371655494
            ),
            #v
            (
                0.5518192679714115,
                -0.21223817998900443,
                -0.8065050839582169
            ),
            #n
            (
                -0.6990925745885297,
                0.409569387132674,
                -0.5861079160691713
            ),
            #vm
            {
                (0, 0): 0.45471427033982176,
                (0, 1): 0.8872473567606278,
                (0, 2): 0.07763414371655494,
                (0, 3): 36.37714162718574,

                (1, 0): 0.5518192679714115,
                (1, 1): -0.21223817998900443,
                (1, 2): -0.806505083958216,
                (1, 3): -62.822501276745314,

                (2, 0): -0.6990925745885297,
                (2, 1): 0.409569387132674,
                (2, 2): -0.5861079160691713,
                (2, 3): -67.40947188911215,

                (3, 0): 0,
                (3, 1): 0,
                (3, 2): 0,
                (3, 3): 1,
            },
            #pm
            {
                (0, 0): 0.7583113266402343,
                (0, 1): 0,
                (0, 2): 0,
                (0, 3): 0,

                (1, 0): 0,
                (1, 1): 1.32704482162041,
                (1, 2): 0,
                (1, 3): 0,

                (2, 0): 0,
                (2, 1): 0,
                (2, 2): -2.066666666666667,
                (2, 3): -24.533333333333335,

                (3, 0): 0,
                (3, 1): 0,
                (3, 2): -1,
                (3, 3): 0,
            }
        )

        # U
        self.assertAlmostEqual(u.x, expected[0][0], delta=d)
        self.assertAlmostEqual(u.y, expected[0][1], delta=d)
        self.assertAlmostEqual(u.z, expected[0][2], delta=d)

        # V
        self.assertAlmostEqual(v.x, expected[1][0], delta=d)
        self.assertAlmostEqual(v.y, expected[1][1], delta=d)
        self.assertAlmostEqual(v.z, expected[1][2], delta=d)

        # N
        self.assertAlmostEqual(n.x, expected[2][0], delta=d)
        self.assertAlmostEqual(n.y, expected[2][1], delta=d)
        self.assertAlmostEqual(n.z, expected[2][2], delta=d)

        # View matrix
        for vm_kv in expected[3].items():
            self.assertAlmostEqual(vm.get_element(*vm_kv[0]), vm_kv[1], delta=d)

        # Projection matrix
        for pm_kv in expected[4].items():
            self.assertAlmostEqual(pm.get_element(*pm_kv[0]), pm_kv[1], delta=d)

    def test_solve3(self):
        d = 1E-5
        s = solve(
            eye=Point3D(-1, -2, 4),
            look=Point3D(3, 1, -2),
            up=Vector3D(0, 1, 0),
            fov=30,
            aspect_ratio=16 / 9,
            near=1,
            far=11
        )
        n = s['n']
        u = s['u']
        v = s['v']
        vm = s['view_mat']
        pm = s['projection_mat']

        expected = (
            #u
            (
                3/sqrt(13),
                0,
                2/sqrt(13)
            ),
            #v
            (
                -6/sqrt(793),
                26/sqrt(793),
                9/sqrt(793)
            ),
            #n
            (
                -4/sqrt(61),
                -3/sqrt(61),
                6/sqrt(61)
            ),
            #vm
            {
                (0, 0): 3/sqrt(13),
                (0, 1): 0,
                (0, 2): 2/sqrt(13),
                (0, 3): -5/sqrt(13),

                (1, 0): -6/sqrt(793),
                (1, 1): 26/sqrt(793),
                (1, 2): 9/sqrt(793),
                (1, 3): 10/sqrt(793),

                (2, 0): -4/sqrt(61),
                (2, 1): -3/sqrt(61),
                (2, 2): 6/sqrt(61),
                (2, 3): -34/sqrt(61),

                (3, 0): 0,
                (3, 1): 0,
                (3, 2): 0,
                (3, 3): 1,
            },
            #pm
            {
                # T = tan(30 * pi / 360)
                # B = -tan(30 * pi / 360)
                # R = 16 * tan(30 * pi / 360) / 9
                # L = -16 * tan(30 * pi / 360) / 9
                (0, 0): 1 / (16 * tan(30 * pi / 360) / 9),
                (0, 1): 0,
                (0, 2): 0,
                (0, 3): 0,

                (1, 0): 0,
                (1, 1): 1 / (tan(30 * pi / 360)),
                (1, 2): 0,
                (1, 3): 0,

                (2, 0): 0,
                (2, 1): 0,
                (2, 2): -1.2,
                (2, 3): -2.2,

                (3, 0): 0,
                (3, 1): 0,
                (3, 2): -1,
                (3, 3): 0,
            }
        )

        # U
        self.assertAlmostEqual(u.x, expected[0][0], delta=d)
        self.assertAlmostEqual(u.y, expected[0][1], delta=d)
        self.assertAlmostEqual(u.z, expected[0][2], delta=d)

        # V
        self.assertAlmostEqual(v.x, expected[1][0], delta=d)
        self.assertAlmostEqual(v.y, expected[1][1], delta=d)
        self.assertAlmostEqual(v.z, expected[1][2], delta=d)

        # N
        self.assertAlmostEqual(n.x, expected[2][0], delta=d)
        self.assertAlmostEqual(n.y, expected[2][1], delta=d)
        self.assertAlmostEqual(n.z, expected[2][2], delta=d)

        # View matrix
        for vm_kv in expected[3].items():
            self.assertAlmostEqual(vm.get_element(*vm_kv[0]), vm_kv[1], delta=d)

        # Projection matrix
        for pm_kv in expected[4].items():
            self.assertAlmostEqual(pm.get_element(*pm_kv[0]), pm_kv[1], delta=d)

    def test_generate(self):
        for _i in range(100):
            g = generate()
            self.assertFalse(g['eye'] == g['look'])
            self.assertEqual((g['eye'].vector_to(g['look'])).dot_product(g['up']), 0)
            self.assertTrue(g['far'] > g['near'])