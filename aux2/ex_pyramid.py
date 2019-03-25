# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Drawing a Pyramid point to point.
Example of how to exchange the shader program.
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import transformations as tr
import sys

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
INT_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True
    useNight = False


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
        print("Toggle GL_FILL/GL_LINE")

    elif key == glfw.KEY_ENTER:
        controller.useNight = not controller.useNight
        print("Toggle shader program")

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


# A simple class container to reference a shape on GPU memory
class GPUShape:
    vao = 0
    vbo = 0
    ebo = 0
    size = 0


def drawShape(shaderProgram, shape):

    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # Setting up the location of the attributes position and color from the VBO
    # A vertex attribute has 3 integers for the position (each is 4 bytes),
    # and 3 numbers to represent the color (each is 4 bytes),
    # Henceforth, we have 3*4 + 3*4 = 24 bytes
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    
    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # Render the active element buffer with the active shader program
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)


def createSky():

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
    #   positions  colors
        -1, -1, 0, 1, 1, 1,
         1, -1, 0, 1, 1, 1,
         1,  1, 0, 0.5, 0.5, 1,
        -1,  1, 0, 0.5, 0.5, 1
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape


def createDunes():

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
    #   positions    colors
        -1,   -1, 0, 160/255.0, 134/255.0, 73/255.0,
         1,   -1, 0, 168/255.0, 121/255.0, 11/255.0,
         1, 0.05, 0, 244/255.0, 223/255.0, 66/255.0,
        -1,    0, 0,         1, 207/255.0, 96/255.0
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape


def createPiramid():

    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
    #   positions        colors
        -0.3, -0.2, 0.0,         1, 207/255.0,  96/255.0,
        0.7,  -0.2, 0.0, 168/255.0, 121/255.0,  11/255.0,
        0.2,   0.7, 0.0, 229/255.0, 214/255.0, 142/255.0,

        0.7,  -0.2, 0.0, 122/255.0, 89/255.0,   13/255.0,
        0.2,   0.7, 0.0, 122/255.0, 89/255.0,   13/255.0,
        0.9,  -0.1, 0.0, 122/255.0, 89/255.0,   13/255.0
        # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         3, 4, 5], dtype= np.uint32)
        
    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 600

    window = glfw.create_window(width, height, "Desert & Piramid", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Defining shaders for our pipeline
    vertex_shader = """
    #version 130
    in vec3 position;
    in vec3 color;

    out vec3 fragColor;

    void main()
    {
        fragColor = color;
        gl_Position = vec4(position, 1.0f);
    }
    """

    fragment_shader = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor, 1.0f);
    }
    """

    fragment_shader_night = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {
        outColor = vec4(fragColor.r * 0.2, fragColor.g * 0.2, (fragColor.b + 0.2) * 0.5, 1.0f);
    }
    """

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    shaderProgramNight = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_night, GL_FRAGMENT_SHADER))

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Creating shapes on GPU memory
    gpuSky = createSky()
    gpuDunes = createDunes()
    gpuPiramid = createPiramid()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing the shapes with a specific shader program depending on the controller state
        if controller.useNight:
            # Telling OpenGL to use our shader program
            glUseProgram(shaderProgramNight)

            drawShape(shaderProgramNight, gpuSky)
            drawShape(shaderProgramNight, gpuDunes)
            drawShape(shaderProgramNight, gpuPiramid)
        else:
            # Telling OpenGL to use our shader program
            glUseProgram(shaderProgram)

            drawShape(shaderProgram, gpuSky)
            drawShape(shaderProgram, gpuDunes)
            drawShape(shaderProgram, gpuPiramid)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()