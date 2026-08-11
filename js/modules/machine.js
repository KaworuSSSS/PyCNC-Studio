
const WORK_AREA = {
    X: 110,
    Y: 70,
    Z: 70
};


/*
============================================================
PyCNC Studio — MACHINE MODULE
============================================================
*/

/* =========================================================
   MACHINE LIMITS
   ========================================================= */

const LIMITS = {

    X_MIN: 0,

    X_MAX: WORK_AREA.X,

    Y_MIN: 0,

    Y_MAX: WORK_AREA.Y,

    Z_MIN: -100,

    Z_MAX: WORK_AREA.Z

};


/* =========================================================
   MACHINE DIMENSIONS
   ========================================================= */

const MACHINE = {

    tableX: WORK_AREA.X,

    tableY: WORK_AREA.Y,

    tableThickness: 40,

    frameHeight: 850,

    columnSize: 70,

    gantryThickness: 70,

    gantryDepth: 100,

    spindleWidth: 90,

    spindleDepth: 90,

    toolLength: 120

};



let machineZ =
    WORK_AREA.Z;


/* =========================================================
   Z BODY
   ========================================================= */

addBox(

    zAxis,

    MACHINE.spindleWidth,

    360,

    MACHINE.spindleDepth,

    black,

    0,

    0,

    0

);


/* =========================================================
   Z GUIDE RODS
   ========================================================= */

for (
    const x of [-30, 30]
) {

    const rod =
        cylinder(
            12,
            360,
            steel
        );

    rod.position.set(
        x,
        0,
        -65
    );

    zAxis.add(
        rod
    );

}


/* =========================================================
   SPINDLE
   ========================================================= */

const spindle =
    new THREE.Group();

zAxis.add(
    spindle
);


/* =========================================================
   SPINDLE BODY
   ========================================================= */

const spindleBody =
    cylinder(
        42,
        180,
        black
    );

spindleBody.position.y =
    -40;

spindle.add(
    spindleBody
);


/* =========================================================
   SPINDLE TOP
   ========================================================= */

const spindleTop =
    cylinder(
        48,
        45,
        aluminum
    );

spindleTop.position.y =
    70;

spindle.add(
    spindleTop
);


/* =========================================================
   MOTOR
   ========================================================= */

const motor =
    cylinder(
        55,
        90,
        aluminumDark
    );

motor.position.y =
    135;

spindle.add(
    motor
);


/* =========================================================
   MOTOR RINGS
   ========================================================= */

for (
    let y = 95;
    y <= 165;
    y += 15
) {

    const ring =
        cylinder(
            58,
            5,
            aluminum
        );

    ring.position.y =
        y;

    spindle.add(
        ring
    );

}


/* =========================================================
   TOOL ROTATION GROUP
   ========================================================= */

const toolRotation =
    new THREE.Group();

spindle.add(
    toolRotation
);


/* =========================================================
   SHAFT
   ========================================================= */

const shaft =
    cylinder(
        16,
        80,
        steel
    );

shaft.position.y =
    -155;

toolRotation.add(
    shaft
);


/* =========================================================
   COLLET
   ========================================================= */

const collet =
    cylinder(
        20,
        35,
        steel
    );

collet.position.y =
    -210;

toolRotation.add(
    collet
);


/* =========================================================
   CUTTER
   ========================================================= */

const cutter =
    cylinder(
        8,
        MACHINE.toolLength,
        steel
    );

cutter.position.y =
    -285;

toolRotation.add(
    cutter
);


/* =========================================================
   TOOL TIP
   ========================================================= */

const toolTip =
    cylinder(
        9,
        20,
        yellow
    );

toolTip.position.y =
    -355;

toolRotation.add(
    toolTip
);


/* =========================================================
   TOOL WORLD POSITION
   ========================================================= */

const toolWorld =
    new THREE.Vector3();


/* =========================================================
   POSITIONING
   =========================================================

   La herramienta se coloca de manera que:

   machineZ = 0

   significa que la punta coincide
   exactamente con TABLE_TOP.
   ========================================================= */

function setMachineZ(z) {

    machineZ =
        THREE.MathUtils.clamp(
            z,
            LIMITS.Z_MIN,
            LIMITS.Z_MAX
        );

}


/* =========================================================
   APPLY MACHINE POSITION
   ========================================================= */

function applyMachinePosition() {

    /*
     * X
     */

    carriage.position.x =
        machineX;


    /*
     * Y
     */

    gantry.position.z =
        machineY;


    /*
     * Z
     */

    /*
     * El eje Z se mueve en
     * coordenadas 3D inversas.
     */

    const zTravel =
        WORK_AREA.Z -
        machineZ;

    zAxis.position.y =
        zTravel;


    /*
     * Protección adicional.
     */

    enforceToolLimit();

}


/* =========================================================
   MACHINE COORDINATES
   ========================================================= */

let machineX =
    WORK_AREA.X / 2;

let machineY =
    WORK_AREA.Y / 2;


/* =========================================================
   TOOL SAFETY
   ========================================================= */

function enforceToolLimit() {

    toolTip.getWorldPosition(
        toolWorld
    );


    /*
     * La punta jamás puede estar
     * por debajo de la superficie.
     */

    if (
        toolWorld.y <
        TABLE_TOP
    ) {

        const correction =
            TABLE_TOP -
            toolWorld.y;

        zAxis.position.y +=
            correction;

        /*
         * Volver a calcular Z lógico.
         */

        machineZ =
            THREE.MathUtils.clamp(

                WORK_AREA.Z -
                zAxis.position.y,

                LIMITS.Z_MIN,
                LIMITS.Z_MAX

            );

    }

}


/* =========================================================
   CLAMP ALL AXES
   ========================================================= */

function clampMachine() {

    machineX =
        THREE.MathUtils.clamp(
            machineX,
            LIMITS.X_MIN,
            LIMITS.X_MAX
        );


    machineY =
        THREE.MathUtils.clamp(
            machineY,
            LIMITS.Y_MIN,
            LIMITS.Y_MAX
        );


    machineZ =
        THREE.MathUtils.clamp(
            machineZ,
            LIMITS.Z_MIN,
            LIMITS.Z_MAX
        );


    applyMachinePosition();

}




export {
    WORK_AREA,
    LIMITS,
    machineX,
    machineY,
    machineZ,
    toolTip,
    toolWorld,
    clampMachine,
    enforceToolLimit,
    applyMachinePosition
};
