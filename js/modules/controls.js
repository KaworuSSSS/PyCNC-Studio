import {
    WORK_AREA,
    machineX,
    machineY,
    machineZ,
    clampMachine
} from "./machine.js";

import {
    state
} from "./program.js";

import {
    pathPoints,
    pathGeometry
} from "./toolpath.js";

import {
    updateHUD
} from "./hud.js";


/*
============================================================
PyCNC Studio — CONTROLS MODULE
============================================================
*/

/* =========================================================
   SIMULATION CONTROL
   ========================================================= */

function startProgram() {

    /*
     * Resume paused program
     */

    if (
        state.paused &&
        !state.stopped
    ) {

        state.paused = false;

        state.running = true;

        setStatus("RUNNING");

        document
            .getElementById("start")
            .textContent = "▶ START";

        return;
    }


    /*
     * Restart completed program
     */

    if (
        state.completed
    ) {

        resetProgram();

    }


    /*
     * Restart after STOP
     */

    if (
        state.stopped
    ) {

        resetProgram();

    }


    state.running = true;

    state.paused = false;

    state.stopped = false;

    state.completed = false;


    setStatus("RUNNING");


    document
        .getElementById("start")
        .textContent = "▶ START";

}


function pauseProgram() {

    if (
        !state.running
    ) {

        return;

    }


    state.running = false;

    state.paused = true;

    state.stopped = false;


    setStatus("PAUSED");


    document
        .getElementById("start")
        .textContent = "▶ RESUME";

}


function stopProgram() {

    state.running = false;

    state.paused = false;

    state.stopped = true;

    state.completed = false;


    setStatus("STOPPED");


    document
        .getElementById("start")
        .textContent = "▶ START";

}


function resetProgram() {

    state.running = false;

    state.paused = false;

    state.stopped = false;

    state.completed = false;

    state.toolpathIndex = 0;

    state.time = 0;


    /*
     * Clear toolpath visualization
     */

    if (
        typeof pathPoints !== "undefined"
    ) {

        pathPoints.length = 0;

    }


    if (
        typeof pathGeometry !== "undefined"
    ) {

        pathGeometry.setFromPoints([]);

    }


    /*
     * Reset machine position
     */

    machineX = 0;

    machineY = 0;

    machineZ = WORK_AREA.Z;


    clampMachine();


    updateHUD();

}


/* =========================================================
   HOME
   ========================================================= */

function goHome() {

    state.running = false;

    state.paused = false;

    state.stopped = false;

    state.completed = false;

    state.toolpathIndex = 0;

    state.time = 0;


    machineX = 0;

    machineY = 0;

    machineZ = WORK_AREA.Z;


    clampMachine();


    updateHUD();


    setStatus("READY");


    document
        .getElementById("start")
        .textContent = "▶ START";

}


/* =========================================================
   START
   ========================================================= */

document
    .getElementById("start")
    .onclick =
    startProgram;


/* =========================================================
   PAUSE
   ========================================================= */

document
    .getElementById("pause")
    .onclick =
    pauseProgram;


/* =========================================================
   STOP
   ========================================================= */

document
    .getElementById("stop")
    .onclick =
    stopProgram;


/* =========================================================
   HOME
   ========================================================= */

document
    .getElementById("home")
    .onclick =
    goHome;


/* =========================================================
   SPEED CONTROL
   ========================================================= */

const speedControl =
    document.getElementById("speed");


if (
    speedControl
) {

    speedControl.addEventListener(
        "input",
        () => {

            state.speed =
                parseFloat(
                    speedControl.value
                );

        }
    );

}


/* =========================================================
   SPEED
   ========================================================= */

document
    .getElementById("speed")
    .oninput =
    event => {

        state.speed =
            parseFloat(
                event.target.value
            );

    };


/* =========================================================
   JOG STEP
   ========================================================= */

let jogStep =
    0.1;


document
    .querySelectorAll(".step")
    .forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    jogStep =
                        parseFloat(
                            button.dataset.step
                        );


                    document
                        .querySelectorAll(".step")
                        .forEach(
                            b => {

                                b.classList.remove(
                                    "active"
                                );

                            }
                        );


                    button.classList.add(
                        "active"
                    );

                }
            );

        }
    );


/* =========================================================
   MANUAL JOG
   ========================================================= */

function jogAxis(
    axis,
    direction
) {

    state.running =
        false;

    state.paused =
        false;

    state.stopped =
        false;


    const distance =
        jogStep *
        direction;


    /*
     * X
     */

    if (
        axis === "x"
    ) {

        machineX +=
            distance;

    }


    /*
     * Y
     */

    if (
        axis === "y"
    ) {

        machineY +=
            distance;

    }


    /*
     * Z
     */

    if (
        axis === "z"
    ) {

        machineZ +=
            distance;

    }


    /*
     * Aplicar límites físicos.
     */

    clampMachine();


    updateHUD();

    setStatus(
        "JOG"
    );

}


/* =========================================================
   JOG BUTTONS
   ========================================================= */

document
    .querySelectorAll(".jog-btn")
    .forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    jogAxis(

                        button.dataset.axis,

                        parseInt(
                            button.dataset.dir
                        )

                    );

                }
            );

        }
    );




export {
    startProgram,
    pauseProgram,
    stopProgram,
    resetProgram,
    goHome
};
