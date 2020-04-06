/**
 Punto en 2D
 @author Pablo Pizarro R. @ppizarror.com
 @date 2018-2019
 @license MIT
 */
"use strict";

/**
 * Clase punto
 *
 * @param {number} posx - Posición en x
 * @param {number} posy - Posición en y
 * @param {number} posz - Posición en z
 * @constructor
 */
function Point2D(posx, posy, posz) {

    /**
     * Guarda las variables
     */
    this._posx = posx;
    this._posy = posy;
    this._posz = posz;

    /**
     * Define la posición en x
     * @param {number} x - Nueva posición
     */
    this.set_x = function (x) {
        // noinspection JSUnusedGlobalSymbols
        this._posx = x;
    };

    /**
     * Define la posición en x
     * @param {number} y - Nueva posición
     */
    this.set_y = function (y) {
        this._posy = y;
    };

    /**
     * Define la posición en x
     * @param {number} z - Nueva posición
     */
    this.set_z = function (z) {
        this._posz = z;
    };

    /**
     * Returna posición en x
     * @returns {number}
     */
    this.get_x = function () {
        return this._posx;
    };

    /**
     * Returna posición en y
     * @returns {number}
     */
    this.get_y = function () {
        return this._posy;
    };

    /**
     * Returna posición en z
     * @returns {number}
     */
    this.get_z = function () {
        return this._posz;
    };

    // noinspection JSUnusedGlobalSymbols
    /**
     * Imprime la posición en consola
     */
    this.disp = function () {
        console.log('(' + this._posx + ', ' + this._posy + ', ' + this._posz + ')');
    };

}