/**
 Pokebola
 Clase pokebola.
 @author Pablo Pizarro R. @ppizarror.com
 @date 2018-2019
 @license MIT
 */
"use strict";

/**
 * Crea una Pokebola.
 *
 * @param {Point2D} pos_inicial - Posición inicial
 * @param {Point2D} velocidad_inicial - Velocidad inicial
 * @param {number} diametro_pokebola - Diámetro pokebola
 * @param {number} color_pokebola - Color pokebola
 * @param {number} alpha_elastico - Coeficiente de rebote
 * @param {number} plano - Posición del plano
 * @param {number} plano_largo - Largo del plano
 * @constructor
 */
function Pokebola(pos_inicial, velocidad_inicial, diametro_pokebola, color_pokebola,
                  alpha_elastico, plano, plano_largo) {

    // noinspection ES6ConvertVarToLetConst
    /**
     * Puntero al objeto
     */
    var self = this;

    /**
     * Guarda las variables
     */
    this._alpha = alpha_elastico;
    this._color = color_pokebola;
    this._dt = 1 / 60; // Incremento de tiempo
    this._g = 98.1665; // "Gravedad"
    this._pos_plano = plano;
    this._pos = pos_inicial;
    this._plano_largo = plano_largo;
    this._radio = diametro_pokebola / 2;
    this._vel = velocidad_inicial;

    /**
     * Crea el modelo en three.js
     */
    this.crear_modelo = function (scene) {

        /**
         * Crea una esfera
         * Basado en: https://threejs.org/docs/#api/en/geometries/SphereGeometry
         */
        let geometry = new THREE.SphereGeometry(this._radio, 32, 32);
        let material = new THREE.MeshPhongMaterial({color: this._color, dithering: true});
        this._sphere = new THREE.Mesh(geometry, material);
        this._sphere.castShadow = true;
        scene.add(this._sphere);
    };

    /**
     * Actualizar posición
     */
    this.actualizar_posicion = function () {

        // Actualiza velocidad en z (gravedad)
        self._vel.set_z(self._vel.get_z() - self._g * self._dt);  // v(t) = v(t-1) + a*dt

        // Actualiza la posición
        self._pos.set_x(self._pos.get_x() + self._vel.get_x() * self._dt);
        self._pos.set_y(self._pos.get_y() + self._vel.get_y() * self._dt);
        self._pos.set_z(self._pos.get_z() + self._vel.get_z() * self._dt);

        // Busca colisiones
        self._detectar_colision();

        // Ubica el modelo
        self._mover_modelo();

    };

    /**
     * Detecta las colisiones.
     */
    this._detectar_colision = function () {
        if (self._pos.get_z() - self._radio < self._pos_plano) { // Colisión inferior
            self._vel.set_z(-self._vel.get_z() * self._alpha);
            self._pos.set_z(self._pos_plano + self._radio);
        }
        if (self._pos.get_x() + self._radio > self._plano_largo) { // Choque en x +
            self._vel.set_x(-self._vel.get_x() * self._alpha);
            self._pos.set_x(self._plano_largo - self._radio);
        }
        if (self._pos.get_x() - self._radio < -self._plano_largo) { // Choque en x -
            self._vel.set_x(-self._vel.get_x() * self._alpha);
            self._pos.set_x(-self._plano_largo + self._radio);
        }
        if (self._pos.get_y() + self._radio > self._plano_largo) { // Choque en y +
            self._vel.set_y(-self._vel.get_y() * self._alpha);
            self._pos.set_y(self._plano_largo - self._radio);
        }
        if (self._pos.get_y() - self._radio < -self._plano_largo) { // Choque en y -
            self._vel.set_y(-self._vel.get_y() * self._alpha);
            self._pos.set_y(-self._plano_largo + self._radio);
        }
    };

    /**
     * Mueve el modelo.
     */
    this._mover_modelo = function () {
        this._sphere.position.x = this._pos.get_x();
        this._sphere.position.y = this._pos.get_z();
        this._sphere.position.z = this._pos.get_y();
    };

}