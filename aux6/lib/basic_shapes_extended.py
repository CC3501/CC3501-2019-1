"""
Archivo utilitario creado para la auxiliar 6, permite definir más figuras
con texturas

@author ppizarror
"""

from lib.basic_shapes import Shape as _Shape
from lib.easy_shaders import GPUShape as _GPUShape
from lib.easy_shaders import toGPUShape as _toGPUShape
from OpenGL.GL import GL_POLYGON as _GL_POLYGON
from OpenGL.GL import glUniformMatrix4fv as _glUniformMatrix4fv
from OpenGL.GL import glGetUniformLocation as _glGetUniformLocation
from OpenGL.GL import GL_TRUE as _GL_TRUE
from OpenGL.GL import GL_TRIANGLES as _GL_TRIANGLES
from OpenGL.GL import glUseProgram as _glUseProgram
import lib.transformations2 as _tr
import lib.tripy as _tripy
from lib.mathlib import _normal_3_points as _normal3


# Merged shape
class AdvancedGPUShape:
    def __init__(self, shapes, model=_tr.identity(), enabled=True, shader=None):
        """
        Constructor.

        :param shapes: List or GPUShape object
        :param model: Basic model transformation matrix
        :param enabled: Indicates if the shape is enabled or not
        :param shader: Shader program
        """
        if not isinstance(shapes, list):
            shapes = [shapes]
        for i in range(len(shapes)):
            if not isinstance(shapes[i], _GPUShape):
                raise Exception('Object {0} of shapes list is not GPUShape instance'.format(i))

        self._shapes = shapes
        self._model = model
        self._modelPrev = None
        self._enabled = enabled
        self._shader = shader

    def setShader(self, shader):
        """
        Set shader.

        :param shader:
        :return:
        """
        self._shader = shader

    def translate(self, tx=0, ty=0, tz=0):
        """
        Translate model.

        :param tx:
        :param ty:
        :param tz:
        :return:
        """
        self._model = _tr.matmul([_tr.translate(tx, ty, tz), self._model])

    def scale(self, sx=1, sy=1, sz=1):
        """
        Scale model.

        :param sx:
        :param sy:
        :param sz:
        :return:
        """
        self._model = _tr.matmul([_tr.scale(sx, sy, sz), self._model])

    def uniformScale(self, s=1):
        """
        Uniform scale model.

        :param s:
        :return:
        """
        self._model = _tr.matmul([_tr.uniformScale(s), self._model])

    def rotationX(self, theta=0):
        """
        Rotate model.

        :param theta:
        :return:
        """
        self._model = _tr.matmul([_tr.rotationX(theta), self._model])

    def rotationY(self, theta=0):
        """
        Rotate model.

        :param theta:
        :return:
        """
        self._model = _tr.matmul([_tr.rotationY(theta), self._model])

    def rotationZ(self, theta=0):
        """
        Rotate model.

        :param theta:
        :return:
        """
        self._model = _tr.matmul([_tr.rotationZ(theta), self._model])

    def rotationA(self, theta, axis):
        """
        Rotate model.

        :param theta:
        :param axis:
        :return:
        """
        self._model = _tr.matmul([_tr.rotationA(theta, axis), self._model])

    def shearing(self, xy=0, yx=0, xz=0, zx=0, yz=0, zy=0):
        """
        Apply shear to model.

        :param xy:
        :param yx:
        :param xz:
        :param zx:
        :param yz:
        :param zy:
        :return:
        """
        self._model = _tr.matmul([_tr.shearing(xy, yx, xz, zx, yz, zy), self._model])

    def applyTemporalTransform(self, t):
        """
        Apply temporal transform to model until drawing.

        :param t:
        :return:
        """
        self._modelPrev = self._model
        self._model = _tr.matmul([t, self._model])

    def draw(self, view, projection, mode=_GL_TRIANGLES, shader=None, usemodel=True):
        """
        Draw model.

        :param view:
        :param projection:
        :param mode:
        :param shader:
        :param usemodel:
        :return:
        """
        if not self._enabled:
            return
        if mode is None:
            mode = _GL_POLYGON
        if shader is None:
            if self._shader is None:
                raise Exception('MergedShape shader is not set')
            shader = self._shader
        _glUseProgram(shader.shaderProgram)
        if usemodel:
            _glUniformMatrix4fv(_glGetUniformLocation(shader.shaderProgram, 'model'), 1, _GL_TRUE, self._model)
        _glUniformMatrix4fv(_glGetUniformLocation(shader.shaderProgram, 'projection'), 1, _GL_TRUE, projection)
        _glUniformMatrix4fv(_glGetUniformLocation(shader.shaderProgram, 'view'), 1, _GL_TRUE, view)
        for i in self._shapes:
            shader.drawShape(i, mode)
        if self._modelPrev is not None:
            self._model = self._modelPrev
            self._modelPrev = None

    def disable(self):
        """
        Disable the model.

        :return:
        """
        self._enabled = False

    def enable(self):
        """
        Enable the model.

        :return:
        """
        self._enabled = True

    def clone(self):
        """
        Clone the model.

        :return:
        """
        return AdvancedGPUShape(self._shapes.copy(), self._model, enabled=self._enabled, shader=self._shader)


def __vertexUnpack3(vertex):
    """
    Extend vertex to 3 dimension.

    :param vertex:
    :return:
    """
    if len(vertex) == 2:
        vertex = vertex + (0,)
    return vertex


def createColorPlaneFromCurve(curve, triangulate, r, g, b, center=None):
    """
    Creates a plane from a curve and a center.

    :param curve: Curve vertex list
    :param triangulate: Create plane from curve triangulation
    :param center: Center position
    :param r: Red color
    :param g: Green color
    :param b: Blue color
    :return: Merged shape
    :rtype: AdvancedGPUShape
    """
    shapes = []

    # Use delaunay triangulation
    if triangulate:
        k = []
        for i in curve:
            k.append((i[0], i[1]))
        tri = _tripy.earclip(k)
        for i in tri:
            x1, y1 = i[0]
            x2, y2 = i[1]
            x3, y3 = i[2]
            shape = createTriangleColor((x1, y1, 0), (x2, y2, 0), (x3, y3, 0), r, g, b)
            shapes.append(_toGPUShape(shape))
    else:
        if center is None:
            center = curve[0]
        for i in range(0, len(curve) - 1):
            x1, y1 = curve[i]
            x2, y2 = curve[(i + 1) % len(curve)]
            c1, c2 = center
            shape = createTriangleColor((x1, y1, 0), (x2, y2, 0), (c1, c2, 0), r, g, b)
            shapes.append(_toGPUShape(shape))
    return AdvancedGPUShape(shapes)


def create4VertexTexture(image_filename, p1, p2, p3, p4, nx=1, ny=1):
    """
    Creates a 4-vertex poly with texture.

    :param image_filename: Image
    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param p4: Vertex (x,y,z)
    :param nx: Texture coord pos
    :param ny: Texture coord pos
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)
    p4 = __vertexUnpack3(p4)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    x4, y4, z4 = p4

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        x1, y1, z1, 0, 0,
        x2, y2, z2, nx, 0,
        x3, y3, z3, nx, ny,
        x4, y4, z4, 0, ny
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return _Shape(vertices, indices, image_filename)


def create4VertexTextureNormal(image_filename, p1, p2, p3, p4, nx=1, ny=1):
    """
    Creates a 4-vertex poly with texture.

    :param image_filename: Image
    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param p4: Vertex (x,y,z)
    :param nx: Texture coord pos
    :param ny: Texture coord pos
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)
    p4 = __vertexUnpack3(p4)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    x4, y4, z4 = p4

    # Calculate the normal
    normal = _normal3(p3, p2, p1)

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        x1, y1, z1, 0, 0, normal.get_x(), normal.get_y(), normal.get_z(),
        x2, y2, z2, nx, 0, normal.get_x(), normal.get_y(), normal.get_z(),
        x3, y3, z3, nx, ny, normal.get_x(), normal.get_y(), normal.get_z(),
        x4, y4, z4, 0, ny, normal.get_x(), normal.get_y(), normal.get_z()
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return _Shape(vertices, indices, image_filename)


def create4VertexColor(p1, p2, p3, p4, r, g, b):
    """
    Creates a 4-vertex poly with color.

    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param p4: Vertex (x,y,z)
    :param r: Red color
    :param g: Green color
    :param b: Blue color
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)
    p4 = __vertexUnpack3(p4)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    x4, y4, z4 = p4

    # Defining locations and color
    vertices = [
        # X, Y,  Z, R, G, B,
        x1, y1, z1, r, g, b,
        x2, y2, z2, r, g, b,
        x3, y3, z3, r, g, b,
        x4, y4, z4, r, g, b
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0
    ]

    return _Shape(vertices, indices)


def create4VertexColorNormal(p1, p2, p3, p4, r, g, b):
    """
    Creates a 4-vertex figure with color and normals.

    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param p4: Vertex (x,y,z)
    :param r: Red color
    :param g: Green color
    :param b: Blue color
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)
    p4 = __vertexUnpack3(p4)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3
    x4, y4, z4 = p4

    # Calculate the normal
    normal = _normal3(p3, p2, p1)

    # Defining locations and color
    vertices = [
        # X, Y,  Z, R, G, B,
        x1, y1, z1, r, g, b, normal.get_x(), normal.get_y(), normal.get_z(),
        x2, y2, z2, r, g, b, normal.get_x(), normal.get_y(), normal.get_z(),
        x3, y3, z3, r, g, b, normal.get_x(), normal.get_y(), normal.get_z(),
        x4, y4, z4, r, g, b, normal.get_x(), normal.get_y(), normal.get_z()
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0
    ]

    return _Shape(vertices, indices)


def createTriangleTexture(image_filename, p1, p2, p3, nx=1, ny=1):
    """
    Creates a triangle with textures.

    :param image_filename: Image
    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param nx: Texture coord pos
    :param ny: Texture coord pos
    :return:
    """
    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        # X, Y,  Z,   U,   V
        x1, y1, z1, (nx + ny) / 2, nx,
        x2, y2, z2, 0.0, 0.0,
        x3, y3, z3, ny, 0.0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2
    ]

    return _Shape(vertices, indices, image_filename)


def createTriangleTextureNormal(image_filename, p1, p2, p3, nx=1, ny=1):
    """
    Creates a triangle with textures.

    :param image_filename: Image
    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param nx: Texture coord pos
    :param ny: Texture coord pos
    :return:
    """
    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    # Calculate the normal
    normal = _normal3(p3, p2, p1)

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        # X, Y,  Z,   U,   V
        x1, y1, z1, (nx + ny) / 2, nx, normal.get_x(), normal.get_y(), normal.get_z(),
        x2, y2, z2, 0.0, 0.0, normal.get_x(), normal.get_y(), normal.get_z(),
        x3, y3, z3, ny, 0.0, normal.get_x(), normal.get_y(), normal.get_z()
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2
    ]

    return _Shape(vertices, indices, image_filename)


def createTriangleColor(p1, p2, p3, r, g, b):
    """
    Creates a triangle with color.

    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param r: Red color
    :param g: Green color
    :param b: Blue color
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    # Defining locations and color
    vertices = [
        # X, Y,  Z, R, G, B,
        x1, y1, z1, r, g, b,
        x2, y2, z2, r, g, b,
        x3, y3, z3, r, g, b,
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2
    ]

    return _Shape(vertices, indices)


def createTriangleColorNormal(p1, p2, p3, r, g, b):
    """
    Creates a triangle with color.

    :param p1: Vertex (x,y,z)
    :param p2: Vertex (x,y,z)
    :param p3: Vertex (x,y,z)
    :param r: Red color
    :param g: Green color
    :param b: Blue color
    :return:
    """
    # Extend
    p1 = __vertexUnpack3(p1)
    p2 = __vertexUnpack3(p2)
    p3 = __vertexUnpack3(p3)

    # Dissamble vertices
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    # Calculate the normal
    normal = _normal3(p3, p2, p1)

    # Defining locations and color
    vertices = [
        # X, Y,  Z, R, G, B,
        x1, y1, z1, r, g, b, normal.get_x(), normal.get_y(), normal.get_z(),
        x2, y2, z2, r, g, b, normal.get_x(), normal.get_y(), normal.get_z(),
        x3, y3, z3, r, g, b, normal.get_x(), normal.get_y(), normal.get_z()
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2
    ]

    return _Shape(vertices, indices)
