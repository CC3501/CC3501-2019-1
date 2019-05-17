"""
Código principal del problema. Instancia un plano y una pokebola.
Esta rebotará siguiendo alguna dirección y una velocidad inicial.

@author Pablo Pizarro R. @ppizarror
@date 2018-2019
@license MIT
"""

# Importación de librerías
from PyOpenGLtoolbox import *  # Hecho con versión 2.3.0
from pokebola import Pokebola

"""
-------------------------------------------------------------------------------
Definición de algunas constantes
-------------------------------------------------------------------------------
"""
FOV = 60
FPS = 60
VENTANA_H = 600
VENTANA_W = 800

"""
-------------------------------------------------------------------------------
Inicio de OpenGL
-------------------------------------------------------------------------------
"""
init_pygame(VENTANA_W, VENTANA_H, 'Simulador Pokebolas', centered_window=True)
init_gl(transparency=False, normalized=True, perspectivecorr=True, antialiasing=True,
        depth=True, smooth=True, version=True, lighting=True, numlights=1)
init_light(GL_LIGHT0)
reshape_window_perspective(w=VENTANA_W, h=VENTANA_H, near=0.01, far=1000, fov=60)
clock = pygame.time.Clock()

"""
-------------------------------------------------------------------------------
Creación de modelos
-------------------------------------------------------------------------------
"""
axis = create_axes(5)  # Retorna una lista con los ejes, parte de la librería

# Crea el plano
cubo = create_cube()
plano = glGenLists(1)
glNewList(plano, GL_COMPILE)
glPushMatrix()
glTranslate(0, 0, -1)
glScale(50, 50, 1)
glColor4fv([0.4, 0.4, 0.4, 1])
glCallList(cubo)
glPopMatrix()
glEndList()

pokebola = Pokebola(Point3(0, -5, 5),  # Posición inicial
                    Vector3(-0.5, 15, 0),  # Velocidad inicial
                    1,  # Radio
                    [1, 0, 0, 1],  # Color
                    alpha_elastico=0.7,  # Coeficiente choque elástico
                    plano=0  # Posición superior del plano en z (considerar mitad de la altura)
                    )

"""
-------------------------------------------------------------------------------
Creación de la cámara
-------------------------------------------------------------------------------
"""
camera = CameraXYZ(Point3(10, 10, 10), Point3(0, 0, 0), Point3(0, 0, 1))
camera.set_radial_vel(100)

"""
-------------------------------------------------------------------------------
Inicio de OpenGL
-------------------------------------------------------------------------------
"""
print('Camara XYZ cartesiana')
print('Rota eje X con teclas W/S')
print('Rota eje Y con teclas A/D')
print('Rota eje Z con teclas Q/E')
print('Zoom in/out con teclas N/M')

while True:

    # Tick del reloj
    clock.tick(FPS)

    # Elimina el buffer
    clear_buffer()

    # Ubica la cámara
    camera.place()

    # Actualiza objetos
    pokebola.actualizar_posicion()

    # Dibuja objetos
    glCallList(plano)
    glDisable(GL_LIGHTING)
    glCallList(axis)
    glEnable(GL_LIGHTING)
    pokebola.dibujar()

    # Chequea eventos
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # Cierra la app
            exit()
    keys = pygame.key.get_pressed()
    if keys[K_w]:  # Rota cámara eje x
        camera.rotate_x(2.5)
    elif keys[K_s]:
        camera.rotate_x(-2.5)
    if keys[K_a]:  # Rota cámara eje y
        camera.rotate_y(-2.5)
    elif keys[K_d]:
        camera.rotate_y(2.5)
    if keys[K_q]:  # Rota cámara eje z
        camera.rotate_z(-2.5)
    elif keys[K_e]:
        camera.rotate_z(2.5)
    if keys[K_n]:  # Acerca / Aleja la cámara
        camera.close()
    elif keys[K_m]:
        camera.far()

    # Vuelca el contenido
    pygame.display.flip()
