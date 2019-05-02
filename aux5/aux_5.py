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
# Add follow_car option
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = False
        self.follow_car = False
        self.lights = False


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

    elif key == glfw.KEY_C:
        controller.follow_car = not controller.follow_car

    else:
        print('Unknown key')

# Create car depending of isNormal value
def createCar(r1,g1,b1, r2, g2, b2, isNormal):
    if isNormal:
        gpuBlackQuad = es.toGPUShape(bs.createColorNormalsCube(0, 0, 0))
        gpuChasisQuad_color1 = es.toGPUShape(bs.createColorNormalsCube(r1, g1, b1))
        gpuChasisQuad_color2 = es.toGPUShape(bs.createColorNormalsCube(r2, g2, b2))
        gpuChasisPrism = es.toGPUShape(bs.createColorNormalTriangularPrism(153 / 255, 204 / 255, 255 / 255))
    else:
        gpuBlackQuad = es.toGPUShape(bs.createColorCube(0,0,0))
        gpuChasisQuad_color1 = es.toGPUShape(bs.createColorCube(r1,g1,b1))
        gpuChasisQuad_color2 = es.toGPUShape(bs.createColorCube(r2,g2,b2))
        gpuChasisPrism = es.toGPUShape(bs.createColorTriangularPrism(153/255, 204/255, 255/255))
    
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
    
    # Creating the bottom chasis of the car
    bot_chasis = sg.SceneGraphNode("bot_chasis")
    bot_chasis.transform = tr2.scale(1.1,0.7,0.1)
    bot_chasis.childs += [gpuChasisQuad_color1]

    # Moving bottom chasis
    moved_b_chasis = sg.SceneGraphNode("moved_b_chasis")
    moved_b_chasis.transform = tr2.translate(0, 0, -0.2)
    moved_b_chasis.childs += [bot_chasis]

    # Creating light support
    light_s = sg.SceneGraphNode("light_s")
    light_s.transform = tr2.scale(1, 0.1, 0.1)
    light_s.childs += [gpuChasisQuad_color2]

    # Creating right light
    right_light = sg.SceneGraphNode("right_light")
    right_light.transform = tr2.translate(0, 0.25, 0)
    right_light.childs += [light_s]

    # Moving right light
    left_light = sg.SceneGraphNode("left_light")
    left_light.transform = tr2.translate(0, -0.25, 0)
    left_light.childs += [light_s]

    # Creating center chasis
    center_chasis = sg.SceneGraphNode("center_chasis")
    center_chasis.transform = tr2.scale(1, 0.4, 0.15)
    center_chasis.childs += [gpuChasisQuad_color1]

    # Moving center chasis
    m_center_chasis = sg.SceneGraphNode("m_center_chasis")
    m_center_chasis.transform = tr2.translate(0.05, 0, 0)
    m_center_chasis.childs += [center_chasis]

    # Creating center quad
    center_quad = sg.SceneGraphNode("center_quad")
    center_quad.transform = tr2.scale(0.26, 0.5, 0.2)
    center_quad.childs += [gpuChasisQuad_color2]

    # Moving center quad
    m_center_quad = sg.SceneGraphNode("m_center_quad")
    m_center_quad.transform = tr2.translate(-0.07, 0, 0.1)
    m_center_quad.childs += [center_quad]

    # Creating front wind shield
    f_wind_shield = sg.SceneGraphNode("f_wind_shield")
    f_wind_shield.transform = tr2.scale(0.25, 0.5, 0.2)
    f_wind_shield.childs += [gpuChasisPrism]

    # Moving front wind shield
    m_f_wind_shield = sg.SceneGraphNode("m_f_wind_shield")
    m_f_wind_shield.transform = tr2.translate(0.2, 0, 0.1)
    m_f_wind_shield.childs += [f_wind_shield]

    # Creating back wind shield
    b_wind_shield = sg.SceneGraphNode("b_wind_shield")
    b_wind_shield.transform = tr2.scale(0.25, 0.5, 0.2)
    b_wind_shield.childs += [gpuChasisPrism]

    # Rotate back wind shield
    r_b_wind_shield = sg.SceneGraphNode("r_b_wind_shield")
    r_b_wind_shield.transform = tr2.rotationZ(np.pi)
    r_b_wind_shield.childs += [b_wind_shield]

    # Moving back wind shield
    m_b_wind_shield = sg.SceneGraphNode("m_b_wind_shield")
    m_b_wind_shield.transform = tr2.translate(-0.3, 0, 0.1)
    m_b_wind_shield.childs += [r_b_wind_shield]

    # Joining chasis parts
    complete_chasis = sg.SceneGraphNode("complete_chasis")
    complete_chasis.childs += [moved_b_chasis]
    complete_chasis.childs += [right_light]
    complete_chasis.childs += [left_light]
    complete_chasis.childs += [m_center_chasis]
    complete_chasis.childs += [m_center_quad]
    complete_chasis.childs += [m_b_wind_shield]
    complete_chasis.childs += [m_f_wind_shield]


    # All pieces together
    car = sg.SceneGraphNode("car")
    car.childs += [complete_chasis]
    car.childs += [frontWheel]
    car.childs += [backWheel]

    return car

# Create ground with textures
def createGround():
    gpuGround_texture = es.toGPUShape(bs.createTextureQuad("ground.jpg"), GL_REPEAT, GL_NEAREST)
    ground_scaled = sg.SceneGraphNode("ground_scaled")
    ground_scaled.transform = tr2.scale(10, 10, 10)
    ground_scaled.childs += [gpuGround_texture]

    ground_rotated = sg.SceneGraphNode("ground_rotated_x")
    ground_rotated.transform = tr2.rotationX(0)
    ground_rotated.childs += [ground_scaled]

    ground = sg.SceneGraphNode("ground")
    ground.transform = tr2.translate(0, 0, 0)
    ground.childs += [ground_rotated]

    return ground

# Create image of ricardo
def createRicardo_1(filename):
    gpuAirport_texture = es.toGPUShape(bs.createTextureQuad(filename), GL_REPEAT, GL_LINEAR)
    ricardo_1_scaled = sg.SceneGraphNode("ricardo_scaled")
    ricardo_1_scaled.transform = tr2.scale(3, 3, 3)
    ricardo_1_scaled.childs += [gpuAirport_texture]

    ricardo_1_rotated = sg.SceneGraphNode("ricardo_rotated")
    ricardo_1_rotated.transform = np.matmul(tr2.rotationX(np.pi / 2), tr2.rotationY(np.pi / 2))
    ricardo_1_rotated.childs += [ricardo_1_scaled]

    ricardo_1 = sg.SceneGraphNode("ricardo")
    ricardo_1.transform = tr2.translate(6, 0, 1)
    ricardo_1.childs += [ricardo_1_rotated]

    return ricardo_1

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 1000
    height = 1000

    window = glfw.create_window(width, height, "Aux 5", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with shaders (simple, texture and lights)
    mvcPipeline = es.SimpleModelViewProjectionShaderProgram()
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    phongPipeline = es.SimplePhongShaderProgram()




    # Setting up the clear screen color
    glClearColor(1, 1, 1, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))
    redCarNode = createCar(252/255,246/255,246/255, 255/255, 153/255, 153/255, controller.lights)
    blueCarNode = createCar(252/255,246/255,246/255, 0, 76/255, 153/255, False)
    groundNode = createGround()
    ricardoNode = createRicardo_1("ricardo1.png")
    blueCarNode.transform = np.matmul(tr2.rotationZ(-np.pi/4), tr2.translate(3.0,0,0.5))

    # Define radius of the circumference
    r = 2

    # lookAt of normal camera
    normal_view = tr2.lookAt(
            np.array([5, 5, 6]),
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )


    while not glfw.window_should_close(window):

        # Telling OpenGL to use our shader program
        glUseProgram(mvcPipeline.shaderProgram)
        # Using the same view and projection matrices in the whole application
        projection = tr2.perspective(45, float(width) / float(height), 0.1, 100)
        glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        # Calculate coordinates of the camera and redCar
        u_px = np.cos(glfw.get_time())
        u_py = np.sin(glfw.get_time())
        x = r * u_px
        y = r * u_py

        u_tx = -u_py
        u_ty = u_px

        if controller.follow_car:
            # moving camera
            normal_view = tr2.lookAt(
                np.array([x, y, 1]),
                np.array([x + r * u_tx, y + r * u_ty, 1]),
                np.array([0, 0, 1])
            )
        else:
            # static camera
            normal_view = tr2.lookAt(
            np.array([5, 5, 6]),
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
            )

        glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "view"), 1, GL_TRUE, normal_view)

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
        redCarNode.transform = np.matmul(tr2.translate(0, 0, 0.5), tr2.translate(x, y, 0))
        redCarNode.transform = np.matmul(redCarNode.transform, tr2.rotationZ(glfw.get_time() + np.pi / 2))
        redWheelRotationNode = sg.findNode(redCarNode, "wheelRotation")
        redWheelRotationNode.transform = tr2.rotationY(10 * glfw.get_time())

        # Uncomment to print the red car position on every iteration
        #print(sg.findPosition(redCarNode, "car"))

        # Drawing the Car
        sg.drawSceneGraphNode(blueCarNode, mvcPipeline)
        if not controller.lights:
            sg.drawSceneGraphNode(redCarNode, mvcPipeline)


        else:
            # Drawing redCar using light shader
            glUseProgram(phongPipeline.shaderProgram)

            # Setting all uniform shader variables
            glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "lightColor"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "lightPos"), -5, -5, 5)
            glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "viewPos"), 5, 5, 6)
            glUniform1ui(glGetUniformLocation(phongPipeline.shaderProgram, "shininess"), 100)
            glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "constantAttenuation"), 0.001)
            glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "linearAttenuation"), 0.1)
            glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

            glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "view"), 1, GL_TRUE, normal_view)

            sg.drawSceneGraphNode(redCarNode, phongPipeline)


        # Drawing ground and ricardo using texture shader
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, normal_view)
        # Drawing ground
        sg.drawSceneGraphNode(groundNode, textureShaderProgram)
        sg.drawSceneGraphNode(ricardoNode, textureShaderProgram)


        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()