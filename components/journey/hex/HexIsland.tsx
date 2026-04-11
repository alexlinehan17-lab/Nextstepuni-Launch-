/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useMemo } from 'react';
import HexTile from './HexTile';
import HexDecoration from './HexDecoration';
import SignDecoration from './SignDecoration';
import Water from './Water';
import { type IslandPlacement } from '../../../types';

/** Approximate height of a Kenney hex tile base surface */
const TILE_SURFACE_Y = 0.23;

/** How recently (ms) a purchase must be to trigger animate-in */
const ANIMATE_WINDOW_MS = 3000;

interface HexIslandProps {
  placements: IslandPlacement[];
  waterColor: string;
  northStarStatement?: string;
}

const HexIsland: React.FC<HexIslandProps> = ({ placements, waterColor, northStarStatement }) => {
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
          <HexTile
            key={`hex-${p.q},${p.r}`}
            q={p.q}
            r={p.r}
            model={p.model}
            rotation={p.rotation}
            animateIn={!!isNew}
            delay={0}
          />
        );
      })}

      {decorations.map((p, i) => {
        const isNew = p.purchasedAt && (now - new Date(p.purchasedAt).getTime()) < ANIMATE_WINDOW_MS;
        const isSign = p.model === 'sign.glb';

        if (isSign) {
          return (
            <SignDecoration
              key={`deco-${p.q},${p.r}-${i}`}
              q={p.q}
              r={p.r}
              tileHeight={TILE_SURFACE_Y}
              model={p.model}
              scale={p.scale}
              rotationY={p.rotation ? (p.rotation * Math.PI) / 3 : undefined}
              offsetX={p.offsetX}
              offsetZ={p.offsetZ}
              animateIn={!!isNew}
              delay={0}
              statement={northStarStatement}
            />
          );
        }

        return (
          <HexDecoration
            key={`deco-${p.q},${p.r}-${i}`}
            q={p.q}
            r={p.r}
            tileHeight={TILE_SURFACE_Y}
            model={p.model}
            scale={p.scale}
            rotationY={p.rotation ? (p.rotation * Math.PI) / 3 : undefined}
            offsetX={p.offsetX}
            offsetZ={p.offsetZ}
            animateIn={!!isNew}
            delay={0}
          />
        );
      })}
    </group>
  );
};

export default React.memo(HexIsland);
