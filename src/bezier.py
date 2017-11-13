import random
from math import factorial

import os

from geometry import Point3D


def create_tex(problems, title):
    lis = []
    directory = os.path.dirname('tex/out/bezier.tex')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('tex/out/bezier.tex', 'w+') as f:
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
            pnts = gen['pnts']
            t_s = gen['t_start']
            t_m = gen['t_mid']
            t_e = gen['t_end']
            lis.append((pnts, (t_m - t_s) / (t_e - t_s)))
            f.write(single_problem(pnts, t_s, t_m, t_e))
        f.write('\\section{Solutions}\n')
        for prob in enumerate(lis):
            f.write('\\subsection*{{Solution {0}}}\n'.format(prob[0]))
            f.write('\\label{{ssec:{0}}}\n'.format(prob[0]))
            f.write('\\addcontentsline{{toc}}{{subsection}}{{\\nameref{{ssec:{0}}}}}\n'.format(prob[0]))
            f.write('{0}\n'.format(solve(*prob[1])))
        f.write('\\end{document}\n')


def single_problem(pnts, t_s, t_m, t_e):
    """
    :type pnts: list of Point3D
    :type t_s: int or float
    :type t_m: int or float
    :type t_e: int or float
    """
    return 'An object is moved along a bezier curve with 4 control points. ' \
           'P1 = {0}, P2 = {1}, P3 = {2}, P4 = {3}. The motion should start ' \
           '{4} seconds after the program starts and it should end {7} seconds ' \
           'later, {5} seconds after the program starts. Where is the object\'s ' \
           'center {6} seconds after the program started?' \
           ''.format(pnts[0], pnts[1], pnts[2], pnts[3], t_s, t_e, t_m, t_e - t_s)


def generate():
    t_start = random.randint(0, 15)
    t_end = random.randint(t_start + 2, 100)
    t_mid = random.randint(t_start + 1, t_end - 1)
    while True:
        pnts = [
            Point3D(random.randint(-150, 150), random.randint(-150, 150), random.randint(-150, 150)),
            Point3D(random.randint(-150, 150), random.randint(-150, 150), random.randint(-150, 150)),
            Point3D(random.randint(-150, 150), random.randint(-150, 150), random.randint(-150, 150)),
            Point3D(random.randint(-150, 150), random.randint(-150, 150), random.randint(-150, 150))
        ]
        for pnt in pnts:
            if len(list(filter(lambda z: z == pnt, pnts))) > 1:
            	continue
        break
    return {'t_start': t_start, 't_mid': t_mid, 't_end': t_end, 'pnts': pnts}


def binom(n, k):
    """
    :type n: int
    :type k: int
    """
    return factorial(n) // factorial(k) // factorial(n - k)


def solve(pnts, time_ratio):
    """
    :type pnts: list of Point3D
    :type time_ratio: float
    """
    return sum(
        [pnts[i].scale(binom(3, i) * ((1 - time_ratio) ** (3 - i)) * (time_ratio ** i)) for i in range(4)],
        Point3D(0, 0, 0)
    )