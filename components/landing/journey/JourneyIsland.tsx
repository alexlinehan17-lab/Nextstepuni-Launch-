import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Undo2, RotateCcw } from 'lucide-react';
import { TileCluster, TilePortrait, Scenery, PaperGround } from '../../journey/paper/TileArt';
import { PaintedWorld } from '../../journey/paper/PaintedWorld';
import { points } from '../../journey/paper/geometry';
import { tileById, type TileKind } from '../../journey/paper/catalogue';
import { COPY } from '../copy';
import { INITIAL_ISLAND, PREVIEW_TILES, openEdges, placePreviewTile, previewView } from './islandPreview';

export default function JourneyIsland() {
  const [placed, setPlaced] = useState(INITIAL_ISLAND);
  const [selected, setSelected] = useState<TileKind>('treehouse');
  const [hovered, setHovered] = useState<string | null>(null);
  const [announcement, setAnnouncement] = useState('');
  const [aspect, setAspect] = useState(2.15);
  const map = useRef<HTMLDivElement>(null);
  const edgeButtons = useRef(new Map<string, HTMLButtonElement>());
  const focusNextEdge = useRef(false);
  const open = useMemo(() => openEdges(placed), [placed]);
  const view = useMemo(() => previewView(placed, aspect), [placed, aspect]);
  const preview = open.find(c => c.key === hovered);
  const copy = COPY.journey;

  useEffect(() => {
    const observer = new ResizeObserver(([entry]) => {
      if (entry.contentRect.width && entry.contentRect.height) {
        setAspect(entry.contentRect.width / entry.contentRect.height);
      }
    });
    if (map.current) observer.observe(map.current);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (focusNextEdge.current) {
      focusNextEdge.current = false;
      edgeButtons.current.get(open[0]?.key)?.focus();
    }
  }, [open]);

  function place(key: string, keyboard: boolean) {
    // Recheck against the latest island, so rapid clicks cannot occupy a cell twice.
    setPlaced(current => placePreviewTile(current, key, selected));
    setHovered(null);
    focusNextEdge.current = keyboard;
    setAnnouncement(`${tileById[selected].name} placed. Your island is growing.`);
  }

  return (
    <div className="journey-demo">
      <div className="journey-demo-top">
        <div>
          <p className="journey-demo-eyebrow">Your little elsewhere</p>
          <p className="journey-demo-count">{placed.length} tiles. Plenty of room to grow.</p>
        </div>
        <div className="journey-demo-tools">
          <button type="button" disabled={placed.length === INITIAL_ISLAND.length} onClick={() => {
            setPlaced(current => current.length > INITIAL_ISLAND.length ? current.slice(0, -1) : current);
            setHovered(null);
            setAnnouncement('Last tile removed. Choose what comes next.');
          }}><Undo2 size={16} aria-hidden="true" />{copy.undo}</button>
          <button type="button" disabled={placed.length === INITIAL_ISLAND.length} onClick={() => {
            setPlaced(INITIAL_ISLAND);
            setHovered(null);
            setAnnouncement('Back to your first three tiles. Start a different island.');
          }}><RotateCcw size={15} aria-hidden="true" />{copy.reset}</button>
        </div>
      </div>

      <div ref={map} className="journey-demo-map" role="group" aria-label="Your island preview" aria-describedby="journey-demo-instruction">
        <PaintedWorld placed={placed} style="pencilatlas" view={view} paperWidth={1400} />
        <svg viewBox={`${view.x} ${view.y} ${view.width} ${view.height}`} className="journey-demo-art" aria-hidden="true">
          {open.map(cell => (
            <g key={cell.key} className={`journey-demo-edge${cell.key === hovered ? ' is-active' : ''}`}>
              <polygon points={points(cell.x, cell.y)} />
              <path d={`M${cell.x - 7},${cell.y}h14M${cell.x},${cell.y - 7}v14`} />
            </g>
          ))}
          <TileCluster cells={placed} />
          {preview && <g opacity="0.65">
            <PaperGround cells={[preview]} edgeStyle="classic" />
            <Scenery kind={selected} x={preview.x} y={preview.y} />
            <polygon points={points(preview.x, preview.y)} fill="none" stroke="#c35319" strokeWidth="3" />
          </g>}
        </svg>
        {open.map((cell, index) => (
          <button
            key={cell.key}
            ref={element => { if (element) edgeButtons.current.set(cell.key, element); else edgeButtons.current.delete(cell.key); }}
            type="button"
            className="journey-demo-place"
            aria-label={`Place ${tileById[selected].name} at open edge ${index + 1}`}
            style={{ left: `${(cell.x - 84 - view.x) / view.width * 100}%`, top: `${(cell.y - 56 - view.y) / view.height * 100}%`, width: `${168 / view.width * 100}%`, height: `${112 / view.height * 100}%` }}
            onPointerEnter={event => { if (event.pointerType !== 'touch') setHovered(cell.key); }}
            onPointerLeave={() => setHovered(null)}
            onFocus={() => setHovered(cell.key)}
            onBlur={() => setHovered(null)}
            onClick={event => place(cell.key, event.detail === 0)}
          />
        ))}
        <span className="sr-only">On your island: {placed.map(p => tileById[p.kind].name).join(', ')}.</span>
      </div>

      <div className="journey-demo-shelf">
        <div className="journey-demo-shelf-heading">
          <h3>{copy.preview}</h3>
          <p id="journey-demo-instruction">{copy.instruction}</p>
        </div>
        <div className="journey-demo-tiles" role="group" aria-label="Choose a tile">
          {PREVIEW_TILES.map(kind => (
            <button type="button" key={kind} aria-pressed={selected === kind} aria-label={`Choose ${tileById[kind].name}`} onClick={event => {
              setSelected(kind);
              setAnnouncement(`${tileById[kind].name} selected. Choose a plus on the map to place it.`);
              if (event.detail === 0) edgeButtons.current.get(open[0]?.key)?.focus();
              else if (map.current && map.current.getBoundingClientRect().top < 68) {
                map.current.scrollIntoView({ block: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
              }
            }}>
              <span className="journey-demo-portrait" aria-hidden="true"><TilePortrait kind={kind} /></span>
              <span>{tileById[kind].name}</span>
              <span className="journey-demo-tile-action" aria-hidden="true">{selected === kind ? 'Ready to place' : 'Choose tile'}</span>
            </button>
          ))}
        </div>
        <p className="journey-demo-note">{copy.note}</p>
      </div>
      <p role="status" className="sr-only" aria-live="polite" aria-atomic="true">{announcement}</p>
    </div>
  );
}
