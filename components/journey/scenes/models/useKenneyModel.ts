/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useMemo } from 'react';
import * as THREE from 'three';
import { useGLTF } from '@react-three/drei';

/* ═══════════════════════════════════════════
   SHARED TOON GRADIENT — 3-band cell shading
   Matches the one in SharedSceneElements.tsx
   ═══════════════════════════════════════════ */

const toonGradientTexture = (() => {
  const data = new Uint8Array([60, 140, 255]);
  const tex = new THREE.DataTexture(data, 3, 1, THREE.RedFormat);
  tex.minFilter = THREE.NearestFilter;
  tex.magFilter = THREE.NearestFilter;
  tex.needsUpdate = true;
  return tex;
})();

/* ═══════════════════════════════════════════
   useKenneyModel — load GLB, clone, apply toon
   ═══════════════════════════════════════════ */

interface UseKenneyModelOptions {
  /** Override all mesh colors to a single color */
  colorOverride?: string;
  /** Map material names → colors for multi-part coloring (e.g. Person shirt/pants/hair) */
  colorMap?: Record<string, string>;
}

/**
 * Loads a Kenney GLB model, clones the scene graph (so the same model
 * can appear multiple times), and replaces all MeshStandardMaterial
 * with MeshToonMaterial using the shared 3-band gradient.
 */
export function useKenneyModel(
  path: string,
  options: UseKenneyModelOptions = {},
): THREE.Group {
  const { scene } = useGLTF(path);
  const { colorOverride, colorMap } = options;

  const cloned = useMemo(() => {
    const clone = scene.clone(true);

    clone.traverse((node) => {
      if (!(node instanceof THREE.Mesh)) return;

      // Enable shadows
      node.castShadow = true;
      node.receiveShadow = true;

      // Get the original material(s)
      const materials = Array.isArray(node.material)
        ? node.material
        : [node.material];

      const newMaterials = materials.map((mat) => {
        // Determine color
        let color: THREE.Color;
        if (colorOverride) {
          color = new THREE.Color(colorOverride);
        } else if (colorMap && mat.name && colorMap[mat.name]) {
          color = new THREE.Color(colorMap[mat.name]);
        } else if (mat instanceof THREE.MeshStandardMaterial) {
          color = mat.color.clone();
        } else {
          color = new THREE.Color('#CCCCCC');
        }

        const toon = new THREE.MeshToonMaterial({
          color,
          gradientMap: toonGradientTexture,
        });
        toon.name = mat.name;
        return toon;
      });

      node.material = Array.isArray(node.material)
        ? newMaterials
        : newMaterials[0];
    });

    return clone;
  }, [scene, colorOverride, colorMap]);

  return cloned;
}
