import random

from geometry import Point2D, Vector2D


def create_tex(problems, title, sw_boundary, ne_boundary):
    lis = []
    with open('../tex/out/collision.tex', 'w+') as f:
        with open('../tex/template/start_content.tex', 'r') as tmp_f:
            for line in enumerate(tmp_f):
                if line[0] == 30:
                    f.write(line[1].replace('X', title))
                else:
                    f.write(line[1])
        for i in range(problems):
            gen = generate(sw_boundary, ne_boundary)
            f.write('\\subsection*{{Problem {0}}}\n'.format(i))
            f.write('\\label{{psec:{0}}}\n'.format(i))
            f.write('\\addcontentsline{{toc}}{{subsection}}{{\\nameref{{psec:{0}}}}}\n'.format(i))
            p = gen['pnt']
            p1 = gen['pnt1']
            p2 = gen['pnt2']
            v = gen['vec']
            lis.append((p, p1, p2, v))
            f.write(single_problem(p, p1, p2, v))
        f.write('\\section{Solutions}\n')
        for prob in enumerate(lis):
            f.write('\\subsection*{{Solution {0}}}\n'.format(prob[0]))
            f.write('\\label{{ssec:{0}}}\n'.format(prob[0]))
            f.write('\\addcontentsline{{toc}}{{subsection}}{{\\nameref{{ssec:{0}}}}}\n'.format(prob[0]))
            sol = solve(*prob[1])
            f.write("$t_\\text{{hit}} = {0}, p_\\text{{hit}} = {1}$ and $r = {2}$\n".format(
                sol['t_hit'], sol['p_hit'], sol['reflection']
            ))
        f.write('\\end{document}\n')


def single_problem(p, p1, p2, v):
    """
    :type p: Point2D
    :type p1: Point2D
    :type p2: Point2D
    :type v: Vector2D
    """
    return 'A line has end points ${0}$ and ${1}$. A particle starts at ${2}$ and ' \
           'travels along in the direction ${3}$. In which point does the path ' \
           'of the particle cross the line? If the particle is made to bounce ' \
           'off the line, what will it\'s new direction vector be?\n'.format(p1, p2, p, v)


def solve(pnt, pnt1, pnt2, vec):
    """
    :type pnt: Point2D
    :type pnt1: Point2D
    :type pnt2: Point2D
    :type vec: Vector2D
    """
    solution = {}
    n = pnt1.vector_to(pnt2).normal()
    pnt_pnt1 = pnt.vector_to(pnt1)
    denominator = n.dot_product(vec)
    if denominator == 0:
        solution['does_hit'] = False
        return solution
    t = n.dot_product(pnt_pnt1) / denominator
    solution['t_hit'] = t
    if t >= 0:
        p = pnt.move_by(vec.scaled(t))
        if pnt1.x == pnt2.x:
            solution['does_hit'] = min(pnt1.y, pnt2.y) <= p.y <= max(pnt1.y, pnt2.y)
        else:
            solution['does_hit'] = min(pnt1.x, pnt2.x) <= p.x <= max(pnt1.x, pnt2.x)
        if solution['does_hit']:
            solution['p_hit'] = p
            solution['reflection'] = vec - n.scaled(2 * n.dot_product(vec) / n.dot_self())
    else:
        solution['does_hit'] = False
    return solution


def generate(sw_boundary, ne_boundary):
    """
    :type sw_boundary: Point2D
    :type ne_boundary: Point2D
    """
    while True:
        problem = {'pnt1': Point2D(
            random.randint(sw_boundary.x, ne_boundary.x),
            random.randint(sw_boundary.y, ne_boundary.y)
        )}
        while True:
            pnt2 = Point2D(
                random.randint(sw_boundary.x, ne_boundary.x),
                random.randint(sw_boundary.y, ne_boundary.y)
            )
            if problem['pnt1'].x != pnt2.x and problem['pnt1'].y != pnt2.y:
                problem['pnt2'] = pnt2
                break
        while True:
            pnt = Point2D(
                random.randint(sw_boundary.x, ne_boundary.x),
                random.randint(sw_boundary.y, ne_boundary.y)
            )
            if not on_line(pnt, problem['pnt1'], problem['pnt2']):
                problem['pnt'] = pnt
                break
        for _i in range(50):
            v = Vector2D(random.randint(-10, 10), random.randint(-10, 10))
            if solve(problem['pnt'], problem['pnt1'], problem['pnt2'], v)['does_hit'] \
                    and v.x != 0 and v.y != 0:
                problem['vec'] = v
                return problem


def on_line(pnt, pnt1, pnt2):
    """
    :type pnt: Point2D
    :type pnt1: Point2D
    :type pnt2: Point2D
    """
    if pnt == pnt1 or pnt == pnt2:
        return True
    if pnt.x == pnt1.x or pnt.x == pnt2.x:
        return False
    if pnt1.slope_to(pnt) == pnt.slope_to(pnt2):
        return True
    if pnt.slope_to(pnt1) == pnt.slope_to(pnt2):
        return True
    if pnt1.slope_to(pnt) == pnt2.slope_to(pnt):
        return True
    return False