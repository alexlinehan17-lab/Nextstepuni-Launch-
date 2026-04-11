/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo, useRef, useState } from 'react';
import type * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import { useGLTF, Html } from '@react-three/drei';
import { hexToWorld } from './hexGeometry';

const DECO_PATH = '/models/decorations/';

interface SignDecorationProps {
  q: number;
  r: number;
  tileHeight: number;
  model: string;
  scale?: number;
  rotationY?: number;
  offsetX?: number;
  offsetZ?: number;
  animateIn?: boolean;
  delay?: number;
  statement?: string;
}

const SignDecoration: React.FC<SignDecorationProps> = ({
  q, r, tileHeight, model, scale = 1,
  rotationY = 0, offsetX = 0, offsetZ = 0,
  animateIn = false, delay = 0, statement,
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
    const ease = t < 0.6
      ? (t / 0.6) * (t / 0.6) * scale
      : scale + (scale * 0.15) * Math.sin((t - 0.6) / 0.4 * Math.PI);
    ref.current.scale.setScalar(Math.max(0.001, t >= 1 ? scale : ease));
    if (t >= 1) setHasAnimated(true);
  });

  const truncated = statement ? (statement.length > 40 ? statement.slice(0, 37) + '...' : statement) : '';
  const [showLabel, setShowLabel] = useState(true);

  return (
    <group
      ref={ref}
      position={[wx + offsetX, tileHeight, wz + offsetZ]}
      rotation={[0, rotationY, 0]}
      scale={animateIn && !hasAnimated ? 0.001 : scale}
      onClick={(e) => { e.stopPropagation(); setShowLabel(v => !v); }}
      onPointerOver={() => { document.body.style.cursor = 'pointer'; }}
      onPointerOut={() => { document.body.style.cursor = 'auto'; }}
    >
      <primitive object={cloned} />
      {truncated && showLabel && (
        <Html
          position={[0, 0.7, 0]}
          center
          distanceFactor={8}
          style={{ pointerEvents: 'none' }}
        >
          <div style={{
            background: 'rgba(0,0,0,0.65)',
            color: '#fff',
            fontSize: '10px',
            fontWeight: 600,
            padding: '3px 8px',
            borderRadius: '6px',
            whiteSpace: 'nowrap',
            maxWidth: '140px',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            fontFamily: 'system-ui, sans-serif',
            lineHeight: 1.3,
          }}>
            {truncated}
          </div>
        </Html>
      )}
    </group>
  );
};

export default React.memo(SignDecoration);
