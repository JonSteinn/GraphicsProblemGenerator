import random
from fractions import Fraction
from math import tan, pi

import os

from geometry import Vector3D, Point3D, Mat4


def create_tex(problems, title):
    lis = []
    directory = os.path.dirname('tex/out/collision.tex')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('tex/out/camera.tex', 'w+') as f:
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
            eye = gen['eye']
            look = gen['look']
            up = gen['up']
            fov = gen['fov']
            aspect_ratio = gen['aspect_ratio']
            near = gen['near']
            far = gen['far']
            lis.append((eye, look, up, fov, aspect_ratio.numerator / aspect_ratio.denominator, near, far))
            f.write(single_problem(eye, look, up, fov, aspect_ratio, near, far))
        f.write('\\section{Solutions}\n')
        for prob in enumerate(lis):
            f.write('\\subsection*{{Solution {0}}}\n'.format(prob[0]))
            f.write('\\label{{ssec:{0}}}\n'.format(prob[0]))
            f.write('\\addcontentsline{{toc}}{{subsection}}{{\\nameref{{ssec:{0}}}}}\n'.format(prob[0]))
            sol = solve(*prob[1])
            f.write("$u = {0}$\\\\\n$v = {1}$\\\\\n$n = {2}$\\\\\n".format(sol['u'], sol['v'], sol['n']))
            f.write(mat_to_tex(sol['view_mat']))
            f.write(mat_to_tex(sol['projection_mat']))
        f.write('\\end{document}\n')


def mat_to_tex(mat):
    s = '\\begin{align*}\\begin{bmatrix}'
    for i in range(4):
        s += '&'.join(map(str, mat.get_row(i))) + '\\\\'
    s += '\\end{bmatrix}\\end{align*}'
    return s


def single_problem(eye, look, up, fov, aspect_ratio, near, far):
    """
    :type eye: Point3D
    :type look: Point3D
    :type up: Vector3D
    :type fov: int or float
    :type aspect_ratio: int or float
    :type near: int or float
    :type far: int or float
    """
    return 'A camera is set up to be positioned in {0}. looking at the point {1}. ' \
           'It has an up vector {2}. Find the point of origin and vectors for the ' \
           'camera\'s coordinate frame. Set up the values in a matrix that represents' \
           ' this position and orientation of a camera. The camera should have a ' \
           'field of view of ${3}^\\circ$, an aspect ratio of {4}, a near plane at ' \
           '{5} and a far plane at {6}. Find the exact values for a matrix that ' \
           'calculates this camera.\n'.format(eye, look, up, fov, aspect_ratio, near, far)


def solve(eye, look, up, fov, aspect_ratio, near, far):
    """
    :type eye: Point3D
    :type look: Point3D
    :type up: Vector3D
    :type fov: int or float
    :type aspect_ratio: int or float
    :type near: int or float
    :type far: int or float
    """
    solution = {}
    n = look.vector_to(eye)
    u = Vector3D.cross_product(up, n)
    n.normalize()
    u.normalize()
    v = Vector3D.cross_product(n, u)
    solution['n'] = n
    solution['u'] = u
    solution['v'] = v
    view_mat = Mat4()
    view_mat.set_element(0, 0, u.x)
    view_mat.set_element(0, 1, u.y)
    view_mat.set_element(0, 2, u.z)
    view_mat.set_element(1, 0, v.x)
    view_mat.set_element(1, 1, v.y)
    view_mat.set_element(1, 2, v.z)
    view_mat.set_element(2, 0, n.x)
    view_mat.set_element(2, 1, n.y)
    view_mat.set_element(2, 2, n.z)
    neg_eye = eye.to_vector().scaled(-1)
    view_mat.set_element(0, 3, neg_eye.dot_product(u))
    view_mat.set_element(1, 3, neg_eye.dot_product(v))
    view_mat.set_element(2, 3, neg_eye.dot_product(n))
    solution['view_mat'] = view_mat
    t = near * tan(fov * pi / 360)
    b = -t
    r = t * aspect_ratio
    l = -r
    projection_mat = Mat4()
    projection_mat.set_element(0, 0, 2 * near / (r - l))
    projection_mat.set_element(0, 2, (r + l) / (r - l))
    projection_mat.set_element(1, 1, 2 * near / (t - b))
    projection_mat.set_element(1, 2, (t + b) / (t - b))
    projection_mat.set_element(2, 2, -(far + near) / (far - near))
    projection_mat.set_element(2, 3, -(2 * far * near) / (far - near))
    projection_mat.set_element(3, 2, -1)
    projection_mat.set_element(3, 3, 0)
    solution['projection_mat'] = projection_mat
    return solution


def generate():
    while True:
        problem = {'eye': Point3D(random.randint(-100, 100), random.randint(-100, 100),random.randint(-100, 100))}
        while True:
            look = Point3D(random.randint(-100, 100), random.randint(-100, 100),random.randint(-100, 100))
            if look != problem['eye']:
                problem['look'] = look
                break
        up = rand_normal(problem['look'].vector_to(problem['eye']), 100)
        if up is None:
            continue
        problem['up'] = up
        problem['fov'] = random.randint(50, 150)
        problem['aspect_ratio'] = Fraction(random.randint(1, 25), random.randint(1, 25))
        problem['near'] = random.randint(1, 25)
        problem['far'] = random.randint(problem['near'] + 1, 100)
        return problem


def rand_normal(vec, tries=10):
    """
    :type vec: Vector3D
    :type tries: int
    """
    for i in range(tries):
        a = random.randint(-50, 50)
        b = random.randint(-50, 50)
        if vec.z != 0:
            two = vec.x * a + vec.y * b
            c = two / (- vec.z)
            c = round(c)
            if two + c * vec.z == 0 and (a != 0 or b != 0 or c != 0):
                return Vector3D(a, b, c)
        elif vec.y != 0:
            two = vec.x * a + vec.z * b
            c = two / (- vec.y)
            c = round(c)
            if two + c * vec.y == 0 and (a != 0 or b != 0 or c != 0):
                return Vector3D(a, c, b)
        else:
            two = vec.z * a + vec.y * b
            c = two / (- vec.x)
            c = round(c)
            if two + c * vec.x == 0 and (a != 0 or b != 0 or c != 0):
                return Vector3D(c, b, a)
    return None