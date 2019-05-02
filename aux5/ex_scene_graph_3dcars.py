# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Drawing 3D cars via scene graph
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import transformations2 as tr2
import basic_shapes as bs
import scene_graph2 as sg
import easy_shaders as es


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


def createCar(r,g,b):

    gpuBlackQuad = es.toGPUShape(bs.createColorCube(0,0,0))
    gpuChasisQuad = es.toGPUShape(bs.createColorCube(r,g,b))
    
    # Cheating a single wheel
    wheel = sg.SceneGraphNode("wheel")
    wheel.transform = tr2.scale(0.2, 0.8, 0.2)
    wheel.childs += [gpuBlackQuad]

    wheelRotation = sg.SceneGraphNode("wheelRotation")
    wheelRotation.childs += [wheel]

    # Instanciating 2 wheels, for the front and back parts
    frontWheel = sg.SceneGraphNode("frontWheel")
    frontWheel.transform = tr2.translate(0.3,0,-0.3)
    frontWheel.childs += [wheelRotation]

    backWheel = sg.SceneGraphNode("backWheel")
    backWheel.transform = tr2.translate(-0.3,0,-0.3)
    backWheel.childs += [wheelRotation]
    
    # Creating the chasis of the car
    chasis = sg.SceneGraphNode("chasis")
    chasis.transform = tr2.scale(1,0.7,0.5)
    chasis.childs += [gpuChasisQuad]

    # All pieces together
    car = sg.SceneGraphNode("car")
    car.childs += [chasis]
    car.childs += [frontWheel]
    car.childs += [backWheel]

    return car


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "3D cars via scene graph", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    mvcPipeline = es.SimpleModelViewProjectionShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(mvcPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))
    redCarNode = createCar(1,0,0)
    blueCarNode = createCar(0,0,1)

    blueCarNode.transform = np.matmul(tr2.rotationZ(-np.pi/4), tr2.translate(3.0,0,0.5))

    # Using the same view and projection matrices in the whole application
    projection = tr2.perspective(45, float(width)/float(height), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    view = tr2.lookAt(
            np.array([5,5,7]),
            np.array([0,0,0]),
            np.array([0,0,1])
        )
    glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        if controller.showAxis:
            glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "model"), 1, GL_TRUE, tr2.identity())
            mvcPipeline.drawShape(gpuAxis, GL_LINES)

        # Moving the red car and rotating its wheels
        redCarNode.transform = tr2.translate(3 * np.sin( glfw.get_time() ),0,0.5)
        redWheelRotationNode = sg.findNode(redCarNode, "wheelRotation")
        redWheelRotationNode.transform = tr2.rotationY(-10 * glfw.get_time())

        # Uncomment to print the red car position on every iteration
        #print(sg.findPosition(redCarNode, "car"))

        # Drawing the Car
        sg.drawSceneGraphNode(redCarNode, mvcPipeline)
        sg.drawSceneGraphNode(blueCarNode, mvcPipeline)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()