/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { Suspense, memo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import type * as THREE from 'three';
import { type IslandPlacement } from '../../types';
import HexIsland from './hex/HexIsland';

/* ── Slow island bob ── */
const IslandFloat: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const ref = useRef<THREE.Group>(null);
  useFrame(({ clock }) => {
    if (ref.current) {
      ref.current.position.y = Math.sin(clock.getElapsedTime() * 0.5) * 0.05;
    }
  });
  return <group ref={ref}>{children}</group>;
};

/* ── Scene lighting ── */
const Lighting: React.FC = () => (
  <>
    <ambientLight intensity={0.5} color="#FFF8E7" />
    <directionalLight
      position={[8, 12, 6]}
      intensity={1.4}
      color="#FFFAF0"
      castShadow
      shadow-mapSize-width={2048}
      shadow-mapSize-height={2048}
      shadow-camera-left={-10}
      shadow-camera-right={10}
      shadow-camera-top={10}
      shadow-camera-bottom={-10}
    />
    <directionalLight position={[-5, 8, -5]} intensity={0.3} color="#B0D0FF" />
    <hemisphereLight args={['#87CEEB', '#3D6B35', 0.3]} />
  </>
);

/* ── Confetti celebration (DOM overlay) ── */
const CelebrationOverlay: React.FC = () => {
  const particles = useRef(
    Array.from({ length: 40 }, (_, i) => ({
      id: i,
      x: 40 + Math.random() * 20,
      delay: Math.random() * 0.5,
      duration: 1.2 + Math.random() * 0.8,
      color: ['#F59E0B', '#EF4444', '#3B82F6', '#10B981', '#8B5CF6', '#EC4899'][i % 6],
      size: 6 + Math.random() * 8,
      dx: (Math.random() - 0.5) * 250,
      dy: -(80 + Math.random() * 300),
      rot: Math.random() * 720,
    }))
  ).current;

  return (
    <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', zIndex: 9999, overflow: 'hidden' }}>
      {particles.map((p) => (
        <div
          key={p.id}
          style={{
            position: 'absolute',
            left: `${p.x}%`,
            bottom: '35%',
            width: p.size,
            height: p.size,
            borderRadius: p.id % 3 === 0 ? '50%' : '2px',
            backgroundColor: p.color,
            animation: `confetti-burst ${p.duration}s ease-out ${p.delay}s forwards`,
            opacity: 0,
            ['--cdx' as string]: `${p.dx}px`,
            ['--cdy' as string]: `${p.dy}px`,
            ['--crot' as string]: `${p.rot}deg`,
          }}
        />
      ))}
      <style>{`
        @keyframes confetti-burst {
          0%   { opacity: 1; transform: translate(0, 0) rotate(0deg); }
          100% { opacity: 0; transform: translate(var(--cdx), var(--cdy)) rotate(var(--crot)); }
        }
      `}</style>
    </div>
  );
};

/* ── Main component ── */
interface JourneyCanvasProps {
  placements: IslandPlacement[];
  waterColor: string;
  celebrationActive?: boolean;
  northStarStatement?: string;
}

const JourneyCanvas: React.FC<JourneyCanvasProps> = ({ placements, waterColor, celebrationActive = false, northStarStatement }) => {
  return (
    <div style={{ position: 'absolute', inset: 0 }}>
      <Canvas
        shadows
        camera={{ position: [6, 7, 6], fov: 35, near: 0.1, far: 200 }}
        gl={{ antialias: true }}
        style={{ background: '#2D2D44' }}
      >
        <color attach="background" args={['#2D2D44']} />
        <fog attach="fog" args={['#2D2D44', 18, 35]} />

        <Lighting />

        <Suspense fallback={null}>
          <IslandFloat>
            <HexIsland placements={placements} waterColor={waterColor} northStarStatement={northStarStatement} />
          </IslandFloat>
        </Suspense>

        <OrbitControls
          enablePan={false}
          enableZoom={true}
          minDistance={4}
          maxDistance={16}
          minPolarAngle={Math.PI / 6}
          maxPolarAngle={Math.PI / 2.8}
          target={[0, 0, 0]}
        />
      </Canvas>

      {celebrationActive && <CelebrationOverlay />}
    </div>
  );
};

export default memo(JourneyCanvas);
