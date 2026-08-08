import * as THREE from "three";

import { OrbitControls } from
    "three/addons/controls/OrbitControls.js";


// =====================================================
// SCENE
// =====================================================

const scene = new THREE.Scene();

scene.background =
    new THREE.Color(0x101318);


// =====================================================
// CAMERA
// =====================================================

const camera =
    new THREE.PerspectiveCamera(
        45,
        window.innerWidth /
        window.innerHeight,
        0.1,
        1000
    );

camera.position.set(
    170,
    150,
    170
);


// =====================================================
// RENDERER
// =====================================================

const renderer =
    new THREE.WebGLRenderer({
        antialias: true
    });

renderer.setPixelRatio(
    Math.min(
        window.devicePixelRatio,
        2
    )
);

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);

renderer.shadowMap.enabled = true;

renderer.shadowMap.type =
    THREE.PCFSoftShadowMap;

document
    .getElementById("viewport")
    .appendChild(renderer.domElement);


// =====================================================
// CONTROLS
// =====================================================

const controls =
    new OrbitControls(
        camera,
        renderer.domElement
    );

controls.target.set(
    50,
    25,
    35
);

controls.enableDamping = true;

controls.dampingFactor = 0.06;


// =====================================================
// LIGHTING
// =====================================================

const ambient =
    new THREE.HemisphereLight(
        0xffffff,
        0x222222,
        2.2
    );

scene.add(ambient);


const keyLight =
    new THREE.DirectionalLight(
        0xffffff,
        3
    );

keyLight.position.set(
    100,
    180,
    120
);

keyLight.castShadow = true;

scene.add(keyLight);


const fillLight =
    new THREE.DirectionalLight(
        0xffffff,
        1
    );

fillLight.position.set(
    -100,
    80,
    -100
);

scene.add(fillLight);


// =====================================================
// MATERIALS
// =====================================================

const aluminum =
    new THREE.MeshStandardMaterial({
        color: 0x70777d,
        metalness: 0.8,
        roughness: 0.28
    });


const darkMetal =
    new THREE.MeshStandardMaterial({
        color: 0x20252a,
        metalness: 0.85,
        roughness: 0.25
    });


const black =
    new THREE.MeshStandardMaterial({
        color: 0x111316,
        metalness: 0.7,
        roughness: 0.3
    });


const workMaterial =
    new THREE.MeshStandardMaterial({
        color: 0xb67c42,
        metalness: 0.05,
        roughness: 0.75
    });


// =====================================================
// CNC MACHINE
// =====================================================

const machine =
    new THREE.Group();

scene.add(machine);


// =====================================================
// HELPER: BOX
// =====================================================

function box(
    width,
    height,
    depth,
    material
) {

    const geometry =
        new THREE.BoxGeometry(
            width,
            height,
            depth
        );

    const mesh =
        new THREE.Mesh(
            geometry,
            material
        );

    mesh.castShadow = true;

    mesh.receiveShadow = true;

    return mesh;
}


// =====================================================
// HELPER: CYLINDER
// =====================================================

function cylinder(
    radius,
    height,
    material
) {

    const geometry =
        new THREE.CylinderGeometry(
            radius,
            radius,
            height,
            32
        );

    const mesh =
        new THREE.Mesh(
            geometry,
            material
        );

    mesh.castShadow = true;

    mesh.receiveShadow = true;

    return mesh;
}


// =====================================================
// BASE
// =====================================================

const base =
    box(
        120,
        8,
        80,
        darkMetal
    );

base.position.set(
    0,
    4,
    0
);

machine.add(base);


// =====================================================
// TABLE
// =====================================================

const table =
    box(
        105,
        4,
        65,
        aluminum
    );

table.position.set(
    0,
    10,
    0
);

machine.add(table);


// =====================================================
// TABLE SLOTS
// =====================================================

for (
    let x = -45;
    x <= 45;
    x += 15
) {

    const slot =
        box(
            2,
            0.8,
            58,
            black
        );

    slot.position.set(
        x,
        12.2,
        0
    );

    machine.add(slot);
}


// =====================================================
// SIDE SUPPORTS
// =====================================================

const leftSupport =
    box(
        8,
        65,
        12,
        aluminum
    );

leftSupport.position.set(
    -52,
    42,
    0
);

machine.add(leftSupport);


const rightSupport =
    box(
        8,
        65,
        12,
        aluminum
    );

rightSupport.position.set(
    52,
    42,
    0
);

machine.add(rightSupport);


// =====================================================
// Y RAILS
// =====================================================

const leftRail =
    cylinder(
        2,
        70,
        darkMetal
    );

leftRail.rotation.z =
    Math.PI / 2;

leftRail.position.set(
    -52,
    18,
    0
);

machine.add(leftRail);


const rightRail =
    cylinder(
        2,
        70,
        darkMetal
    );

rightRail.rotation.z =
    Math.PI / 2;

rightRail.position.set(
    52,
    18,
    0
);

machine.add(rightRail);


// =====================================================
// GANTRY
// =====================================================

const gantry =
    new THREE.Group();

machine.add(gantry);


// =====================================================
// GANTRY COLUMNS
// =====================================================

const gantryLeft =
    box(
        8,
        60,
        10,
        aluminum
    );

gantryLeft.position.set(
    -48,
    50,
    0
);

gantry.add(gantryLeft);


const gantryRight =
    box(
        8,
        60,
        10,
        aluminum
    );

gantryRight.position.set(
    48,
    50,
    0
);

gantry.add(gantryRight);


// =====================================================
// GANTRY CROSS BEAM
// =====================================================

const crossBeam =
    box(
        105,
        12,
        12,
        aluminum
    );

crossBeam.position.set(
    0,
    78,
    0
);

gantry.add(crossBeam);


// =====================================================
// X RAILS
// =====================================================

const xRail1 =
    cylinder(
        2,
        92,
        darkMetal
    );

xRail1.rotation.z =
    Math.PI / 2;

xRail1.position.set(
    0,
    68,
    -7
);

gantry.add(xRail1);


const xRail2 =
    cylinder(
        2,
        92,
        darkMetal
    );

xRail2.rotation.z =
    Math.PI / 2;

xRail2.position.set(
    0,
    68,
    7
);

gantry.add(xRail2);


// =====================================================
// X CARRIAGE
// =====================================================

const carriage =
    new THREE.Group();

gantry.add(carriage);

carriage.position.set(
    0,
    0,
    0
);


// =====================================================
// CARRIAGE BODY
// =====================================================

const carriageBody =
    box(
        20,
        30,
        22,
        darkMetal
    );

carriageBody.position.set(
    0,
    58,
    0
);

carriage.add(carriageBody);


// =====================================================
// Z RAILS
// =====================================================

const zRailLeft =
    cylinder(
        1.8,
        45,
        darkMetal
    );

zRailLeft.position.set(
    -7,
    35,
    0
);

carriage.add(zRailLeft);


const zRailRight =
    cylinder(
        1.8,
        45,
        darkMetal
    );

zRailRight.position.set(
    7,
    35,
    0
);

carriage.add(zRailRight);


// =====================================================
// SPINDLE
// =====================================================

const spindle =
    new THREE.Group();

carriage.add(spindle);


// spindle body

const spindleBody =
    cylinder(
        7,
        28,
        black
    );

spindleBody.position.set(
    0,
    30,
    0
);

spindle.add(spindleBody);


// spindle nose

const spindleNose =
    cylinder(
        4,
        10,
        aluminum
    );

spindleNose.position.set(
    0,
    11,
    0
);

spindle.add(spindleNose);


// =====================================================
// TOOL
// =====================================================

const tool =
    cylinder(
        1.4,
        14,
        aluminum
    );

tool.position.set(
    0,
    0,
    0
);

spindle.add(tool);


// =====================================================
// WORKPIECE
// =====================================================

const workpiece =
    box(
        55,
        10,
        40,
        workMaterial
    );

workpiece.position.set(
    0,
    18,
    0
);

machine.add(workpiece);


// =====================================================
// TOOLPATH
// =====================================================

const pathMaterial =
    new THREE.LineBasicMaterial({
        color: 0xff3333
    });

const pathGeometry =
    new THREE.BufferGeometry();

const path =
    new THREE.Line(
        pathGeometry,
        pathMaterial
    );

scene.add(path);


// =====================================================
// GRID
// =====================================================

const grid =
    new THREE.GridHelper(
        220,
        22,
        0x555555,
        0x222222
    );

grid.position.y = 0;

scene.add(grid);


// =====================================================
// AXES
// =====================================================

const axes =
    new THREE.AxesHelper(
        40
    );

scene.add(axes);


// =====================================================
// MACHINE POSITION
// =====================================================

const machinePosition = {

    x: 0,
    y: 0,
    z: 0

};


// =====================================================
// UPDATE TOOL POSITION
// =====================================================

function updateMachine() {

    const x =
        machinePosition.x;

    const y =
        machinePosition.y;

    const z =
        machinePosition.z;


    // Y moves the gantry

    gantry.position.z =
        y;


    // X moves carriage

    carriage.position.x =
        x;


    // Z moves spindle

    spindle.position.y =
        -z;


    document
        .getElementById("pos-x")
        .textContent =
        x.toFixed(2);

    document
        .getElementById("pos-y")
        .textContent =
        y.toFixed(2);

    document
        .getElementById("pos-z")
        .textContent =
        z.toFixed(2);
}


// =====================================================
// DEMO MOTION
// =====================================================

let time = 0;

function demoMotion() {

    time += 0.008;

    machinePosition.x =
        Math.sin(time) * 35;

    machinePosition.y =
        Math.cos(time * 0.7) * 20;

    machinePosition.z =
        8 +
        Math.sin(time * 1.5) * 5;

    updateMachine();
}


// =====================================================
// RESIZE
// =====================================================

window.addEventListener(
    "resize",
    () => {

        camera.aspect =
            window.innerWidth /
            window.innerHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );

    }
);


// =====================================================
// ANIMATION
// =====================================================

function animate() {

    requestAnimationFrame(
        animate
    );

    demoMotion();

    controls.update();

    renderer.render(
        scene,
        camera
    );
}


updateMachine();

animate();
