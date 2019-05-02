# coding=utf-8
"""
Crea un modelo usando curvas en 3D.

@author ppizarror
"""

# Library imports
import glfw
from OpenGL.GL import *
import numpy as np
import sys

import lib.transformations2 as tr2
import lib.basic_shapes as bs
import lib.easy_shaders as es

# Import extended shapes
import lib.basic_shapes_extended as bs_ext

# Import curve
import lib.catrom as catrom


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# Global controller as communication with the callback function
controller = Controller()


# noinspection PyUnusedLocal
def on_key(window_obj, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "C", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colores
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Create models
    gpuAxis = es.toGPUShape(bs.createAxis(10))
    obj_axis = bs_ext.MergedShape(gpuAxis, shader=colorShaderProgram)

    # Create one side of the wall
    vertices = [[1, 0], [0.9, 0.4], [0.5, 0.5], [0, 0.5]]
    curve = catrom.getSplineFixed(vertices, 10)

    obj_planeL = bs_ext.createColorPlaneFromCurve(curve, False, 0.6, 0.6, 0.6, center=(0, 0))
    obj_planeL.uniformScale(1.1)
    obj_planeL.rotationX(np.pi / 2)
    obj_planeL.rotationZ(-np.pi / 2)
    obj_planeL.translate(0.5, 0, 0)
    obj_planeL.setShader(colorShaderProgram)

    # Create other side of the wall
    obj_planeR = obj_planeL.clone()
    obj_planeR.translate(-1, 0, 0)

    # Create screen plane of model
    s1 = (0.5, 0, 0)
    s2 = (-0.5, 0, 0)
    s3 = (-0.5, 0.55, 0)
    s4 = (0.5, 0.55, 0)
    gpuTexturePlane = es.toGPUShape(bs_ext.createTexture4Vertex('shrek.png', s1, s2, s3, s4), GL_REPEAT, GL_LINEAR)
    planeS = bs_ext.MergedShape(gpuTexturePlane, shader=textureShaderProgram)
    planeS.rotationX(np.pi / 2)

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

        # Create camera
        view = tr2.lookAt(
            np.array([2, 2, 1]),
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )

        # Draw objects
        obj_axis.draw(view, projection, mode=GL_LINES)
        obj_planeL.draw(view, projection)
        obj_planeR.draw(view, projection)
        planeS.draw(view, projection)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
