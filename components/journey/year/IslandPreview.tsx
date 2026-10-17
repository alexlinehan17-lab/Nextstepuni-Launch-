/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { PaperGround, Scenery } from '../paper/TileArt';
import { coastalMap } from '../paper/collection';
import { WonderRaster } from '../visitors/VisitorArt';
import { islandPieces } from './yearIslands';
import type { YearIslandTile } from '../../../functions/src/islandProjection';

/** Home plus four rings: enough to recognise an island, cheap for a long list. */
const PREVIEW_TILES = 61;

/**
 * A still drawing of a classmate's island for the Your year list. It draws only
 * once its card is near the viewport, and never animates or repaints, so a long
 * year group costs nothing while the student scrolls past it.
 */
export function IslandPreview({ tiles, label }: { tiles: YearIslandTile[]; label: string }) {
  const ref = useRef<HTMLSpanElement>(null),
    [visible, setVisible] = useState(false);
  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        setVisible(true);
        observer.disconnect();
      }
    }, { rootMargin: '200px' });
    observer.observe(node);
    return () => observer.disconnect();
  }, []);
  // The projection lists tiles nearest home first, so a cap keeps the core.
  const cells = useMemo(() => islandPieces(tiles.slice(0, PREVIEW_TILES)), [tiles]);
  const viewBox = useMemo(() => {
    const xs = cells.map(cell => cell.x), ys = cells.map(cell => cell.y);
    const left = Math.min(...xs) - 110, right = Math.max(...xs) + 110;
    const top = Math.min(...ys) - 175, bottom = Math.max(...ys) + 95;
    return `${left} ${top} ${right - left} ${bottom - top}`;
  }, [cells]);
  return (
    <span ref={ref} className="year-island-preview" style={{ backgroundImage: `url(${coastalMap})` }}>
      {visible && (
        <svg viewBox={viewBox} preserveAspectRatio="xMidYMid meet" role="img" aria-label={label}>
          <PaperGround cells={cells} />
          {[...cells].sort((a, b) => a.y - b.y || a.x - b.x).map(cell => cell.wonderId
            ? <WonderRaster key={cell.key} id={cell.wonderId} x={cell.x} y={cell.y} />
            : <Scenery key={cell.key} kind={cell.kind} x={cell.x} y={cell.y} />)}
        </svg>
      )}
    </span>
  );
}
