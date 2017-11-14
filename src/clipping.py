import random
import os
from geometry import Point2D


def create_tex(problems, title):
    lis = []
    directory = os.path.dirname('tex/out/clipping.tex')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('tex/out/clipping.tex', 'w+') as f:
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
            win = gen['win']
            p1 = gen['p1']
            p2 = gen['p2']
            lis.append((win, p1, p2))
            f.write(single_problem(win, p1, p2))
        f.write('\\section{Solutions}\n')
        for prob in enumerate(lis):
            f.write('\\subsection*{{Solution {0}}}\n'.format(prob[0]))
            f.write('\\label{{ssec:{0}}}\n'.format(prob[0]))
            f.write('\\addcontentsline{{toc}}{{subsection}}{{\\nameref{{ssec:{0}}}}}\n'.format(prob[0]))
            w, p1, p2 = prob[1]
            f.write('{0}'.format(single_solution(solve(w, p1, p2))))
        f.write('\\end{document}\n')


def single_problem(window, pnt1, pnt2):
    """
    :type window: tuple of int
    :type pnt1: Point2D
    :type pnt2: Point2D
    """
    return 'Consider the window $W(l,r,b,t) = {0}$. ' \
           'A line has two endpoints, $P1={1}$ and $P2={2}$. ' \
           'Use the Cohen Sutherland clipping algorithm ' \
           'to clip the line against the window. ' \
           'Show the steps the algorithm takes\n'.format(window, pnt1, pnt2)


def single_solution(sol):
    """
    :type sol: dict
    """
    steps = sol['steps']
    dx = sol['dx']
    dy = sol['dy']
    s = 'dx = {0} and dy = {1}\\\\\n'.format(dx, dy)
    for i in range(steps):
        st = 'step{0}'.format(i)
        values = sol[st]
        s += '{0}:\\\\\np1 = {1}, b1 = {2}\\\\\np2 = {3}, b2 = {4}\\\\\n'.format(
            st, values[0], "".join(map(str, values[1])), values[2], "".join(map(str, values[3]))
        )
    s += '{0}\\\\\n'.format(sol['result'])
    return s


def generate():
    problem = {}
    l = random.randint(-500, 500)
    r = random.randint(l + 5, max(500, l + 100))
    b = random.randint(-500, 500)
    t = random.randint(b + 5, max(500, b + 100))
    win = (l, r, b, t)
    while True:
        p1 = Point2D(random.randint(-750, 750), random.randint(-750, 750), False)
        p2 = Point2D(random.randint(-750, 750), random.randint(-750, 750), False)
        b1 = get_bits(win, p1)
        b2 = get_bits(win, p2)
        if not trivial_accept(b1, b2) and not trivial_reject(b1, b2):
            problem['win'] = win
            problem['p1'] = p1
            problem['p2'] = p2
            return problem


def solve(win, pnt1, pnt2):
    """
    :param win: left-right-bottom-top
    :type win: tuple of int
    :type pnt1: Point2D
    :type pnt2: Point2D
    """
    dx = pnt2.x - pnt1.x
    dy = pnt2.y - pnt1.y
    steps = []
    solution = {'dx': dx, 'dy': dy}
    while True:
        bits1 = get_bits(win, pnt1)
        bits2 = get_bits(win, pnt2)
        steps.append((pnt1, bits1, pnt2, bits2))
        if trivial_accept(bits1, bits2):
            solution['result'] = 'trivial accept'
            break
        if trivial_reject(bits1, bits2):
            solution['result'] = 'trivial reject'
            break
        pnt1, clipped = clip(win, pnt1, bits1, dx, dy)
        if not clipped:
            pnt2, clipped = clip(win, pnt2, bits2, dx, dy)
    solution['steps'] = len(steps)
    for step in enumerate(steps):
        solution['step{0}'.format(step[0])] = step[1]
    return solution


def get_bits(win, pnt):
    """
    bits are [left, right, bottom, top] like window
    and are really just a list of 0s ans 1s.

    :param win: left-right-bottom-top
    :type win: tuple of int
    :type pnt: Point2D
    """
    bits = [0, 0, 0, 0]
    if pnt.x < win[0]:
        bits[0] = 1
    elif pnt.x > win[1]:
        bits[1] = 1
    if pnt.y < win[2]:
        bits[2] = 1
    elif pnt.y > win[3]:
        bits[3] = 1
    return bits


def trivial_accept(bits1, bits2):
    """
    :type bits1: list of int
    :type bits2: list of int
    """
    return 1 not in bits1 and 1 not in bits2


def trivial_reject(bits1, bits2):
    """
    :type bits1: list of int
    :type bits2: list of int
    """
    return 1 in [bit_and(bits1[i], bits2[i]) for i in range(4)]


def bit_and(b1, b2):
    """
    :type b1:
    :type b2:
    """
    if b1 == 1 and b2 == 1:
        return 1


def clip(win, pnt, bits, dx, dy):
    """
    :param win: left-right-bottom-top
    :type win: tuple of int
    :type pnt: Point2D
    :type bits: list of int
    :type dx: float or int
    :type dy: float or int
    """
    if bits[0] == 1:
        return Point2D(win[0], pnt.y + (win[0] - pnt.x) * dy / dx, False), True
    if bits[1] == 1:
        return Point2D(win[1], pnt.y + (win[1] - pnt.x) * dy / dx, False), True
    if bits[2] == 1:
        return Point2D(pnt.x + (win[2] - pnt.y) * dx / dy, win[2], False), True
    if bits[3] == 1:
        return Point2D(pnt.x + (win[3] - pnt.y) * dx / dy, win[3], False), True
    return pnt, False
