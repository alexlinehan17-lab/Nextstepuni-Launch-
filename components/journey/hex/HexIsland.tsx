/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { Suspense, useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import HexTile from './HexTile';
import HexDecoration from './HexDecoration';
import SignDecoration from './SignDecoration';
import Water from './Water';
import { type IslandPlacement } from '../../../types';
import { hexToWorld } from './hexGeometry';

/** Approximate height of a Kenney hex tile base surface */
const TILE_SURFACE_Y = 0.23;

/** How recently (ms) a purchase must be to trigger animate-in */
const ANIMATE_WINDOW_MS = 3000;

/** A quick, lifted glide between build cells. Keeping the model mounted means
 * choosing another cell no longer produces a jarring remove-and-recreate. */
const FloatingPlacementPreview: React.FC<{
  q: number;
  r: number;
  children: React.ReactNode;
}> = ({ q, r, children }) => {
  const ref = useRef<THREE.Group>(null);
  const [targetX, targetZ] = hexToWorld(q, r);
  const firstFrame = useRef(true);

  useFrame((_, delta) => {
    if (!ref.current) return;
    if (firstFrame.current) {
      ref.current.position.set(targetX, 0.48, targetZ);
      firstFrame.current = false;
    }
    const distance = Math.hypot(targetX - ref.current.position.x, targetZ - ref.current.position.z);
    ref.current.position.x = THREE.MathUtils.damp(ref.current.position.x, targetX, 20, delta);
    ref.current.position.z = THREE.MathUtils.damp(ref.current.position.z, targetZ, 20, delta);
    const lift = distance > 0.015 ? Math.min(0.55, 0.14 + distance * 0.32) : 0;
    ref.current.position.y = THREE.MathUtils.damp(ref.current.position.y, lift, 22, delta);
  });

  return <group ref={ref}>{children}</group>;
};

interface HexIslandProps {
  placements: IslandPlacement[];
  waterColor: string;
  northStarStatement?: string;
  buildMode?: boolean;
  previewPlacement?: IslandPlacement | null;
  selectedPlacementId?: string | null;
  onSelectPlacement?: (placement: IslandPlacement) => void;
}

const HexIsland: React.FC<HexIslandProps> = ({
  placements, waterColor, northStarStatement, buildMode = false,
  previewPlacement, selectedPlacementId: _selectedPlacementId, onSelectPlacement,
}) => {
  const now = Date.now();

  // For hex placements at the same (q, r), last one wins (buildings override terrain)
  const hexTiles = useMemo(() => {
    const best = new Map<string, IslandPlacement>();
    for (const p of placements) {
      if (p.type !== 'hex') continue;
      const key = `${p.q},${p.r}`;
      best.set(key, p); // last write wins
    }
    return Array.from(best.values());
  }, [placements]);

  const decorations = useMemo(() => {
    return placements.filter(p => p.type === 'decoration');
  }, [placements]);

  return (
    <group>
      <Water size={40} color={waterColor} />

      {hexTiles.map((p) => {
        const isNew = p.purchasedAt && (now - new Date(p.purchasedAt).getTime()) < ANIMATE_WINDOW_MS;
        return (
          <Suspense key={`hex-${p.q},${p.r}`} fallback={null}>
            <HexTile
              q={p.q}
              r={p.r}
              model={p.model}
              rotation={p.rotation}
              animateIn={!!isNew && !buildMode}
              delay={0}
              onSelect={buildMode && p.placementId ? () => onSelectPlacement?.(p) : undefined}
            />
          </Suspense>
        );
      })}

      {decorations.map((p, i) => {
        const isNew = p.purchasedAt && (now - new Date(p.purchasedAt).getTime()) < ANIMATE_WINDOW_MS;
        const isSign = p.model === 'sign.glb';

        if (isSign) {
          return (
            <Suspense key={p.placementId ?? `deco-${p.q},${p.r}-${i}`} fallback={null}>
              <SignDecoration
                q={p.q}
                r={p.r}
                tileHeight={TILE_SURFACE_Y}
                model={p.model}
                scale={p.scale}
                rotationY={p.rotation ? (p.rotation * Math.PI) / 3 : undefined}
                offsetX={p.offsetX}
                offsetZ={p.offsetZ}
                animateIn={!!isNew && !buildMode}
                delay={0}
                statement={northStarStatement}
              />
            </Suspense>
          );
        }

        return (
          <Suspense key={p.placementId ?? `deco-${p.q},${p.r}-${i}`} fallback={null}>
          <HexDecoration
            q={p.q}
            r={p.r}
            tileHeight={TILE_SURFACE_Y}
            model={p.model}
            scale={p.scale}
            rotationY={p.rotation ? (p.rotation * Math.PI) / 3 : undefined}
            offsetX={p.offsetX}
            offsetZ={p.offsetZ}
            animateIn={!!isNew && !buildMode}
            delay={0}
            onSelect={buildMode && p.placementId ? () => onSelectPlacement?.(p) : undefined}
          />
          </Suspense>
        );
      })}

      {previewPlacement?.type === 'hex' && (
        <FloatingPlacementPreview q={previewPlacement.q} r={previewPlacement.r}>
          <Suspense fallback={null}>
            <HexTile q={0} r={0} model={previewPlacement.model} rotation={previewPlacement.rotation} />
          </Suspense>
        </FloatingPlacementPreview>
      )}
      {previewPlacement?.type === 'decoration' && (
        <FloatingPlacementPreview q={previewPlacement.q} r={previewPlacement.r}>
          <Suspense fallback={null}>
            <HexDecoration
              q={0}
              r={0}
              tileHeight={TILE_SURFACE_Y + 0.02}
              model={previewPlacement.model}
              scale={previewPlacement.scale}
              rotationY={previewPlacement.rotation ? (previewPlacement.rotation * Math.PI) / 3 : undefined}
              offsetX={previewPlacement.offsetX}
              offsetZ={previewPlacement.offsetZ}
            />
          </Suspense>
        </FloatingPlacementPreview>
      )}
    </group>
  );
};

export default React.memo(HexIsland);
