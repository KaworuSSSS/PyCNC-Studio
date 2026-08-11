import {
    WORK_AREA,
    LIMITS,
    machineX,
    machineY,
    machineZ,
    clampMachine
} from "./machine.js";

import {
    state,
    CNC_PROGRAM
} from "./program.js";

import {
    pathPoints,
    pathGeometry,
    toolPath
} from "./toolpath.js";

import {
    updateHUD
} from "./hud.js";

import {
    startProgram,
    pauseProgram,
    stopProgram,
    resetProgram,
    goHome
} from "./controls.js";


/*
============================================================
PyCNC Studio — MAIN / ANIMATION MODULE
============================================================
*/

/* =========================================================
   SCENE
   ========================================================= */

const scene =
    new THREE.Scene();

scene.background =
    new THREE.Color(
        0x0d1115
    );

scene.fog =
    new THREE.Fog(
        0x0d1115,
        900,
        3000
    );


/* =========================================================
   CAMERA
   ========================================================= */

const camera =
    new THREE.PerspectiveCamera(

        40,

        innerWidth /
        innerHeight,

        1,

        5000

    );

camera.position.set(
    1450,
    1200,
    1600
);


/* =========================================================
   RENDERER
   ========================================================= */

const renderer =
    new THREE.WebGLRenderer({

        antialias: true

    });

renderer.setPixelRatio(
    Math.min(
        devicePixelRatio,
        2
    )
);

renderer.setSize(
    innerWidth,
    innerHeight
);

renderer.shadowMap.enabled =
    true;

renderer.shadowMap.type =
    THREE.PCFSoftShadowMap;

renderer.outputColorSpace =
    THREE.SRGBColorSpace;

document
    .getElementById("viewport")
    .appendChild(
        renderer.domElement
    );


/* =========================================================
   CAMERA CONTROLS
   ========================================================= */

const controls =
    new OrbitControls(
        camera,
        renderer.domElement
    );

controls.target.set(
    WORK_AREA.X / 2,
    450,
    WORK_AREA.Y / 2
);

controls.enableDamping =
    true;

controls.dampingFactor =
    0.055;

controls.minDistance =
    500;

controls.maxDistance =
    3500;


/* =========================================================
   LIGHTS
   ========================================================= */

scene.add(
    new THREE.HemisphereLight(
        0xe8eef2,
        0x161b20,
        2.0
    )
);


const keyLight =
    new THREE.DirectionalLight(
        0xffffff,
        3.5
    );

keyLight.position.set(
    900,
    1800,
    1000
);

keyLight.castShadow =
    true;

keyLight.shadow.mapSize.set(
    2048,
    2048
);

scene.add(
    keyLight
);


const fillLight =
    new THREE.DirectionalLight(
        0x8ca9c7,
        1.1
    );

fillLight.position.set(
    -900,
    900,
    -900
);

scene.add(
    fillLight
);


/* =========================================================
   MATERIALS
   ========================================================= */

function mat(
    color,
    metalness,
    roughness
) {

    return new THREE.MeshStandardMaterial({

        color,
        metalness,
        roughness

    });

}


const aluminum =
    mat(
        0x626b70,
        0.85,
        0.28
    );

const aluminumDark =
    mat(
        0x272d31,
        0.90,
        0.22
    );

const aluminumLight =
    mat(
        0x929b9f,
        0.90,
        0.20
    );

const black =
    mat(
        0x101315,
        0.88,
        0.20
    );

const steel =
    mat(
        0xb8c0c4,
        0.94,
        0.15
    );

const rubber =
    mat(
        0x0b0d0f,
        0.15,
        0.78
    );

const yellow =
    mat(
        0xd5a72a,
        0.55,
        0.30
    );

const workMaterial =
    mat(
        0x8a5530,
        0.10,
        0.65
    );


/* =========================================================
   GEOMETRY
   ========================================================= */

function box(
    x,
    y,
    z,
    material
) {

    const mesh =
        new THREE.Mesh(

            new THREE.BoxGeometry(
                x,
                y,
                z
            ),

            material

        );

    mesh.castShadow =
        true;

    mesh.receiveShadow =
        true;

    return mesh;

}


function cylinder(
    radius,
    height,
    material,
    segments = 32
) {

    const mesh =
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                radius,
                radius,
                height,
                segments
            ),

            material

        );

    mesh.castShadow =
        true;

    mesh.receiveShadow =
        true;

    return mesh;

}


function addBox(
    parent,
    sx,
    sy,
    sz,
    material,
    px,
    py,
    pz
) {

    const mesh =
        box(
            sx,
            sy,
            sz,
            material
        );

    mesh.position.set(
        px,
        py,
        pz
    );

    parent.add(
        mesh
    );

    return mesh;

}



/* =========================================================
   MACHINE ROOT
   ========================================================= */

const cnc =
    new THREE.Group();

scene.add(
    cnc
);


/*
 * Usaremos:
 *
 * X = izquierda/derecha
 * Y = altura
 * Z = profundidad
 *
 * El origen de trabajo estará en:
 *
 * X = 0
 * Z = 0
 * Y = superficie de mesa
 */


const TABLE_Y =
    80;


/* =========================================================
   BASE
   ========================================================= */

addBox(

    cnc,

    WORK_AREA.X + 180,

    60,

    WORK_AREA.Y + 180,

    aluminumDark,

    WORK_AREA.X / 2,

    30,

    WORK_AREA.Y / 2

);


/* =========================================================
   TABLE
   ========================================================= */

addBox(

    cnc,

    WORK_AREA.X,

    MACHINE.tableThickness,

    WORK_AREA.Y,

    aluminumLight,

    WORK_AREA.X / 2,

    TABLE_Y,

    WORK_AREA.Y / 2

);


/* =========================================================
   WORK SURFACE
   ========================================================= */

const TABLE_TOP =
    TABLE_Y +
    MACHINE.tableThickness / 2;


addBox(

    cnc,

    WORK_AREA.X - 40,

    8,

    WORK_AREA.Y - 40,

    black,

    WORK_AREA.X / 2,

    TABLE_TOP + 4,

    WORK_AREA.Y / 2

);


/* =========================================================
   T SLOTS
   ========================================================= */

for (
    let x = 50;
    x < WORK_AREA.X;
    x += 50
) {

    addBox(

        cnc,

        4,

        2,

        WORK_AREA.Y - 60,

        aluminumLight,

        x,

        TABLE_TOP + 9,

        WORK_AREA.Y / 2

    );

}


/* =========================================================
   WORKPIECE
   ========================================================= */

const workpiece =
    addBox(

        cnc,

        420,

        35,

        260,

        workMaterial,

        WORK_AREA.X / 2,

        TABLE_TOP + 26,

        WORK_AREA.Y / 2

    );


/* =========================================================
   VISE
   ========================================================= */

addBox(
    cnc,
    500,
    20,
    330,
    aluminumDark,
    WORK_AREA.X / 2,
    TABLE_TOP + 14,
    WORK_AREA.Y / 2
);

addBox(
    cnc,
    25,
    90,
    330,
    steel,
    WORK_AREA.X / 2 - 230,
    TABLE_TOP + 65,
    WORK_AREA.Y / 2
);

addBox(
    cnc,
    25,
    90,
    330,
    steel,
    WORK_AREA.X / 2 + 230,
    TABLE_TOP + 65,
    WORK_AREA.Y / 2
);


/* =========================================================
   COLUMNS
   ========================================================= */

const columnHeight =
    MACHINE.frameHeight;

const columnY =
    TABLE_TOP +
    columnHeight / 2;


for (
    const x of [
        35,
        WORK_AREA.X - 35
    ]
) {

    for (
        const z of [
            35,
            WORK_AREA.Y - 35
        ]
    ) {

        addBox(

            cnc,

            MACHINE.columnSize,

            columnHeight,

            MACHINE.columnSize,

            aluminum,

            x,

            columnY,

            z

        );

        addBox(

            cnc,

            MACHINE.columnSize + 25,

            35,

            MACHINE.columnSize + 25,

            aluminumDark,

            x,

            TABLE_TOP + 20,

            z

        );

    }

}


/* =========================================================
   UPPER FRAME
   ========================================================= */

const FRAME_TOP =
    TABLE_TOP +
    columnHeight;


addBox(

    cnc,

    WORK_AREA.X + 70,

    80,

    100,

    aluminumDark,

    WORK_AREA.X / 2,

    FRAME_TOP,

    40

);

addBox(

    cnc,

    WORK_AREA.X + 70,

    80,

    100,

    aluminumDark,

    WORK_AREA.X / 2,

    FRAME_TOP,

    WORK_AREA.Y - 40

);


/* =========================================================
   GANTRY
   ========================================================= */

const gantry =
    new THREE.Group();

cnc.add(
    gantry
);


/*
 * gantry.position.x
 * = coordenada CNC X
 *
 * gantry.position.z
 * = coordenada CNC Y
 */


gantry.position.set(
    0,
    0,
    0
);


/* =========================================================
   GANTRY BEAM
   ========================================================= */

const gantryBeam =
    addBox(

        gantry,

        WORK_AREA.X + 30,

        90,

        100,

        aluminum,

        WORK_AREA.X / 2,

        FRAME_TOP - 120,

        0

    );


/* =========================================================
   GANTRY SIDE PLATES
   ========================================================= */

addBox(
    gantry,
    60,
    180,
    110,
    aluminumDark,
    45,
    FRAME_TOP - 190,
    0
);

addBox(
    gantry,
    60,
    180,
    110,
    aluminumDark,
    WORK_AREA.X - 45,
    FRAME_TOP - 190,
    0
);


/* =========================================================
   Y RAILS
   ========================================================= */

for (
    const x of [
        180,
        WORK_AREA.X - 180
    ]
) {

    const rail =
        cylinder(
            16,
            WORK_AREA.Y,
            steel
        );

    rail.rotation.x =
        Math.PI / 2;

    rail.position.set(
        x,
        FRAME_TOP - 100,
        WORK_AREA.Y / 2
    );

    cnc.add(
        rail
    );

}


/* =========================================================
   CARRIAGE
   ========================================================= */

const carriage =
    new THREE.Group();

gantry.add(
    carriage
);


/*
 * carriage.position.x
 * representa el movimiento X
 */

carriage.position.x =
    WORK_AREA.X / 2;


/* =========================================================
   CARRIAGE BODY
   ========================================================= */

addBox(

    carriage,

    180,

    180,

    130,

    aluminumDark,

    0,

    FRAME_TOP - 220,

    0

);

addBox(

    carriage,

    150,

    100,

    150,

    aluminum,

    0,

    FRAME_TOP - 340,

    0

);


/* =========================================================
   X RAILS
   ========================================================= */

for (
    const y of [
        FRAME_TOP - 270,
        FRAME_TOP - 340
    ]
) {

    const rail =
        cylinder(
            14,
            WORK_AREA.X,
            steel
        );

    rail.rotation.z =
        Math.PI / 2;

    rail.position.set(
    	WORK_AREA.X / 2,
   	 y,
    	-70
	);

    gantry.add(
        rail
    );

}


/* =========================================================
   Z AXIS
   ========================================================= */

const zAxis =
    new THREE.Group();

carriage.add(
    zAxis
);


/*
 * Coordenada Z:
 *
 * 0 = herramienta en mesa
 * 700 = herramienta arriba
 */



	/* =========================================================
   CNC SIMULATION
   ========================================================= */

function simulate(now) {

    /*
     * First frame
     */

    if (
        state.lastTime === undefined
    ) {

        state.lastTime = now;

        return;

    }


    /*
     * Calculate elapsed time
     */

    const delta =
        (now - state.lastTime) / 1000;

    state.lastTime = now;


    /*
     * Nothing to do when machine
     * is not running.
     */

    if (
        !state.running
    ) {

        return;

    }


    /*
     * Current CNC program
     */

    const toolpath =
        CNC_PROGRAM.toolpath;


    /*
     * Program finished
     */

    if (
        state.toolpathIndex >=
        toolpath.length
    ) {

        state.running = false;

        state.paused = false;

        state.stopped = false;

        state.completed = true;


        setStatus(
            "COMPLETED"
        );


        document
            .getElementById("start")
            .textContent =
            "↻ RESTART";


        updateHUD();

        return;

    }


    /*
     * Current target
     */

    const target =
        toolpath[
            state.toolpathIndex
        ];


    /*
     * Simulation speed.
     *
     * The slider changes the movement
     * speed without changing the
     * coordinates.
     */

    const movementSpeed =
        40 * state.speed;


    /*
     * Current position
     */

    const current = {

        X: machineX,

        Y: machineY,

        Z: machineZ

    };


    /*
     * Distance to target
     */

    const dx =
        target.X - current.X;

    const dy =
        target.Y - current.Y;

    const dz =
        target.Z - current.Z;


    const distance =
        Math.sqrt(
            dx * dx +
            dy * dy +
            dz * dz
        );


    /*
     * Target reached
     */

    if (
        distance < 0.05
    ) {

        machineX =
            target.X;

        machineY =
            target.Y;

        machineZ =
            target.Z;


        /*
         * Add point to visible toolpath
         */

        if (
            typeof pathPoints !==
            "undefined"
        ) {

            pathPoints.push(
                new THREE.Vector3(
                    machineX,
                    machineZ,
                    machineY
                )
            );

        }


        if (
            typeof pathGeometry !==
            "undefined"
        ) {

            pathGeometry.setFromPoints(
                pathPoints
            );

        }


        /*
         * Move to next command
         */

        state.toolpathIndex++;


        updateHUD();

        return;

    }


    /*
     * Movement for this frame
     */

    const step =
        movementSpeed * delta;


    const ratio =
        Math.min(
            step / distance,
            1
        );


    machineX +=
        dx * ratio;

    machineY +=
        dy * ratio;

    machineZ +=
        dz * ratio;


    /*
     * Respect machine limits
     */

    clampMachine();


    /*
     * Add current point to toolpath
     */

    if (
        typeof pathPoints !==
        "undefined"
    ) {

        pathPoints.push(
            new THREE.Vector3(
                machineX,
                machineZ,
                machineY
            )
        );

    }


    if (
        typeof pathGeometry !==
        "undefined"
    ) {

        pathGeometry.setFromPoints(
            pathPoints
        );

    }


    /*
     * Update HUD
     */

    updateHUD();

}


function animate(now) {

    requestAnimationFrame(
        animate
    );


    const delta =
        Math.min(

            (now - previous) /
            1000,

            0.05

        );


    previous =
        now;


    simulate(
        delta
    );


    controls.update();


    renderer.render(
        scene,
        camera
    );

}


animate(
    performance.now()
);
