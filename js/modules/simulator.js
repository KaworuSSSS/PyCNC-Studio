import {
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
    pathGeometry
} from "./toolpath.js";

import {
    updateHUD
} from "./hud.js";


/*
============================================================
PyCNC Studio — SIMULATOR MODULE
============================================================
*/

/* =========================================================
   JOG HOME
   ========================================================= */

document
    .getElementById("jogHome")
    .addEventListener(
        "click",
        goHome
    );


/* =========================================================
   KEYBOARD
   ========================================================= */

window.addEventListener(
    "keydown",
    event => {

        if (
            event.target.tagName ===
            "INPUT"
        ) {

            return;

        }


        const key =
            event.key.toLowerCase();


        if (key === "a") {

            jogAxis(
                "x",
                -1
            );

        }

        if (key === "d") {

            jogAxis(
                "x",
                1
            );

        }

        if (key === "w") {

            jogAxis(
                "y",
                1
            );

        }

        if (key === "s") {

            jogAxis(
                "y",
                -1
            );

        }

        if (key === "r") {

            jogAxis(
                "z",
                1
            );

        }

        if (key === "f") {

            jogAxis(
                "z",
                -1
            );

        }

    }
);


/* =========================================================
   INITIAL POSITION
   ========================================================= */

goHome();


/* =========================================================
   RESIZE
   ========================================================= */

window.addEventListener(
    "resize",
    () => {

        camera.aspect =
            innerWidth /
            innerHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            innerWidth,
            innerHeight
        );

    }
);


/* =========================================================
   ANIMATION
   ========================================================= */

let previous =
    performance.now();
