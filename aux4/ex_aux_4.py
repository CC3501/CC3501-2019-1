# coding=utf-8
"""
Diego Donoso
Universidad de Chile, CC3501, 2019
"""

import numpy as np
import matplotlib.pyplot as mpl
import ex_curves
from mpl_toolkits.mplot3d import Axes3D


def plotCurve_2d(ax, curve, label, color=(0, 0, 1)):
    xs = curve[:, 0]
    ys = curve[:, 1]

    ax.plot(xs, ys, label=label, color=color)


# M is the cubic curve matrix, N is the number of samples between 0 and 1
def evalCurve_2d(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)

    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 2), dtype=float)
    for i in range(len(ts)):
        T = ex_curves.generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T

    return curve

def evalCurve_2d_range(M, N, start, end):
    # The parameter t should move between 0 and 1
    ts = np.linspace(start, end, N)

    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 2), dtype=float)
    for i in range(len(ts)):
        T = ex_curves.generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T

    return curve

def hermite_1_a():
    P1 = np.array([[0, 0]]).T
    P2 = np.array([[1, 0]]).T
    T1 = np.array([[10, 0]]).T
    T2 = np.array([[0, 10]]).T
    GMh = ex_curves.hermiteMatrix(P1, P2, T1, T2)
    print(GMh)
    N = 50

    return evalCurve_2d(GMh, N)



def hermite_bezier_b():
    R0 = np.array([[1, 0]]).T
    R1 = np.array([[1, 0.5]]).T
    R2 = np.array([[0.8, 0.3]]).T
    R3 = np.array([[0,1]]).T

    N = 50

    GMb = ex_curves.bezierMatrix(R0, R1, R2, R3)

    return np.concatenate((hermite_1_a(), evalCurve_2d_range(GMb, N, 0, 1)))


def catmull_rom(p1, p2, p3, p4, p5):
    N = 50
    c1 = evalCurve_2d_range(catmull_matrix_p2_start(p1, p2, p3, p4), N, 0, 1)
    c2 = evalCurve_2d_range(catmull_matrix_p2_start(p2, p3, p4, p5), N, 0, 1)
    return np.concatenate((c1, c2))


def catmull_matrix_p2_start(p1, p2, p3, p4):
    G = np.concatenate((p1, p2, p3, p4), axis=1)

    Mc = 0.5 * np.array([[0, -1, 2, -1], [2, 0, -5, 3], [0, 1, 4, -3], [0, 0, -1, 1]])
    return np.matmul(G, Mc)

def fix_data(curve):
    max_x, min_x, max_y, min_y = get_max_min(curve)
    dist_x = max_x - min_x
    dist_y = max_y - min_y
    curve[:, 0] *= (2 / dist_x)
    curve[:, 1] *= (2 / dist_y)

    nmaxx, nminx, nmaxy, nminy = get_max_min(curve)
    curve[:, 0] -= (nminx + 1)
    curve[:, 1] -= (nminy + 1)
    return curve

def get_max_min(curve):
    ejex = curve[:, 0]
    ejey = curve[:, 1]
    max_x = ejex.max()
    min_x = ejex.min()
    max_y = ejey.max()
    min_y = ejey.min()
    return max_x, min_x, max_y, min_y

