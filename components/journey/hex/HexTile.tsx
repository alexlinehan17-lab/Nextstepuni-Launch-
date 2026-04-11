/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useRef, useState } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { useGLTF } from '@react-three/drei';
import { hexToWorld } from './hexGeometry';

const HEX_PATH = '/models/hex/';

interface HexTileProps {
  q: number;
  r: number;
  model: string;
  rotation?: number;
  radius?: number;
  animateIn?: boolean;
  delay?: number;
}

const HexTile: React.FC<HexTileProps> = ({
  q, r, model, rotation = 0, radius = 1,
  animateIn = false, delay = 0,
}) => {
  const { scene } = useGLTF(`${HEX_PATH}${model}`);
  const cloned = useMemo(() => {
    const clone = scene.clone(true);
    clone.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        mesh.castShadow = true;
        mesh.receiveShadow = true;
      }
    });
    return clone;
  }, [scene]);

  const [wx, wz] = useMemo(() => hexToWorld(q, r, radius), [q, r, radius]);
  const ref = useRef<THREE.Group>(null);
  const startTime = useRef(-1);
  const [hasAnimated, setHasAnimated] = useState(false);

  // Once animation completes, mark it done so model swaps don't re-trigger
  useFrame(({ clock }) => {
    if (!ref.current) return;
    if (!animateIn || hasAnimated) {
      ref.current.position.y = 0;
      ref.current.scale.setScalar(1);
      return;
    }
    if (startTime.current < 0) startTime.current = clock.getElapsedTime();
    const elapsed = clock.getElapsedTime() - startTime.current - delay;
    if (elapsed < 0) {
      ref.current.position.y = -3;
      ref.current.scale.setScalar(0.001);
      return;
    }
    const t = Math.min(elapsed / 0.6, 1);
    const ease = 1 - Math.pow(1 - t, 3);
    ref.current.position.y = -3 + ease * 3;
    ref.current.scale.setScalar(ease);
    if (t >= 1) setHasAnimated(true);
  });

  const rotY = (rotation * Math.PI) / 3;

  return (
    <group
      ref={ref}
      position={[wx, animateIn && !hasAnimated ? -3 : 0, wz]}
      rotation={[0, rotY, 0]}
      scale={animateIn && !hasAnimated ? 0.001 : 1}
    >
      <primitive object={cloned} />
    </group>
  );
};

export default React.memo(HexTile);
