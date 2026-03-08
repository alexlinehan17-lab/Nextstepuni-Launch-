/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useRef } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';

/** Animated water plane surrounding the island */
const Water: React.FC<{ size?: number; color?: string }> = ({
  size = 60,
  color = '#3B9EBF',
}) => {
  const ref = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    ref.current.position.y = -0.15 + Math.sin(clock.getElapsedTime() * 0.8) * 0.03;
  });

  return (
    <mesh ref={ref} rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.15, 0]} receiveShadow>
      <circleGeometry args={[size, 64]} />
      <meshToonMaterial color={color} transparent opacity={0.85} />
    </mesh>
  );
};

export default React.memo(Water);
