# coding=utf-8
"""
Diego Donoso
Universidad de Chile, CC3501, 2019
"""
import numpy as np
import matplotlib.pyplot as mpl
import ex_curves
from mpl_toolkits.mplot3d import Axes3D
from ex_quad_controlled import *
from ex_aux_4 import *

if __name__ == "__main__":

    C1 = np.array([[0, 0]]).T
    C2 = np.array([[1, 0]]).T
    C3 = np.array([[1, 1]]).T
    C4 = np.array([[2, 1]]).T
    C5 = np.array([[2, 2]]).T
    c1 = fix_data(catmull_rom(C1, C2, C3, C4, C5))

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
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Creating shapes on GPU memory
    quads = []
    for i in range(10):
        quads.append(createQuad())
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # theta is modified an amount proportional to the time spent in a loop iteration

        # Drawing the Quad with the given transformation
        for i  in range(10):
            pos = int(len(c1) * i / 10)
            transform = tr.matmul([tr.scale(0.1, 0.1, 1), tr.translate(c1[pos][0], c1[pos][1], 0), tr.scale(0.8, 0.8, 0.8)])
            drawShape(shaderProgram, quads[i], transform)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()