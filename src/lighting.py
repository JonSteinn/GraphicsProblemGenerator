import random
from math import sqrt

import os

from geometry import Point3D, Vector3D


def create_tex(problems, title):
    lis = []
    directory = os.path.dirname('tex/out/collision.tex')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('tex/out/lighting.tex', 'w+') as f:
        with open('tex/template/start_content.tex', 'r') as tmp_f:
            for line in enumerate(tmp_f):
                if line[0] == 23:
                    f.write(line[1].replace('X', title))
                else:
                    f.write(line[1])
        for i in range(problems):
            gen = generate()
            f.write('\\subsection*{{Problem {0}}}\n'.format(i))
            f.write('\\label{{psec:{0}}}\n'.format(i))
            f.write('\\addcontentsline{{toc}}{{subsection}}{{\\nameref{{psec:{0}}}}}\n'.format(i))
            param = (
                gen['v_pos'],
                gen['v_norm'],
                gen['c_pos'],
                gen['l_pos'],
                gen['g_a'],
                gen['l_a'],
                gen['l_d'],
                gen['l_s'],
                gen['m_a'],
                gen['m_d'],
                gen['m_s'],
                gen['shine'],
            )
            lis.append(param)
            f.write(single_problem(param))
        f.write('\\section{Solutions}\n')
        for prob in enumerate(lis):
            f.write('\\subsection*{{Solution {0}}}\n'.format(prob[0]))
            f.write('\\label{{ssec:{0}}}\n'.format(prob[0]))
            f.write('\\addcontentsline{{toc}}{{subsection}}{{\\nameref{{ssec:{0}}}}}\n'.format(prob[0]))
            f.write('rgb = {0}\n'.format(solve(*prob[1])))
        f.write('\\end{document}\n')


def single_problem(parameters):
    return 'A single light is in the light model in an OpenGL program. ' \
           'It has the ambient values {5}, diffuse values {6}, specular ' \
           'values {7} and position {3}. There is also a global ambient ' \
           'factor of {4} in the light model. A camera is positioned in ' \
           '{2} and looks towards P. P has the color values: ambient {8}, ' \
           'diffuse {9} and specular {10}. It has a shininess value of ' \
           '{11}. It has the position {0} and a normal {1}. What will be ' \
           'the color value for P on the screen?\n'.format(*parameters)


def solve(v_pos, v_normal, c_pos, l_pos, g_a, l_a, l_d, l_s, m_a, m_d, m_s, shine):
    """
    :type v_pos: Point3D
    :type v_normal: Vector3D
    :type c_pos: Point3D
    :type l_pos: Point3D
    :type g_a: Color
    :type l_a: Color
    :type l_d: Color
    :type l_s: Color
    :type m_a: Color
    :type m_d: Color
    :type m_s: Color
    :type shine: float or int
    """
    v = v_pos.vector_to(c_pos)
    s = v_pos.vector_to(l_pos)
    h = v + s
    lamb = lambert(s, v_normal)
    phon = phong(h, v_normal)
    return Color(
        r=(l_a.r + g_a.r) * m_a.r + l_d.r * m_d.r * lamb + l_s.r * m_s.r * phon**shine,
        g=(l_a.g + g_a.g) * m_a.g + l_d.g * m_d.g * lamb + l_s.g * m_s.g * phon**shine,
        b=(l_a.b + g_a.b) * m_a.b + l_d.b * m_d.b * lamb + l_s.b * m_s.b * phon**shine,
    )


def generate():
    problem = {}
    while True:
        vertex_pos = Point3D(random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100))
        vertex_normal = Vector3D(random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))
        cam = Point3D(random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100))
        light = Point3D(random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100))
        if vertex_pos != cam and vertex_pos != light and cam != light:
            v = vertex_pos.vector_to(cam)
            s = vertex_pos.vector_to(light)
            h = v + s
            if vertex_normal.dot_self() == 0 or s.dot_self() == 0 or h.dot_self() == 0:
                continue
            problem['v_pos'] = vertex_pos
            problem['v_norm'] = vertex_normal
            problem['c_pos'] = cam
            problem['l_pos'] = light
            break
    while True:
        g_a = Color.random_color()
        l_a = Color.random_color()
        if g_a.r + l_a.r > 1.0 or g_a.b + l_a.b > 1.0 or g_a.g + l_a.g > 1.0:
            continue
        l_d = Color.random_color()
        l_s = Color.random_color()
        m_a = Color.random_color()
        m_d = Color.random_color()
        m_s = Color.random_color()
        shine = random.randint(10, 250)
        s = solve(problem['v_pos'], problem['v_norm'], problem['c_pos'], problem['l_pos'],
              g_a, l_a, l_d, l_s, m_a, m_d, m_s, shine)
        if s.r > 1.0 or s.g > 1.0 or s.b > 1.0:
            continue
        problem['g_a'] = g_a
        problem['l_a'] = l_a
        problem['l_d'] = l_d
        problem['l_s'] = l_s
        problem['m_a'] = m_a
        problem['m_d'] = m_d
        problem['m_s'] = m_s
        problem['shine'] = shine
        return problem


def lambert(s, m):
    """
    :type s: Vector3D
    :type m: Vector3D
    """
    return max(0.0, s.dot_product(m) / sqrt(s.dot_self() * m.dot_self()))


def phong(h, m):
    """
    :type h: Vector3D
    :type m: Vector3D
    """
    return max(0.0, h.dot_product(m) / sqrt(h.dot_self() * m.dot_self()))


class Color:
    def __init__(self, r, g, b):
        """
        :type r: float or int
        :type g: float or int
        :type b: float or int
        """
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return '({0},{1},{2})'.format(self.r, self.g, self.b)

    @staticmethod
    def random_color():
        return Color(
            r=float('{:.2f}'.format(random.random())),
            g=float('{:.2f}'.format(random.random())),
            b=float('{:.2f}'.format(random.random()))
        )