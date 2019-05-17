"""
Clase pokebola. La idea de esta clase es definir todos los
métodos propios de este objeto:
    - Detectar colisión con el plano
    - Modificar su velocidad
    - Dibujarse

@author Pablo Pizarro R. @ppizarror
@date 2018-2019
@license MIT
"""

# Importación de librerías
from PyOpenGLtoolbox import *


class Pokebola:
    def __init__(self, pos_inicial, velocidad_inicial, diametro_pokebola, color_pokebola,
                 alpha_elastico, plano):
        """
        Constructor

        @param pos_inicial: Posición inicial de la Pokebola
        @param velocidad_inicial: Velocidad inicial de la Pokebola
        @param diametro_pokebola: Radio de la Pokebola
        @param color_pokebola: Color de la Pokebola
        @param alpha_elastico: Constante elática de rebote
        @param plano: Posición en z del plano
        @type pos_inicial: Point3
        @type velocidad_inicial: Vector3
        @type diametro_pokebola: float
        @type color_pokebola: list
        @type alpha_elastico: float
        @type plano: float
        """
        self._alpha = alpha_elastico
        self._color = color_pokebola
        self._dt = 1 / 60  # Incremento de tiempo, idealmente se debería calcular y no asumir constante
        self._g = 9.8  # "Gravedad" del mundo
        self._modelo = load_gmsh_model("esfera.msh", diametro_pokebola, 0, 0, 0, True, False)
        self._pos = pos_inicial
        self._pos_plano = plano
        self._radio = diametro_pokebola / 2
        self._vel = velocidad_inicial

    def actualizar_posicion(self):
        """
        La idea de esta función es actualizar la posición de la pokebola, para ello
        se usa un contador interno del tiempo (que se incrementa cada vez que se llama
        a esta función). Luego se aplican las funciones matemáticas para modificar la velocidad
        (intro a la física).

        Si se choca con el plano entonces se rebota. El plano se define entre (-50,-50) y (50,50),
        si las coordenadas (x,y) están dentro de ese cuadrante y la posición inferior de la pokebola
        (o sea, centro-radio) es igual o inferior al plano rebota
        :return:
        """

        # Actualiza velocidad en z (gravedad)
        self._vel.set_z(self._vel.get_z() - self._g * self._dt)  # v(t) = v(t-1) + a*dt

        # Actualiza la posición
        self._pos.set_x(self._pos.get_x() + self._vel.get_x() * self._dt)
        self._pos.set_y(self._pos.get_y() + self._vel.get_y() * self._dt)
        self._pos.set_z(self._pos.get_z() + self._vel.get_z() * self._dt)

        # Busca colisiones
        self._detectar_colision()

    def _detectar_colision(self):
        """
        Maneja las colisiones
        :return:
        """

        # Colisión con el plano
        if self._pos.get_z() - self._radio <= self._pos_plano:
            self._vel.set_z(-self._vel.get_z() * self._alpha)
            self._pos.set_z(self._pos_plano + self._radio)

    def dibujar(self):
        """
        Dibuja el modelo
        :return:
        """
        self._modelo.draw(self._pos.export_to_list(), self._color)
