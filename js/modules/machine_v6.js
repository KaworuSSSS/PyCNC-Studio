
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";


export function buildMachine({
    scene,
    cnc,
    zAxis,
    MACHINE,
    LIMITS,
    WORK_AREA,
    materials,
    box,
    addBox,
    cylinder
}) {

    const {
        black,
        steel,
        aluminum,
        aluminumDark,
        yellow
    } = materials;


    /*
    ============================================================
    MACHINE POSITION
    ============================================================
    */

    let machineX =
        WORK_AREA.X / 2;

    let machineY =
        WORK_AREA.Y / 2;

    let machineZ =
        WORK_AREA.Z;


    /*
    ============================================================
    Z BODY
    ============================================================
    */

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


    /*
    ============================================================
    Z GUIDE RODS
    ============================================================
    */

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


    /*
    ============================================================
    SPINDLE
    ============================================================
    */

    const spindle =
        new THREE.Group();

    zAxis.add(
        spindle
    );


    /*
    ============================================================
    SPINDLE BODY
    ============================================================
    */

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


    /*
    ============================================================
    SPINDLE TOP
    ============================================================
    */

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


    /*
    ============================================================
    MOTOR
    ============================================================
    */

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


    /*
    ============================================================
    MOTOR RINGS
    ============================================================
    */

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


    /*
    ============================================================
    TOOL ROTATION GROUP
    ============================================================
    */

    const toolRotation =
        new THREE.Group();

    spindle.add(
        toolRotation
    );


    /*
    ============================================================
    SHAFT
    ============================================================
    */

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


    /*
    ============================================================
    COLLET
    ============================================================
    */

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


    /*
    ============================================================
    CUTTER
    ============================================================
    */

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


    /*
    ============================================================
    TOOL TIP
    ============================================================
    */

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


    /*
    ============================================================
    TOOL WORLD POSITION
    ============================================================
    */

    const toolWorld =
        new THREE.Vector3();


    /*
    ============================================================
    TABLE TOP
    ============================================================
    */

    const TABLE_TOP =
        MACHINE.tableY +
        MACHINE.tableThickness / 2;


    /*
    ============================================================
    APPLY MACHINE POSITION
    ============================================================
    */

    function applyMachinePosition() {

        /*
         * X
         *
         * machineX representa la coordenada
         * X de la máquina.
         */
        if (typeof machineX !== "number") {
            machineX =
                WORK_AREA.X / 2;
        }

        carriage.position.x =
            machineX;


        /*
         * Y
         *
         * machineY representa la coordenada
         * Y de la máquina.
         */
        if (typeof machineY !== "number") {
            machineY =
                WORK_AREA.Y / 2;
        }

        gantry.position.z =
            machineY;


        /*
         * Z
         */

        const zTravel =
            WORK_AREA.Z -
            machineZ;

        zAxis.position.y =
            zTravel;


        /*
         * SAFETY
         */

        enforceToolLimit();

    }


    /*
    ============================================================
    TOOL SAFETY
    ============================================================
    */

    function enforceToolLimit() {

        toolTip.getWorldPosition(
            toolWorld
        );


        if (
            toolWorld.y <
            TABLE_TOP
        ) {

            const correction =
                TABLE_TOP -
                toolWorld.y;

            zAxis.position.y +=
                correction;

        }

    }


    /*
    ============================================================
    CLAMP ALL AXES
    ============================================================
    */

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


    /*
    ============================================================
    INITIAL POSITION
    ============================================================
    */

    clampMachine();


    /*
    ============================================================
    RETURN MACHINE API
    ============================================================
    */

    return {

        cnc,

        zAxis,

        spindle,

        toolRotation,

        toolTip,

        toolWorld,

        TABLE_TOP,

        get machineX() {
            return machineX;
        },

        get machineY() {
            return machineY;
        },

        get machineZ() {
            return machineZ;
        },

        setMachineX(value) {

            machineX =
                value;

            clampMachine();
            applyMachinePosition();

        },

        setMachineY(value) {

            machineY =
                value;

            clampMachine();
            applyMachinePosition();

        },

        setMachineZ(value) {

            machineZ =
                value;

            clampMachine();
            applyMachinePosition();

        },

        clampMachine,

        enforceToolLimit,

        applyMachinePosition

    };

}
