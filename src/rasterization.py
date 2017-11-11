import random

import os

from geometry import Point2D


def create_tex(problems, title):
    lis = []
    directory = os.path.dirname('tex/out/collision.tex')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('tex/out/rasterization.tex', 'w+') as f:
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
                gen['p'],
                gen['p1'],
                gen['v1'],
                gen['p2'],
                gen['v2'],
                gen['p3'],
                gen['v3']
            )
            lis.append(param)
            f.write(single_problem(param))
        f.write('\\section{Solutions}\n')
        for prob in enumerate(lis):
            f.write('\\subsection*{{Solution {0}}}\n'.format(prob[0]))
            f.write('\\label{{ssec:{0}}}\n'.format(prob[0]))
            f.write('\\addcontentsline{{toc}}{{subsection}}{{\\nameref{{ssec:{0}}}}}\n'.format(prob[0]))
            f.write('{0}\n'.format(solve(*prob[1])))
        f.write('\\end{document}\n')


def single_problem(parameters):
    return 'Three vertices of a triangle have been sent through the OpenGL pipeline.' \
           'They have the following pixel positions as well as values for the varying ' \
           'variable $v_d$\n' \
           '\\begin{{center}}\n' \
           '\\begin{{tabular}}{{c|c}}\n' \
           'Position & Values\\\\\n' \
           '\\hline\\\\\n' \
           '{1} & {2}\\\\\n' \
           '{3} & {4}\\\\\n' \
           '{5} & {6}\\\\\n' \
           '\\end{{tabular}}\n' \
           '\\end{{center}}\n' \
           'What will the fragment shader value of $v_d$ be set to at pixel {0}?\n'.format(*parameters)


def generate():
    problem = {}
    generate_points(problem)
    if coin_toss():
        problem['v1'] = (lambda z: tuple([z]*3))(random.randint(1, 150))
        problem['v2'] = (lambda z: tuple([z]*3))(random.randint(1, 150))
        problem['v3'] = (lambda z: tuple([z]*3))(random.randint(1, 150))
    else:
        problem['v1'] = (random.random(), random.random(), random.random())
        problem['v2'] = (random.random(), random.random(), random.random())
        problem['v3'] = (random.random(), random.random(), random.random())
    return problem


def generate_points(dic):
    """
    :type dic: dict
    """
    while True:
        p1 = Point2D(random.randint(0, 150), random.randint(0, 150), frac=False)
        p2 = Point2D(random.randint(0, 150), random.randint(0, 150), frac=False)
        p3 = Point2D(random.randint(0, 150), random.randint(0, 150), frac=False)
        if len({p1.x, p2.x, p3.x}) != 3:
            continue
        if len({p1.y, p2.y, p3.y}) != 3:
            continue
        if triangle_area(p1, p2, p3) < 10:
            continue
        min_x = min(p1.x, p2.x, p3.x)
        max_x = max(p1.x, p2.x, p3.x)
        if max_x - min_x <= 1:
            continue
        min_y = min(p1.y, p2.y, p3.y)
        max_y = max(p1.y, p2.y, p3.y)
        if max_y < min_y <= 1:
            continue
        for i in range(100):
            p = Point2D(random.randint(min_x + 1, max_x - 1), random.randint(min_y + 1, max_y - 1), frac=False)
            if p.inside_triangle(p1, p2, p3):
                dic['p'] = p
                dic['p1'] = p1
                dic['p2'] = p2
                dic['p3'] = p3
                return


def triangle_area(p1, p2, p3):
    """
    :type p1: Point2D
    :type p2: Point2D
    :type p3: Point2D
    """
    return 0.5 * abs((p1.x - p3.x) * (p2.y - p1.y) - (p1.x - p2.x) * (p3.y - p1.y))


def coin_toss():
    return random.randint(0, 1) == 1


def solve(p, p1, v1, p2, v2, p3, v3):
    """
    :type p: Point2D
    :type p1: Point2D
    :type v1: tuple of int or tuple of float
    :type p2: Point2D
    :type v2: tuple of int or tuple of float
    :type p3: Point2D
    :type v3: tuple of int or tuple of float
    """
    p_low, v_low = lowest(p1, p2, p3, v1, v2, v3)
    p_left, p_right = left_right(p_low, [p1, p2, p3])
    v_left = list(filter(lambda z: z[0] == p_left, [(p1, v1), (p2, v2), (p3, v3)]))[0][1]
    v_right = list(filter(lambda z: z[0] == p_right, [(p1, v1), (p2, v2), (p3, v3)]))[0][1]
    y_left_ratio = (p.y - p_low.y) / (p_left.y - p_low.y)
    y_right_ratio = (p.y - p_low.y) / (p_right.y - p_low.y)
    x_l = lerp(p_low.x, p_left.x, y_left_ratio)
    x_r = lerp(p_low.x, p_right.x, y_right_ratio)
    c_left = tuple([lerp(v_low[i], v_left[i], y_left_ratio) for i in range(3)])
    c_right = tuple([lerp(v_low[i], v_right[i], y_right_ratio) for i in range(3)])
    x_ratio = (p.x - x_l) / (x_r - x_l)
    return tuple([lerp(c_left[i], c_right[i], x_ratio) for i in range(3)])


def lerp(a, b, r):
    """
    :type a: int or float
    :type b: int or float
    :type r: int or float
    """
    return (1-r) * a + r * b


def lowest(p1, p2, p3, v1, v2, v3):
    """
    :type p1: Point2D
    :type p2: Point2D
    :type p3: Point2D
    :type v1: tuple of int or tuple of float
    :type v2: tuple of int or tuple of float
    :type v3: tuple of int or tuple of float
    """
    if p1.y < p2.y:
        if p1.y < p3.y:
            return p1, v1
        return p3, v3
    if p2.y < p3.y:
        return p2, v2
    return p3, v3


def left_right(p_low, pnts):
    """
    :type p_low: Point2D
    :type pnts: list of Point2D
    """
    pnts.remove(p_low)
    return tuple(sorted(pnts, key=lambda z: z.x, reverse=False))