
from ex_aux_4 import *

if __name__ == "__main__":
    """
    Example for Hermite curve
    """

    hermiteCurve = hermite_1_a()

    fig = mpl.figure()
    ax = fig.gca()

    plotCurve_2d(ax, hermiteCurve, "Hermite curve", (1, 0, 0))

    """
        Example for Bezier curve 
    """



    R0 = np.array([[1, 0]]).T
    R1 = np.array([[1, 0.5]]).T
    R2 = np.array([[0.8, 0.3]]).T
    R3 = np.array([[0, 1]]).T
    controlPoints = np.concatenate((R0, R1, R2, R3), axis=1)
    # plotCurve_2d(ax, hermite_bezier_b(), "Bezier curve")
    #ax.scatter(controlPoints[0, :], controlPoints[1, :], color=(1, 0, 0))

    """
        Example for catmull rom
    """
    C1 = np.array([[0, 0]]).T
    C2 = np.array([[1, 0]]).T
    C3 = np.array([[1, 1]]).T
    C4 = np.array([[2, 1]]).T
    C5 = np.array([[2, 2]]).T
    c1= catmull_rom(C1, C2, C3, C4, C5)
    #plotCurve_2d(ax, fix_data(c1), "curve 1")



    ax.set_xlabel('x')
    ax.set_ylabel('y')
    mpl.show()