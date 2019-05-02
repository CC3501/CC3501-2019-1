"""
Genera una spline de CatRom con varios vertices
@author ppizarror
"""


def splineCatRom(puntos, fps):
    def frange(start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step

    vertices = []
    for t in frange(0, len(puntos) - 3, 1 / (2 * fps)):
        p1 = int(t) + 1
        p2 = p1 + 1
        p3 = p2 + 1
        p0 = p1 - 1

        t = t - int(t)
        tt = t * t
        ttt = tt * t

        q1 = -ttt + 2.0 * tt - t
        q2 = 3.0 * ttt - 5.0 * tt + 2.0
        q3 = -3.0 * ttt + 4 * tt + t
        q4 = ttt - tt

        tx = 0.5 * (puntos[p0][0] * q1 + puntos[p1][0] * q2 + puntos[p2][0] * q3 + puntos[p3][0] * q4)
        ty = 0.5 * (puntos[p0][1] * q1 + puntos[p1][1] * q2 + puntos[p2][1] * q3 + puntos[p3][1] * q4)
        if (tx, ty) not in vertices:
            vertices.append((tx, ty))
    return vertices
