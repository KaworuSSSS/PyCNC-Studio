/*
 * PyCNC Studio
 * Shared machine materials
 */

import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js";


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


export const aluminum =
    mat(
        0x626b70,
        0.85,
        0.28
    );


export const aluminumDark =
    mat(
        0x272d31,
        0.90,
        0.22
    );


export const aluminumLight =
    mat(
        0x9aa3a7,
        0.80,
        0.22
    );


export const black =
    mat(
        0x101315,
        0.88,
        0.20
    );


export const steel =
    mat(
        0xb8c0c4,
        0.94,
        0.15
    );


export const yellow =
    mat(
        0xd5a72a,
        0.55,
        0.30
    );


export const workMaterial =
    new THREE.MeshStandardMaterial({

        color: 0x30363a,

        metalness: 0.20,

        roughness: 0.70

    });
