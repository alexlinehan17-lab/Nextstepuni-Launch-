/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useRef, useState } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { useGLTF } from '@react-three/drei';
import { hexToWorld } from './hexGeometry';

const DECO_PATH = '/models/decorations/';

interface HexDecorationProps {
  q: number;
  r: number;
  /** Height of the hex tile this sits on */
  tileHeight: number;
  model: string;
  scale?: number;
  rotationY?: number;
  offsetX?: number;
  offsetZ?: number;
  animateIn?: boolean;
  delay?: number;
}

const HexDecoration: React.FC<HexDecorationProps> = ({
  q, r, tileHeight, model, scale = 1,
  rotationY = 0, offsetX = 0, offsetZ = 0,
  animateIn = false, delay = 0,
}) => {
  const { scene } = useGLTF(`${DECO_PATH}${model}`);
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

  const [wx, wz] = useMemo(() => hexToWorld(q, r), [q, r]);
  const ref = useRef<THREE.Group>(null);
  const startTime = useRef(-1);
  const [hasAnimated, setHasAnimated] = useState(false);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    if (!animateIn || hasAnimated) {
      ref.current.scale.setScalar(scale);
      return;
    }
    if (startTime.current < 0) startTime.current = clock.getElapsedTime();
    const elapsed = clock.getElapsedTime() - startTime.current - delay;
    if (elapsed < 0) {
      ref.current.scale.setScalar(0.001);
      return;
    }
    const t = Math.min(elapsed / 0.4, 1);
    // Bounce overshoot
    const ease = t < 0.6
      ? (t / 0.6) * (t / 0.6) * scale
      : scale + (scale * 0.15) * Math.sin((t - 0.6) / 0.4 * Math.PI);
    ref.current.scale.setScalar(Math.max(0.001, t >= 1 ? scale : ease));
    if (t >= 1) setHasAnimated(true);
  });

  return (
    <group
      ref={ref}
      position={[wx + offsetX, tileHeight, wz + offsetZ]}
      rotation={[0, rotationY, 0]}
      scale={animateIn && !hasAnimated ? 0.001 : scale}
    >
      <primitive object={cloned} />
    </group>
  );
};

export default React.memo(HexDecoration);
