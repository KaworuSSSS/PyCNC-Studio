import {
    toolTip,
    toolWorld
} from "./machine.js";


/*
============================================================
PyCNC Studio — TOOLPATH MODULE
============================================================
*/

/* =========================================================
   PATH
   ========================================================= */

const pathPoints =
    [];

const pathGeometry =
    new THREE.BufferGeometry();

const pathMaterial =
    new THREE.LineBasicMaterial({

        color: 0xff4545,

        transparent: true,

        opacity: 0.8

    });

const toolPath =
    new THREE.Line(
        pathGeometry,
        pathMaterial
    );

scene.add(
    toolPath
);


function recordPath() {

    toolTip.getWorldPosition(
        toolWorld
    );

    pathPoints.push(
        toolWorld.clone()
    );


    if (
        pathPoints.length >
        1200
    ) {

        pathPoints.shift();

    }


    pathGeometry.setFromPoints(
        pathPoints
    );

}




export {
    pathPoints,
    pathGeometry,
    toolPath,
    recordPath
};
