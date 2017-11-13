import random

from geometry import Point2D


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


def solve2(win, pnt1, pnt2):
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
        pnt2, clipped = clip(win, pnt2, bits2, dx, dy)
        if not clipped:
            pnt1, clipped = clip(win, pnt1, bits1, dx, dy)
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

"""
g = generate()
for _g_ in g.items():
    print(_g_[0], _g_[1])
s = solve(g['win'], g['p1'], g['p2'])
for _x_ in s.items():
    print(_x_[0], end=' ')
    if type(_x_[1]) == tuple:
        print(_x_[1][0], _x_[1][1], _x_[1][2], _x_[1][3])
    else:
        print(_x_[1])"""