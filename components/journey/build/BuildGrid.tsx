import React, { useMemo } from 'react';
import type { ThreeEvent } from '@react-three/fiber';
import type { BuildCell } from './islandBuildModel';
import { hexToWorld } from '../hex/hexGeometry';

interface BuildGridProps {
  cells: BuildCell[];
  selectedCell?: { q: number; r: number } | null;
  onSelect: (cell: BuildCell) => void;
}

const BuildGrid: React.FC<BuildGridProps> = ({ cells, selectedCell, onSelect }) => {
  // Kenney's pointy-top tiles have a 0.577 outer radius. Matching that
  // footprint (and orientation) makes frontier cells share a full edge with
  // the island instead of appearing to balance between two corners.
  const geometryArgs = useMemo(() => [0.565, 0.565, 0.035, 6] as const, []);

  return (
    <group>
      {cells.map(cell => {
        const [x, z] = hexToWorld(cell.q, cell.r);
        const selected = selectedCell?.q === cell.q && selectedCell?.r === cell.r;
        const color = selected ? '#F26B1F' : cell.recommended ? '#9ED9C5' : cell.valid ? '#FFF4E8' : '#4A4745';
        return (
          <mesh
            key={`${cell.q},${cell.r}`}
            position={[x, cell.frontier ? 0.08 : 0.38, z]}
            rotation={[0, 0, 0]}
            onClick={(event: ThreeEvent<MouseEvent>) => {
              event.stopPropagation();
              onSelect(cell);
            }}
            onPointerOver={(event: ThreeEvent<PointerEvent>) => {
              event.stopPropagation();
              document.body.style.cursor = cell.valid ? 'pointer' : 'not-allowed';
            }}
            onPointerOut={() => { document.body.style.cursor = 'default'; }}
          >
            <cylinderGeometry args={geometryArgs} />
            <meshBasicMaterial
              color={color}
              transparent
              opacity={selected ? 0.72 : cell.valid ? 0.38 : 0.2}
              depthWrite={false}
            />
          </mesh>
        );
      })}
    </group>
  );
};

export default BuildGrid;
