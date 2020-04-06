/**
 MAIN
 Inicia la aplicación.
 @author Pablo Pizarro R. @ppizarror.com
 @date 2018-2019
 @license MIT
 */
"use strict";

/**
 * Función de la aplicación
 * @constructor
 */
function Aplicacion() {

    /**
     * Puntero al objeto
     */
    let self = this;

    /**
     * Indica que la aplicación ha sido inicializada
     */
    this._app_iniciada = false;

    /**
     * Propiedades de los objetos del mundo
     * @protected
     */
    this.objects_props = {

        /**
         * Plano de la escena
         */
        plane: {
            color: 0x222222,        // Color del plano
            dithering: false,       // Aplica dithering al material
            obj: null,              // Almacena el objeto
        },

        /**
         * Cámara
         */
        camera: {
            angle: 56,                          // Ángulo de la cámara (FOV)
            autorotate: false,                  // Rotar automáticamente en torno al objetivo
            far: 9.000,                         // Plano lejano de la cámara (% diagonal larga)
            light: {                            // Luz pegada a la cámara
                color: 0X181818,
                decay: 1.500,
                distance: 0.483,
                intensity: 0.600,
            },
            maxdistance: 2.500,                 // Distancia máxima (% diagonal larga)
            maxpolarangle: 1.000,               // Máximo ángulo que puede alcanzar la cámara (Por pi/2)
            near: 0.001,                        // Plano cercano de la cámara
            nopan: true,                        // Activa/desactiva el PAN del mouse
            posx: 0.500,                        // Posición inicial en x (% dimensión del mundo)
            posy: 0.500,                        // Posición inicial en y (% dimensión del mundo)
            posz: 0.500,                        // Posición inicial en z
            rotationx: -1.000,                  // Rotación inicial con respecto al eje x (Por pi/2)
            rotationy: -1.300,                  // Rotación inicial con respecto al eje y (Por pi/2)
            rotationz: -0.500,                  // Rotación inicial con respecto al eje z (Por pi/2)
            target: {                           // Target de la cámara, posición inicial con respecto a la dimensión
                x: 0.000,
                y: 0.000,
                z: 0.000,
            },
            zoom: 1.000,                        // Factor de zoom
        },

    };

    /**
     * Límites del mundo, modificar
     */
    this._worldsize = {
        x: 100,
        y: 100,
        z: 100,
    };

    /**
     * Reajusta el canvas al cambiar el tamaño.
     *
     * @function
     * @protected
     * @param {boolean} type - Indica tipo de carga, si es true se añade evento, si es false se borra
     * @since 0.1.0
     */
    this._threeResize = function (type) {

        /**
         * Nombre del evento
         * @type {string}
         */
        let $ev = 'resize.application' + generateID();

        /**
         * Activa el evento
         */
        if (type) {
            let $f = function (e) {

                /**
                 * Previene otros cambios, útil por ThreeControls
                 */
                if (notNullUndf(e)) e.preventDefault();

                /**
                 * Se obtiene el ancho y el alto del DIV
                 */
                let $w = Math.ceil(getElementWidth(self.maindiv));
                let $h = Math.ceil(getElementHeight(self.maindiv));

                /**
                 * Actualiza el aspecto del canvas
                 */
                self.objects_props.camera.aspect = $w / $h;

                /**
                 * Actualiza Three.js
                 */
                self._three_camera.aspect = $w / $h;
                self._three_camera.updateProjectionMatrix();
                self._renderer.setSize($w, $h); // Actualiza el render
                self._renderer.setPixelRatio(window.devicePixelRatio);

                /**
                 * Redibuja
                 */
                self._animateFrame();

            };
            // noinspection JSCheckFunctionSignatures
            $(window).on($ev, $f);
            $f();
        }

        /**
         * Desactiva el evento
         */
        else {
            // noinspection JSCheckFunctionSignatures
            $(window).off($ev);
        }

    };

    /**
     * Inicia Three.js.
     *
     * @function
     * @private
     */
    this._initThree = function () {

        /**
         * --------------------------------------------------------------------
         * Calcula límites del mapa
         * --------------------------------------------------------------------
         */
        this._worldsize.diagl = Math.sqrt(Math.pow(2 * this._worldsize.x, 2) + Math.pow(2 * this._worldsize.y, 2) + Math.pow(this._worldsize.z, 2));
        this._worldsize.diagx = Math.sqrt(Math.pow(2 * this._worldsize.x, 2) + Math.pow(this._worldsize.z, 2));
        this._worldsize.diagy = Math.sqrt(Math.pow(2 * this._worldsize.y, 2) + Math.pow(this._worldsize.z, 2));

        /**
         * --------------------------------------------------------------------
         * Setea cámara
         * --------------------------------------------------------------------
         */

        // Restricciones de la cámara
        this.objects_props.camera.far *= this._worldsize.diagl;
        this.objects_props.camera.maxdistance *= this._worldsize.diagl;
        this.objects_props.camera.maxpolarangle *= Math.PI / 2;

        // Posición inicial de la cámara
        this.objects_props.camera.posx *= this._worldsize.x;
        this.objects_props.camera.posy *= this._worldsize.y;
        this.objects_props.camera.posz *= this._worldsize.z;

        // Rotaciones iniciales
        this.objects_props.camera.rotationx *= Math.PI / 2;
        this.objects_props.camera.rotationy *= Math.PI / 2;
        this.objects_props.camera.rotationz *= Math.PI / 2;

        // Target de la cámara
        this.objects_props.camera.target.x *= this._worldsize.x;
        this.objects_props.camera.target.y *= this._worldsize.y;
        this.objects_props.camera.target.z *= this._worldsize.z;

        // Suma el target a la cámara para mantener distancias
        this.objects_props.camera.posx += this.objects_props.camera.target.x;
        this.objects_props.camera.posy += this.objects_props.camera.target.y;
        this.objects_props.camera.posz += this.objects_props.camera.target.z;

        // Posición inicial de la cámara
        self.objects_props.camera.initialTarget = {
            x: this.objects_props.camera.target.x,
            y: this.objects_props.camera.target.y,
            z: this.objects_props.camera.target.z
        };

        /**
         * --------------------------------------------------------------------
         * Setea propiedades de las luces
         * --------------------------------------------------------------------
         */
        this.objects_props.camera.light.distance *= this._worldsize.diagl;

        /**
         * --------------------------------------------------------------------
         * Inicia el render de Three.js
         * --------------------------------------------------------------------
         */
        this._renderer = new THREE.WebGLRenderer({

            // Activa las transparencias
            alpha: false,

            // Antialias
            antialias: true,

            // Tiene un búffer de profundidad de 16 bits
            depth: true,

            // Búffer de profundidad logarítmico, usado cuando hay mucha diferencia en la escena
            logarithmicDepthBuffer: false,

            // Preferencia de WebGL, puede ser "high-performance", "low-power" ó "default"
            powerPreference: "default",

            // Precisión
            precision: 'highp',

            // Los colores ya tienen incorporado las transparencias
            premultipliedAlpha: true,

            // Para capturas, si molesta deshabilitar
            preserveDrawingBuffer: false,

            // El búffer de dibujo tiene un stencil de 8 bits
            stencil: false,

        });

        /**
         * --------------------------------------------------------------------
         * Crea la escena
         * --------------------------------------------------------------------
         */
        this._scene = new THREE.Scene();
        this._scene.name = 'APLICACION-POKEBOLA-REBOTADORA';

        /**
         * --------------------------------------------------------------------
         * Modifica el render para las luces
         * --------------------------------------------------------------------
         */
        this._renderer.shadowMap.enabled = true;
        this._renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this._renderer.gammaInput = true;
        this._renderer.gammaOutput = true;

        /**
         * --------------------------------------------------------------------
         * Crea la cámara
         * --------------------------------------------------------------------
         * @private
         */
        this._three_camera = new THREE.PerspectiveCamera(
            self.objects_props.camera.angle,
            self.objects_props.camera.aspect,
            self.objects_props.camera.near,
            self.objects_props.camera.far,
        );
        this._three_camera.zoom = this.objects_props.camera.zoom;

        // noinspection JSUnusedGlobalSymbols
        this._cameralight = new THREE.PointLight();
        this._cameralight.color.setHex(this.objects_props.camera.light.color);
        this._cameralight.decay = this.objects_props.camera.light.decay;
        this._cameralight.distance = this.objects_props.camera.light.distance;
        this._cameralight.intensity = this.objects_props.camera.light.intensity;
        this._three_camera.add(this._cameralight);

        /**
         * --------------------------------------------------------------------
         * Añade el render al div
         * --------------------------------------------------------------------
         * @private
         */
        this.maindiv = $('#app');
        this.maindiv.append(this._renderer.domElement);

        /**
         * --------------------------------------------------------------------
         * Añade la cámara al escenario
         * --------------------------------------------------------------------
         */
        this._scene.add(this._three_camera);

        /**
         * --------------------------------------------------------------------
         * Crea los controles
         * --------------------------------------------------------------------
         */
        this._controls = new THREE.OrbitControls(this._three_camera, this._renderer.domElement);
        this._controls.addEventListener('change', this._render);

        // El pan sólo está disponible en móvil, en escritorio usar teclado
        this._controls.enablePan = true;

        // Desactiva las fechas
        this._controls.enableKey = false;

        // Autorotar (?) esta característica funciona sólo con requestAnimateFrame()
        this._controls.autoRotate = this.objects_props.camera.autorotate;

        // Define límites de la camara
        this._controls.maxPolarAngle = this.objects_props.camera.maxpolarangle;
        this._controls.maxDistance = this.objects_props.camera.maxdistance;

        /**
         * --------------------------------------------------------------------
         * Setea posición inicial de la cámara
         * --------------------------------------------------------------------
         */
        this._setInitialCameraPosition();

    };

    /**
     * Define la posición inicial de la cámara.
     *
     * @function
     * @private
     */
    this._setInitialCameraPosition = function () {

        /**
         * Setea posición inicial
         */
        this._three_camera.position.x = this.objects_props.camera.posy;
        this._three_camera.position.y = this.objects_props.camera.posz;
        this._three_camera.position.z = this.objects_props.camera.posx;

        /**
         * Setea ángulo inicial
         */
        this._three_camera.rotation.x = this.objects_props.camera.rotationy;
        this._three_camera.rotation.y = this.objects_props.camera.rotationz;
        this._three_camera.rotation.z = this.objects_props.camera.rotationx;

        /**
         * Target inicial
         */
        this.objects_props.camera.target.x = self.objects_props.camera.initialTarget.x;
        this.objects_props.camera.target.y = self.objects_props.camera.initialTarget.y;
        this.objects_props.camera.target.z = self.objects_props.camera.initialTarget.z;

        /**
         * Actualiza la cámara
         */
        this._setCameraTarget();

    };

    /**
     * Setea el target de la cámara.
     *
     * @function
     * @private
     */
    this._setCameraTarget = function () {
        // noinspection JSSuspiciousNameCombination
        self._controls.target.set(self.objects_props.camera.target.y, self.objects_props.camera.target.z, self.objects_props.camera.target.x);
        self._controls.update();
    };

    /**
     * Actualiza controles y renderiza.
     *
     * @function
     */
    this._animateFrame = function () {

        /**
         * Actualiza los controles
         */
        this._controls.update();

        /**
         * Renderiza un cuadro
         */
        this._render();

    };

    /**
     * Thread de animación, dibuja mediante {@link requestAnimationFrame}.
     *
     * @function
     * @private
     */
    this._animationThread = function () {
        if (!self._animateThread) return;
        requestAnimationFrame(self._initAnimate);
        self._animateFrame();
    };

    /**
     * Inicia el thread de actualizaciones.
     *
     * @function
     */
    this._initAnimate = function () {
        self._animateThread = true;
        self._animationThread();
    };

    /**
     * Renderiza el contenido de Three.js.
     *
     * @function
     * @private
     */
    this._render = function () {

        /**
         * Actualiza los modelos
         */
        if (self._app_iniciada) {
            self._pokebola.actualizar_posicion();
        }

        /**
         * Renderiza
         */
        self._renderer.render(self._scene, self._three_camera);

    };

    /**
     * Inicia la aplicación.
     * Basado en: https://threejs.org/examples/?q=light#webgl_lights_spotlight
     *
     * @function
     */
    this.init = function () {

        /**
         * Inicia three.js
         */
        this._initThree();
        this._threeResize(true);

        /**
         * Agrega luz ambiental
         */
        let ambient = new THREE.AmbientLight(0xffffff, 0.1);
        this._scene.add(ambient);

        /**
         * Agrega la luz puntual
         */
        let spotLight = new THREE.SpotLight(0xffffff, 1);
        spotLight.position.set(15, 40, 35);
        spotLight.angle = Math.PI / 4;
        spotLight.penumbra = 0.05;
        spotLight.decay = 2;
        spotLight.distance = 200;
        spotLight.castShadow = true;
        spotLight.shadow.mapSize.width = 1024;
        spotLight.shadow.mapSize.height = 1024;
        spotLight.shadow.camera.near = 10;
        spotLight.shadow.camera.far = 200;
        this._scene.add(spotLight);

        /**
         * Crea los modelos
         */
        let $helpersize = Math.min(self._worldsize.x, self._worldsize.y, self._worldsize.z) * 0.15;
        this._axis_helper = new THREE.AxesHelper($helpersize);
        this._scene.add(this._axis_helper);

        // Grilla
        let $mapsize = 2 * Math.max(this._worldsize.x, this._worldsize.y);
        let $griddist = 25;
        this._grid_helper = new THREE.GridHelper($mapsize, $griddist);
        this._grid_helper.position.y = 0;
        this._grid_helper.material.opacity = 0.1;
        this._grid_helper.material.transparent = true;
        this._scene.add(this._grid_helper);

        // Plano
        let material = new THREE.MeshPhongMaterial({color: 0x808080, dithering: true});
        let geometry = new THREE.PlaneBufferGeometry(2 * this._worldsize.x, 2 * this._worldsize.y);
        let mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(0, -0.5, 0);
        mesh.rotation.x = -Math.PI * 0.5;
        mesh.receiveShadow = true;
        this._scene.add(mesh);

        // noinspection JSUnusedLocalSymbols
        let lightHelper = new THREE.SpotLightHelper(spotLight);
        // this._scene.add(lightHelper);

        /**
         * Crea la pokebola
         */
        this._pokebola = new Pokebola(new Point2D(-5, -5, 30), new Point2D(-45, -35, 10), 10, 0xff0000, 0.6, -0.5, 100);
        this._pokebola.crear_modelo(this._scene);

        /**
         * Inicia el renderizado continuo
         */
        self._app_iniciada = true;
        this._initAnimate();

    };

}

$(function () {

    /**
     * Crea la aplicación
     */
    let app = new Aplicacion();

    /**
     * Inicia la aplicación
     */
    app.init();

});