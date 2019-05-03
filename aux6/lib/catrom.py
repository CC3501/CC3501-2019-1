"""
Genera una spline de Catmull-Rom con varios vertices.

@author ppizarror
"""

import math


def __checkValidVertex(vertex):
    """
    Chequea que el vertice es valido.

    :param vertex:
    :return:
    """
    assert isinstance(vertex, list), 'Vertex {0} is not a list'.format(vertex)
    assert len(vertex) != 1, 'Vertex {0} cannot be a number'.format(vertex)
    assert len(vertex) == 2, 'Vertex [{0}] invalid'.format(','.join(str(x) for x in vertex))


def getSpline(vertices, fps):
    """
    Crea una spline a partir de una lista de vertices.

    :param vertices:
    :param fps:
    :return:
    """
    for i in vertices:
        __checkValidVertex(i)
    crs = []
    for x in range(0, len(vertices) - 3):
        points = [vertices[x], vertices[x + 1], vertices[x + 2], vertices[x + 3]]
        t = 0
        while t < len(points) - 3.0:
            p1 = 1
            p2 = 2
            p3 = 3
            p0 = 0

            t = t - math.floor(t)
            tt = t * t
            ttt = tt * t

            q1 = -ttt + 2.0 * tt - t
            q2 = 3.0 * ttt - 5.0 * tt + 2.0
            q3 = -3.0 * ttt + 4.0 * tt + t
            q4 = ttt - tt
            tx = 0.5 * (points[p0][0] * q1 + points[p1][0] * q2 + points[p2][0] * q3 + points[p3][0] * q4)
            ty = 0.5 * (points[p0][1] * q1 + points[p1][1] * q2 + points[p2][1] * q3 + points[p3][1] * q4)

            crs.append([tx, ty])
            t += 1 / fps
    return crs


def getSplineFixed(vertices, fps):
    """
    Crea una spline con los extremos fijos.

    :param vertices: Lista de vertices
    :type vertices: list
    :param fps: Velocidad de avance
    :type fps: float
    :return:
    """
    v = vertices.copy()
    v.insert(0, vertices[0])
    v.append(vertices[-1])
    return getSpline(v, fps)
