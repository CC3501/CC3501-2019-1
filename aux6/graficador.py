# coding=utf-8
"""
Graficador, genera una superficie 3D que representa una función.

@author ppizarror
"""

# Library imports
import glfw
from OpenGL.GL import *
import sys
import numpy as np

import lib.transformations2 as tr2
import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.camera as cam
from lib.mathlib import Point3
import lib.basic_shapes_extended as bs_ext
import lib.lights as light
from lib.colors import colorHSV


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# Global controller as communication with the callback function
controller = Controller()

# Create camera
camera = cam.CameraR(r=3.5, center=Point3())
camera.set_r_vel(0.1)


# noinspection PyUnusedLocal
def on_key(window_obj, key, scancode, action, mods):
    global controller

    if action == glfw.REPEAT or action == glfw.PRESS:
        # Move the camera position
        if key == glfw.KEY_LEFT:
            camera.rotate_phi(-4)
        elif key == glfw.KEY_RIGHT:
            camera.rotate_phi(4)
        elif key == glfw.KEY_UP:
            camera.rotate_theta(-4)
        elif key == glfw.KEY_DOWN:
            camera.rotate_theta(4)
        elif key == glfw.KEY_A:
            camera.close()
        elif key == glfw.KEY_D:
            camera.far()

        # Move the center of the camera
        elif key == glfw.KEY_I:
            camera.move_center_x(-0.05)
        elif key == glfw.KEY_K:
            camera.move_center_x(0.05)
        elif key == glfw.KEY_J:
            camera.move_center_y(-0.05)
        elif key == glfw.KEY_L:
            camera.move_center_y(0.05)
        elif key == glfw.KEY_U:
            camera.move_center_z(-0.05)
        elif key == glfw.KEY_O:
            camera.move_center_z(0.05)

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        sys.exit()


def f(x, y, fun):
    """
    Function that returns the value of z for each vertex.
    z = f(x,y)

    :param x:
    :param y:
    :param fun: Function number
    :return:
    """
    if fun == 0:
        return x * y
    elif fun == 1:  # Bumps
        return np.sin(5 * x) * np.cos(5 * y) / 5
    elif fun == 2:  # Pyramid
        return 1 - abs(x + y) - abs(y - x)
    elif fun == 3:  # Hills
        return 0.2 * (3 * np.exp(-(y + 1) ** 2 - x ** 2) * (x - 1) ** 2 - (-(x + 1) ** 2 - y ** 2)
                      / 3 + np.exp(-x ** 2 - y ** 2) * (10 * x ** 3 - 2 * x + 10 * y ** 5))
    elif fun == 4:  # Mantle
        return np.sin(10 * (x ** 2 + y ** 2)) / 10
    elif fun == 5:  # Intersecting fences
        return 0.75 / np.exp((x * 5) ** 2 * (y * 5) ** 2)
    elif fun == 6:  # Letter A
        return ((1 - np.sign(-x - 0.9 + abs(y * 2))) / 3 * (np.sign(0.9 - x) + 1) / 3) * \
               (np.sign(x + 0.65) + 1) / 2 - (
                       (1 - np.sign(-x - 0.39 + abs(y * 2))) / 3 * (np.sign(0.9 - x) + 1) / 3) + (
                       (1 - np.sign(-x - 0.39 + abs(y * 2))) / 3 * (np.sign(0.6 - x) + 1) / 3) * (
                       np.sign(x - 0.35) + 1) / 2
    else:
        return 0


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

    window = glfw.create_window(width, height, 'Graficador cuma', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colores
    phongPipeline = es.SimplePhongShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Create models
    gpuAxis = es.toGPUShape(bs.createAxis(1))
    obj_axis = bs_ext.AdvancedGPUShape(gpuAxis, shader=colorShaderProgram)

    # Create the grid of the system
    vertex_grid = []
    nx = 40
    ny = 40
    zlim = [0, 0]

    for i in range(nx):  # x
        for j in range(ny):  # y
            xp = -1 + 2 / (nx - 1) * j
            yp = -1 + 2 / (ny - 1) * i
            zp = f(xp, yp, 4)  # Function number 4
            zlim = [min(zp, zlim[0]), max(zp, zlim[1])]
            vertex_grid.append([xp, yp, zp])

    # Calculate the difference between max and min zvalue
    dz = abs(zlim[1] - zlim[0])
    zmean = (zlim[1] + zlim[0]) / 2
    dzf = min(1.0, 1 / (dz + 0.001))  # Height factor

    # Multiply all values for a factor, so the maximum height will be 1
    # Also the plot is centered
    for i in range(len(vertex_grid)):
        vertex_grid[i][2] = (vertex_grid[i][2] - zmean) * dzf
        zlim = [min(vertex_grid[i][2], zlim[0]), max(vertex_grid[i][2], zlim[1])]
    dz = abs(zlim[1] - zlim[0])

    # Force the color
    color_plot = {
        'enabled': False,
        'color': [1, 1, 1]
    }

    # Create the quads
    quad_shapes = []
    for i in range(nx - 1):  # x
        for j in range(ny - 1):
            # Select positions
            a = i * ny + j
            b = a + 1
            c = (i + 1) * ny + j + 1
            d = c - 1

            # Select vertices
            pa = vertex_grid[a]
            pb = vertex_grid[b]
            pc = vertex_grid[c]
            pd = vertex_grid[d]

            # Calculate color from interpolation
            zval = (pa[2] + pb[2] + pc[2] + pd[2]) / 4  # Average height of quad
            zf = (zval - zlim[0]) / (dz + 0.001)
            if not color_plot['enabled']:
                color = colorHSV(1 - zf)
            else:
                color = color_plot['color']

            # Create the figure
            quad_shapes.append(es.toGPUShape(bs_ext.create4VertexColorNormal(pa, pb, pc, pd,
                                                                             color[0], color[1], color[2])))

    # Create main object
    obj_main = bs_ext.AdvancedGPUShape(quad_shapes, shader=phongPipeline)

    # Create light
    obj_light = light.Light(phongPipeline, [0, 0, 6], [1, 1, 1])

    # Main loop
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Create projection
        # projection = tr2.ortho(-1, 1, -1, 1, 0.1, 100)
        projection = tr2.perspective(45, float(width) / float(height), 0.1, 100)

        # Get camera view matrix
        view = camera.get_view()

        # Place light
        obj_light.place()

        # Draw objects
        obj_axis.draw(view, projection, mode=GL_LINES)
        obj_main.draw(view, projection)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen
        glfw.swap_buffers(window)

    glfw.terminate()
