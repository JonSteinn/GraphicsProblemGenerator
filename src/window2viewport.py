import random

from geometry import Point2D


def generate():
    while True:
        w = random_window()
        v = random_viewport()
        dvx = v[1] - v[0]
        dwx = w[1] - w[0]
        dvy = v[3] - v[2]
        dwy = w[3] - w[2]
        for _i in range(100):
            pnt = Point2D(random.randint(w[0], w[1]), random.randint(w[2], w[3]), False)
            if (dvx*pnt.x + v[0]*dwx - dvx*w[0]) % dwx == 0 and (dvy*pnt.y + v[2]*dwy - dvy*w[2]) % dwy == 0:
                return {
                    'w': w,
                    'v': v,
                    'p': pnt
                }


def random_viewport():
    return (
        0,
        next_multiple_of_n(random.randint(100, 2000), 10),
        0,
        next_multiple_of_n(random.randint(100, 2000), 10)
    )


def random_window():
    l = next_multiple_of_n(random.randint(-500, 495), 5)
    r = next_multiple_of_n(random.randint(l + 5, 500), 5)
    b = next_multiple_of_n(random.randint(-500, 495), 5)
    t = next_multiple_of_n(random.randint(b + 5, 500), 5)
    return l, r, b, t


def next_multiple_of_n(x, n):
    while x % n != 0:
        x += sign(x)
    return x


def sign(x):
    return -1 if x < 0 else 1


def solve(w, v, pnt):
    """
    :param: w: window (left, right, bottom, top)
    :type w: tuple of int
    :param: v: viewport (left, right, bottom, top)
    :type v: tuple of int
    :type pnt: Point2D
    """
    dvx = v[1] - v[0]
    dwx = w[1] - w[0]
    dvy = v[3] - v[2]
    dwy = w[3] - w[2]
    return Point2D(
        int((dvx * pnt.x + v[0] * dwx - dvx * w[0]) // dwx),
        int((dvy * pnt.y + v[2] * dwy - dvy * w[2]) // dwy),
        False
    )
