/**
 UTILS
 Funciones utilitarias.
 @author Pablo Pizarro R. @ppizarror.com
 @date 2018-2019
 @license MIT
 */
"use strict";

/**
 * Retorna la altura en px del elemento en el DOM.
 *
 * @function
 * @param {Object} elem - Elemento jQuery
 * @returns {number} - Altura
 */
function getElementHeight(elem) {
    try {
        // noinspection JSValidateTypes
        return elem.outerHeight();
    } catch (e) {
        return -1;
    } finally {
    }
}

/**
 * Retorna el ancho en px del elemento en el DOM.
 *
 * @function
 * @param {Object} elem - Elemento jQuery
 * @returns {number} - Ancho
 */
function getElementWidth(elem) {
    try {
        // noinspection JSValidateTypes
        return elem.outerWidth();
    } catch (e) {
        return -1;
    } finally {
    }
}

/**
 * Retorna verdadero si el objeto no es nulo e indefinido.
 *
 * @function
 * @param {object} obj - Objeto a comprobar
 * @returns {boolean} - Booleano de comprobación
 */
function notNullUndf(obj) {
    return obj !== null && obj !== undefined;
}

/**
 * Genera un string aleatorio.
 *
 * @function
 * @returns {string} - String aleatorio
 */
function generateID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = Math.random() * 16 | 0;
        let v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}