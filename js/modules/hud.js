import {
    machineX,
    machineY,
    machineZ
} from "./machine.js";


/*
============================================================
PyCNC Studio — HUD MODULE
============================================================
*/

/* =========================================================
   HUD
   ========================================================= */

function updateHUD() {

    document
        .getElementById("x")
        .textContent =
        machineX.toFixed(2);

    document
        .getElementById("y")
        .textContent =
        machineY.toFixed(2);

    document
        .getElementById("z")
        .textContent =
        machineZ.toFixed(2);

}


function setStatus(text) {

    document
        .getElementById("statusText")
        .textContent =
        text;

}




export {
    updateHUD
};
