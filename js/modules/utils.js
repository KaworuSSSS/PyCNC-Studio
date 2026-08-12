/*
 * PyCNC Studio
 * Shared geometry utilities
 */

import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";


export function box(
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

    mesh.castShadow = true;
    mesh.receiveShadow = true;

    return mesh;
}


export function addBox(
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


export function cylinder(
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

    mesh.castShadow = true;
    mesh.receiveShadow = true;

    return mesh;
}
