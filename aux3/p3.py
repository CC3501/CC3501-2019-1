# coding=utf-8
"""
Daniel Calderon - Pablo Pizarro R., CC3501, 2019-1
Controlling the movement of a quad
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
    x = 0.0
    y = 0.0
    theta = 0.0
    rotate = False
    fillPolygon = True


class ChessBoard:
    def __init__(self, w, h):
        # Creates a board centered of width w and height h
        self.w = w
        self.h = h

        # Tile sizes
        self.tile_size_x = self.w / 10
        self.tile_size_y = self.h / 10

        # Creating shapes on GPU memory
        self.gpuQuadBlack = createQuad([0, 0, 0])
        self.gpuQuadWhite = createQuad([1, 1, 1])

    def draw_board(self, shaderProgram):
        # Draw board
        colorBlack = False
        for i in range(10):  # y
            for j in range(10):  # x

                # Here we create the transform matrix
                cx, cy = self.get_coord(i, j)
                transform = tr.matmul([tr.scale(self.tile_size_x, self.tile_size_y, 1), tr.translate(cx, cy, 0)])

                # Draw the shape depending of the color
                if colorBlack:
                    drawShape(shaderProgram, self.gpuQuadBlack, transform)
                else:
                    drawShape(shaderProgram, self.gpuQuadWhite, transform)

                # Swap colors
                colorBlack = not colorBlack

            # Swap colors
            colorBlack = not colorBlack

    def get_coord(self, x, y):
        # Returns the coordinate of the element (x,y)
        a = -self.w / 2 + x * self.w / 10
        b = -self.h / 2 + y * self.h / 10
        return a, b

    def get_element_size(self):
        return self.w / 10, self.h / 10


# we will use the global controller as communication with the callback function
controller = Controller()


# noinspection PyUnusedLocal
def on_key(window, key, scancode, action, mods):
    global controller

    # Keep pressed buttons
    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_LEFT:
            controller.x -= 0.1
        elif key == glfw.KEY_RIGHT:
            controller.x += 0.1
        elif key == glfw.KEY_UP:
            controller.y += 0.1
        elif key == glfw.KEY_DOWN:
            controller.y -= 0.1

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_SPACE:
        controller.rotate = not controller.rotate

    elif key == glfw.KEY_1:
        controller.fillPolygon = not controller.fillPolygon

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


def drawShape(shaderProgram, shape, transform):
    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # updating the new transform attribute
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_FALSE, transform)

    # Describing how the data is stored in the VBO
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # This line tells the active shader program to render the active element buffer with the given size
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)


# Creates a quad with only 1 color
def createQuad(color):
    # Here the new shape will be stored
    gpuShape = GPUShape()

    # Defining locations and colors for each vertex of the shape

    vertexData = np.array([
        #   positions        colors
        -0.5, -0.5, 0.0, color[0], color[1], color[2],
        0.5, -0.5, 0.0, color[0], color[1], color[2],
        0.5, 0.5, 0.0, color[0], color[1], color[2],
        -0.5, 0.5, 0.0, color[0], color[1], color[2]
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype=np.uint32)

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


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Drawing a Quad via a EBO", None, None)

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

    uniform mat4 transform;

    void main()
    {
        fragColor = color;
        gl_Position = transform * vec4(position, 1.0f);
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

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Creating Chess board
    chessBoard = ChessBoard(1, 1)

    # Fill mode Polygon
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Get initial time
    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # theta is modified an amount proportional to the time spent in a loop iteration
        if controller.rotate:
            controller.theta += dt

        # Using transformations we will attempt to draw a 10x10 board
        chessBoard.draw_board(shaderProgram)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
