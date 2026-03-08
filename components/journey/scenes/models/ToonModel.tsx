/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { useKenneyModel } from './useKenneyModel';

/**
 * Generic component for simple static props that don't need
 * animations or special logic. Just loads a GLB and renders it.
 */
interface ToonModelProps {
  path: string;
  position?: [number, number, number];
  rotation?: [number, number, number];
  scale?: number | [number, number, number];
  colorOverride?: string;
  colorMap?: Record<string, string>;
}

export const ToonModel: React.FC<ToonModelProps> = ({
  path,
  position = [0, 0, 0],
  rotation = [0, 0, 0],
  scale = 1,
  colorOverride,
  colorMap,
}) => {
  const scene = useKenneyModel(path, { colorOverride, colorMap });
  const scaleArr: [number, number, number] = Array.isArray(scale)
    ? scale
    : [scale, scale, scale];

  return (
    <group position={position} rotation={rotation} scale={scaleArr}>
      <primitive object={scene} />
    </group>
  );
};
