# coding=utf-8
"""
Crea un cilindro en 3D.

@author ppizarror
"""

# Library imports
import glfw
from OpenGL.GL import *
import sys

import lib.transformations2 as tr2
import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.camera as cam
from lib.mathlib import Point3
import numpy as np

# Import extended shapes
import lib.basic_shapes_extended as bs_ext

# Import lights
import lib.lights as light


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True


# Global controller as communication with the callback function
controller = Controller()

# Create camera
camera = cam.CameraR(r=3, center=Point3())
camera.set_r_vel(0.1)


# noinspection PyUnusedLocal
def on_key(window_obj, key, scancode, action, mods):
    global controller
    global obj_light

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

    elif key == glfw.KEY_Z:
        obj_light.change_color(np.random.random(), np.random.random(), np.random.random())


if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

    window = glfw.create_window(width, height, 'Cilindro bonito', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colores
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    phongPipeline = es.SimplePhongShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Create models
    gpuAxis = es.toGPUShape(bs.createAxis(1))
    obj_axis = bs_ext.AdvancedGPUShape(gpuAxis, shader=colorShaderProgram)

    # Create cilynder, the objective is create many cuads from the bottom, top and
    # mantle. The cilynder is parametrized using an angle theta, a radius r and
    # the height
    h = 1
    r = 0.25

    # Latitude and longitude of the cylinder, latitude subdivides theta, longitude
    # subdivides h
    lat = 20
    lon = 20

    # Angle step
    dang = 2 * np.pi / lat

    # Color
    color = {
        'r': 1,  # Red
        'g': 0,  # Green
        'b': 0,  # Blue
    }

    cylinder_shape = []  # Store shapes

    # Create mantle
    for i in range(lon):  # Vertical component
        for j in range(lat):  # Horizontal component

            # Angle on step j
            ang = dang * j

            # Here we create a quad from 4 vertices
            #
            #    a/---- b/
            #    |      |
            #    d ---- c
            a = [r * np.cos(ang), r * np.sin(ang), h / lon * (i + 1)]
            b = [r * np.cos(ang + dang), r * np.sin(ang + dang), h / lon * (i + 1)]
            c = [r * np.cos(ang + dang), r * np.sin(ang + dang), h / lon * i]
            d = [r * np.cos(ang), r * np.sin(ang), h / lon * i]

            # Create quad
            shape = bs_ext.create4VertexColorNormal(a, b, c, d, color['r'], color['g'], color['b'])
            cylinder_shape.append(es.toGPUShape(shape))

    # Add the two covers
    for j in range(lat):
        ang = dang * j

        # Bottom
        a = [0, 0, 0]
        b = [r * np.cos(ang), r * np.sin(ang), 0]
        c = [r * np.cos(ang + dang), r * np.sin(ang + dang), 0]
        shape = bs_ext.createTriangleColorNormal(c, b, a, color['r'], color['g'], color['b'])
        cylinder_shape.append(es.toGPUShape(shape))

        # Top
        a = [0, 0, h]
        b = [r * np.cos(ang), r * np.sin(ang), h]
        c = [r * np.cos(ang + dang), r * np.sin(ang + dang), h]
        shape = bs_ext.createTriangleColorNormal(c, b, a, color['r'], color['g'], color['b'])
        cylinder_shape.append(es.toGPUShape(shape))

    # Create cylinder object
    obj_cylinder = bs_ext.AdvancedGPUShape(cylinder_shape, shader=phongPipeline)

    # Create light
    obj_light = light.Light(shader=phongPipeline, position=[5, 5, 5], color=[1, 1, 1])

    # Main execution loop
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
        obj_cylinder.draw(view, projection)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen
        glfw.swap_buffers(window)

    glfw.terminate()
