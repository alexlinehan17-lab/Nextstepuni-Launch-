import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import {
  ArrowUpRight,
  Check,
  Home,
  Minus,
  Move,
  Plus,
  Undo2,
  X,
} from "lucide-react";
import {
  frontier,
  visibleDiscoveries,
  buildable,
  groupFor,
  shelfGroups,
  type IslandState,
  type ShelfGroup,
} from "./model";
import { PaperGround, Scenery, TilePortrait } from "./TileArt";
import { tileById, type TileKind } from "./catalogue";
import { PaintedWorld } from "./PaintedWorld";
import { centre, points } from "./geometry";
import { piece } from "./studioModel";
import { PAPER_LANDMARKS } from "../../../functions/src/paperIslandModel";
import { OpenCorners } from "./OpenCorners";
import { legendById, stickerSrc, type LegendId } from "./collection";
import { StickerRaster } from "./StickerArt";
import { crewArt, crewById, type CrewId } from "../visitors/catalogue";
import { WonderRaster, WonderTileArt } from "../visitors/VisitorArt";
export const defaultCamera = { x: 0, y: -75, zoom: 1 };
export type Camera = typeof defaultCamera;
/** The pan layer is this many times the visible map in each direction (paper.css
 * `.island-pan`, inset -25%), so a drag uncovers painted sea, not bare container. */
const OVERSCAN = 1.5;
const bound = (camera: Camera): Camera => ({
  x: Number.isFinite(camera.x) ? camera.x : 0,
  y: Number.isFinite(camera.y) ? camera.y : 0,
  zoom: Math.max(0.8, Math.min(1.8, camera.zoom)),
});
export function IslandMap({
  world,
  building,
  chosen,
  chosenWonder,
  candidate,
  onCandidate,
  onInspect,
  onDiscover,
  onTreasure,
  onInspectWonder,
  visitor,
  onVisit,
  camera,
  setCamera,
  editable,
  selectedTile,
  onSelectTile,
}: {
  world: IslandState;
  building: boolean;
  chosen: TileKind;
  chosenWonder?: CrewId | null;
  candidate: string | null;
  onCandidate: (key: string) => void;
  onInspect: (kind: TileKind) => void;
  onDiscover: (id: LegendId) => void;
  onTreasure: (id: string) => void;
  onInspectWonder?: (id: CrewId) => void;
  visitor?: { id:CrewId; q:number; r:number };
  onVisit?: (id:CrewId) => void;
  camera: Camera;
  setCamera: React.Dispatch<React.SetStateAction<Camera>>;
  /** Build mode: placed tiles that can be swapped or removed, by cell key → name. */
  editable?: Map<string, string>;
  selectedTile?: string | null;
  onSelectTile?: (key: string) => void;
}) {
  const [narrow, setNarrow] = useState(
    () => window.matchMedia("(max-width:700px)").matches,
  );
  useEffect(() => {
    const media = window.matchMedia("(max-width:700px)"),
      change = () => setNarrow(media.matches);
    media.addEventListener("change", change);
    return () => media.removeEventListener("change", change);
  }, []);
  const renderZoom = camera.zoom * (narrow ? (building ? 1.2 : 0.8) : 1),
    renderY = camera.y;
  // A drag moves the whole map as one composited layer and commits the camera
  // once, on release. Committing it per pointermove re-rendered every tile and
  // rebuilt the painted world (four full-size canvases) on every finger
  // movement — the island lag students reported on school iPads (2026-10-12).
  const panRef = useRef<HTMLDivElement>(null),
    frame = useRef(0),
    drag = useRef<{
      x: number;
      y: number;
      px: number;
      py: number;
      scale: number;
      dx: number;
      dy: number;
      /** Furthest the layer may shift before its overscan edge shows (px). */
      reachX: number;
      reachY: number;
    } | null>(null),
    movingWonder=chosenWonder?world.placed.find(cell=>cell.wonderId===chosenWonder):undefined,
    slots = frontier(chosenWonder?world.placed.filter(cell=>cell.wonderId!==chosenWonder):world.placed)
      .filter(slot=>slot.key!==movingWonder?.key),
    preview = building ? slots.find((c) => c.key === candidate) : undefined,
    seen = visibleDiscoveries(world.placed),
    ghost = preview ? piece(preview.q, preview.r, chosen,undefined,chosenWonder??undefined) : null;
  const selectedName=chosenWonder?crewById[chosenWonder].wonder:tileById[chosen].name;
  // The overscanned layer scales its CSS box and its viewBox by the same
  // factor, so world units per pixel and the centre are unchanged.
  const view = {
    x: camera.x - (920 * OVERSCAN) / renderZoom,
    y: renderY - (620 * OVERSCAN) / renderZoom,
    width: (1840 * OVERSCAN) / renderZoom,
    height: (1240 * OVERSCAN) / renderZoom,
  };
  // The new camera and the cleared offset reach the screen in the same frame:
  // layout effects run before paint, and PaintedWorld repaints in its own.
  useLayoutEffect(() => {
    if (panRef.current) panRef.current.style.transform = "";
  }, [camera.x, camera.y, renderZoom]);
  useEffect(() => () => cancelAnimationFrame(frame.current), []);
  const endDrag = () => {
    const p = drag.current;
    drag.current = null;
    cancelAnimationFrame(frame.current);
    frame.current = 0;
    if (!p || (!p.dx && !p.dy)) {
      if (panRef.current) panRef.current.style.transform = "";
      return;
    }
    setCamera((c) =>
      bound({ ...c, x: p.px - p.dx * p.scale, y: p.py - p.dy * p.scale }),
    );
  };
  return (
    <div className="island-map-container">
      <div className="island-pan" ref={panRef}>
        <PaintedWorld placed={world.placed} style="pencilatlas" view={view} />
        <svg
          className="student-map"
          viewBox={`${view.x} ${view.y} ${view.width} ${view.height}`}
          preserveAspectRatio="xMidYMid slice"
          role="group"
          tabIndex={0}
          aria-label="Your island. Drag to explore, use arrow keys to pan, or select an open corner in build mode."
          onPointerDown={(e) => {
            if ((e.target as Element).closest("[data-map-control]")) return;
            const rect = e.currentTarget.getBoundingClientRect();
            drag.current = {
              x: e.clientX,
              y: e.clientY,
              px: camera.x,
              py: camera.y,
              scale: Math.min(view.width / rect.width, view.height / rect.height),
              dx: 0,
              dy: 0,
              reachX: (rect.width * (OVERSCAN - 1)) / OVERSCAN / 2 * 0.8,
              reachY: (rect.height * (OVERSCAN - 1)) / OVERSCAN / 2 * 0.8,
            };
            e.currentTarget.setPointerCapture(e.pointerId);
          }}
          onPointerMove={(e) => {
            const p = drag.current;
            if (!p) return;
            // Whole pixels: a fractional offset can make WebKit re-rasterise the layer.
            p.dx = Math.round(e.clientX - p.x);
            p.dy = Math.round(e.clientY - p.y);
            if (!frame.current)
              frame.current = requestAnimationFrame(() => {
                frame.current = 0;
                const q = drag.current;
                if (!q || !panRef.current) return;
                if (Math.abs(q.dx) > q.reachX || Math.abs(q.dy) > q.reachY) {
                  // A long drag would uncover the edge of the overscan: commit
                  // the camera here and carry on from the new origin.
                  const x = q.px - q.dx * q.scale,
                    y = q.py - q.dy * q.scale;
                  Object.assign(q, { x: q.x + q.dx, y: q.y + q.dy, px: x, py: y, dx: 0, dy: 0 });
                  setCamera((c) => bound({ ...c, x, y }));
                  return;
                }
                panRef.current.style.transform = `translate3d(${q.dx}px, ${q.dy}px, 0)`;
              });
          }}
          onPointerUp={endDrag}
          onPointerCancel={endDrag}
          onKeyDown={(e) => {
            if (e.target !== e.currentTarget) return;
            const moves: Record<string, [number, number]> = {
              ArrowLeft: [-75, 0],
              ArrowRight: [75, 0],
              ArrowUp: [0, -75],
              ArrowDown: [0, 75],
            };
            if (moves[e.key]) {
              e.preventDefault();
              const [x, y] = moves[e.key];
              setCamera((c) => bound({ ...c, x: c.x + x, y: c.y + y }));
            }
            if (e.key === "Home") {
              e.preventDefault();
              setCamera(defaultCamera);
            }
          }}
        >
          {building &&
            slots.map((cell, index) => (
              <g
                key={cell.key}
                data-map-control="slot"
                data-open-corner={cell.key}
                role="button"
                tabIndex={0}
                aria-label={`Preview ${selectedName} at open corner ${index + 1}`}
                aria-pressed={candidate === cell.key}
                transform={`translate(${cell.x} ${cell.y})`}
                className={`map-placement-slot ${candidate === cell.key ? "selected" : ""}`}
                onClick={() => onCandidate(cell.key)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    onCandidate(cell.key);
                  }
                }}
              >
                <polygon points={points()} fill="transparent" />
                <OpenCorners />
                <polygon
                  className="slot-highlight"
                  points={points()}
                  pointerEvents="none"
                />
              </g>
            ))}
          <g pointerEvents="none">
            <PaperGround cells={world.placed} />
            {ghost && <PaperGround cells={[ghost]} opacity={0.66} />}
            {/* The selected tile's wash sits on the ground, under the scenery,
                so it never tints a neighbour's tall art; the outline stays on top. */}
            {building && selectedTile && (() => {
              const cell = world.placed.find(c => c.key === selectedTile);
              return cell ? <polygon className="island-tile-edit-wash" points={points(cell.x, cell.y)} /> : null;
            })()}
          </g>
          {[...world.placed, ...(ghost ? [ghost] : [])]
            .sort((a, b) => a.y - b.y || a.x - b.x)
            .map((cell) => (
              <g
                key={cell.key}
                data-island-tile={cell.key === ghost?.key ? undefined : cell.kind}
                data-cell={cell.key}
                data-ink-edge={cell.inkEdge.variant}
                data-wonder-tile={cell.key===ghost?.key?undefined:cell.wonderId}
                pointerEvents={building ? "none" : undefined}
                opacity={cell.key === ghost?.key ? 0.68 : 1}
              >
                {cell.wonderId?<WonderRaster id={cell.wonderId} x={cell.x} y={cell.y}/>:<Scenery kind={cell.kind} x={cell.x} y={cell.y} />}
              </g>
            ))}
          {!building &&
            world.placed.map((cell) => (
              <polygon
                key={cell.key}
                data-map-control="tile"
                className="island-tile-hit"
                points={points(cell.x, cell.y)}
                fill="transparent"
                role="button"
                tabIndex={0}
                aria-label={`Inspect ${cell.wonderId?crewById[cell.wonderId].wonder:tileById[cell.kind].name}`}
                onClick={() => {
                  const cache = PAPER_LANDMARKS.find(
                    (d) =>
                      d.q === cell.q && d.r === cell.r && d.kind === "treasure",
                  );
                  if (cache) onTreasure(cache.id);
                  else if (cell.wonderId) onInspectWonder?.(cell.wonderId);
                  else onInspect(cell.kind);
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    if (cell.wonderId) onInspectWonder?.(cell.wonderId);
                    else onInspect(cell.kind);
                  }
                }}
              />
            ))}
          {building && editable && world.placed.filter(cell => editable.has(cell.key)).map(cell => {
            const selected = selectedTile === cell.key, name = editable.get(cell.key)!;
            return (
              <polygon
                key={`edit-${cell.key}`}
                data-map-control="tile-edit"
                data-edit-tile={cell.key}
                className={`island-tile-edit ${selected ? "selected" : ""}`}
                points={points(cell.x, cell.y)}
                role="button"
                tabIndex={0}
                aria-label={`Swap or remove ${name}`}
                aria-pressed={selected}
                onClick={() => onSelectTile?.(cell.key)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    onSelectTile?.(cell.key);
                  }
                }}
              />
            );
          })}
          {ghost && (
            <polygon
              points={points(ghost.x, ghost.y)}
              fill="none"
              stroke="#f87628"
              strokeWidth="3"
              pointerEvents="none"
              data-placement-preview={ghost.key}
            />
          )}
          {seen.map((d) => {
            const pos = centre(d.q, d.r);
            return (
              <g
                key={d.id}
                transform={`translate(${pos.x} ${pos.y})`}
                data-map-control="discovery"
                data-visible-discovery={d.id}
                className="student-discovery"
                role="button"
                tabIndex={0}
                aria-label={`Discover ${legendById[d.id].name}`}
                onClick={() => onDiscover(d.id)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    onDiscover(d.id);
                  }
                }}
              >
                <circle r="100" className="discovery-focus" />
                <StickerRaster
                  src={stickerSrc(d.id)}
                  x={-80}
                  y={-80}
                  size={160}
                />
              </g>
            );
          })}
          {!building&&visitor&&onVisit&&<g
            className="map-visitor" data-map-control="visitor" data-visitor={visitor.id}
            transform={`translate(${centre(visitor.q,visitor.r).x+70} ${centre(visitor.q,visitor.r).y-190})`}
            role="button" tabIndex={0} aria-label={`Meet ${crewById[visitor.id].name}`}
            onClick={()=>onVisit(visitor.id)} onKeyDown={event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();onVisit(visitor.id);}}}
          ><image href={crewArt(visitor.id)} x="-52" y="-100" width="104" height="104"/><rect x="-54" y="7" width="108" height="29" rx="5"/><text y="27">{crewById[visitor.id].name}</text></g>}
        </svg>
      </div>
      <div className="map-navigation">
        <span>
          <Move size={13} /> Drag to explore
        </span>
        <div>
          <button
            aria-label="Zoom out"
            disabled={camera.zoom <= 0.8}
            onClick={() =>
              setCamera((c) => bound({ ...c, zoom: c.zoom - 0.15 }))
            }
          >
            <Minus size={17} />
          </button>
          <small>{Math.round(camera.zoom * 100)}%</small>
          <button
            aria-label="Zoom in"
            disabled={camera.zoom >= 1.8}
            onClick={() =>
              setCamera((c) => bound({ ...c, zoom: c.zoom + 0.15 }))
            }
          >
            <Plus size={17} />
          </button>
          <button
            aria-label="Centre island"
            onClick={() => setCamera(defaultCamera)}
          >
            <Home size={17} />
          </button>
        </div>
      </div>
    </div>
  );
}

function ShelfPortrait({ kind }: { kind: TileKind }) {
  const ref = useRef<HTMLSpanElement>(null),
    [visible, setVisible] = useState(false);
  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { rootMargin: "150px" },
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, []);
  return (
    <span ref={ref} className="shelf-portrait">
      {visible ? <TilePortrait kind={kind} /> : null}
    </span>
  );
}

export function TileShelf({
  chosen,
  chosenWonder,
  wonders=[],
  onChooseWonder,
  onChoose,
  balance,
  credits = 0,
  group,
  setGroup,
  orientation,
}: {
  chosen: TileKind;
  chosenWonder?: CrewId | null;
  wonders?: CrewId[];
  onChooseWonder?: (id:CrewId)=>void;
  onChoose: (kind: TileKind) => void;
  balance: number;
  credits?: number;
  group: ShelfGroup;
  setGroup: (group: ShelfGroup) => void;
  orientation: "row" | "column";
}) {
  const scroller = useRef<HTMLDivElement>(null),
    items = buildable.filter(
      (t) => group === "All tiles" || groupFor(t.id) === group,
    ),groups=wonders.length?[...shelfGroups,"Wonder tiles" as const]:shelfGroups;
  useEffect(() => {
    scroller.current?.scrollTo({ left: 0, top: 0, behavior: "instant" });
  }, [group]);
  useEffect(() => {
    const track = scroller.current;
    if (!track) return;
    const wheel = (event: WheelEvent) => {
      if (
        !event.ctrlKey &&
        Math.abs(event.deltaY) > Math.abs(event.deltaX) &&
        track.scrollWidth > track.clientWidth
      ) {
        event.preventDefault();
        track.scrollLeft +=
          event.deltaY *
          (event.deltaMode === 1
            ? 16
            : event.deltaMode === 2
              ? track.clientWidth
              : 1);
      }
    };
    track.addEventListener("wheel", wheel, { passive: false });
    return () => track.removeEventListener("wheel", wheel);
  }, []);
  return (
    <section
      className={`tile-shelf ${orientation}`}
      aria-label="Tile collection"
    >
      <div className="category-heading">
        <nav className="tile-categories" aria-label="Tile categories">
          {groups.map((name) => (
            <button
              key={name}
              aria-pressed={group === name}
              onClick={() => setGroup(name)}
            >
              {name}
            </button>
          ))}
        </nav>
        <span>{group==="Wonder tiles"?wonders.length:items.length} tiles</span>
      </div>
      <div className="student-tile-grid" ref={scroller}>
        {items.map((item) => {
          const t = {
            ...item,
            price: item.id === "meadow" && credits > 0 ? 0 : item.price,
          };
          return (
            <button
              className="shelf-tile"
              key={t.id}
              aria-label={`Choose ${t.name}`}
              aria-pressed={!chosenWonder&&chosen === t.id}
              onClick={() => onChoose(t.id)}
            >
              <ShelfPortrait kind={t.id} />
              <strong>{t.name}</strong>
              <span className={t.price > balance ? "over-budget" : ""}>
                {t.id === "meadow" && credits > 0
                  ? `${credits} earned tiles`
                  : `${t.price} JP`}
              </span>
            </button>
          );
        })}
        {group==="Wonder tiles"&&wonders.map(id=><button className="shelf-tile" key={id} aria-label={`Choose ${crewById[id].wonder}`} aria-pressed={chosenWonder===id} onClick={()=>onChooseWonder?.(id)}><span className="shelf-portrait"><WonderTileArt id={id} className="tile-portrait"/></span><strong>{crewById[id].wonder}</strong><span>Earned · yours to place</span></button>)}
      </div>
    </section>
  );
}

export function Placement({
  world,
  chosen,
  chosenWonder,
  candidate,
  onPlace,
  onUndo,
  busy = false,
  full = false,
}: {
  world: IslandState;
  chosen: TileKind;
  chosenWonder?: CrewId | null;
  candidate: string | null;
  onPlace: () => void;
  onUndo: () => void;
  busy?: boolean;
  full?: boolean;
}) {
  const item = chosenWonder?{...tileById.meadow,name:crewById[chosenWonder].wonder,description:crewById[chosenWonder].wonderStory,price:0}:tileById[chosen],
    t = {
      ...item,
      price: chosenWonder||chosen === "meadow" && world.credits > 0 ? 0 : item.price,
    },
    canPay = world.balance >= t.price;
  return (
    <aside
      className={`placement-inspector ${full ? "full" : ""}`}
      aria-label="Your selected tile"
    >
      {full && (chosenWonder?<WonderTileArt id={chosenWonder}/>:<TilePortrait kind={chosen} />)}
      <div className="placement-title">
        <h3>{t.name}</h3>
        <span>{chosenWonder?"A visitor’s gift":`${t.price} JP`}</span>
      </div>
      {full && <p>{t.description}</p>}
      <button
        className="primary-action place-action"
        disabled={busy || !candidate || !canPay}
        onClick={onPlace}
      >
        {busy
          ? "Saving…"
          : !canPay
            ? `Save ${t.price - world.balance} more JP`
            : candidate
              ? chosenWonder?(world.placed.some(tile=>tile.wonderId===chosenWonder)?"Move this Wonder":"Place this Wonder"):"Place this tile"
              : "Select a spot on your island"}
        <span>
          {candidate && canPay ? (
            <Check size={17} />
          ) : (
            <ArrowUpRight size={19} />
          )}
        </span>
      </button>
      <div className="placement-foot">
        <span>
          {candidate && canPay
            ? chosenWonder?"Your gift · no Journey Points needed":`${world.balance - t.price} JP left after placing`
            : "Tap a tile on your island to swap or remove it"}
        </span>
        <button
          aria-label="Undo last placement"
          disabled={busy || !world.history.length}
          onClick={onUndo}
        >
          <Undo2 size={14} /> Undo
        </button>
      </div>
    </aside>
  );
}

/** Build mode, a placed tile selected: swap it for the shelf tile, or take it off. */
export function TileEditor({
  name,
  replaceName,
  replaceNote,
  replaceBlock,
  removeNote,
  removeBlock,
  note,
  busy,
  onReplace,
  onRemove,
  onClose,
}: {
  name: string;
  replaceName: string;
  replaceNote: string;
  replaceBlock: string | null;
  removeNote: string;
  removeBlock: string | null;
  /** Why a button is unavailable, when one is. */
  note: string | null;
  busy: boolean;
  onReplace: () => void;
  onRemove: () => void;
  onClose: () => void;
}) {
  return (
    <aside className="placement-inspector tile-editor" aria-label={`Change ${name}`}>
      <div className="placement-title">
        <h3>{name}</h3>
        <button className="tile-editor-close" aria-label="Stop changing this tile" onClick={onClose}>
          <X size={16} />
        </button>
      </div>
      <div className="tile-editor-actions">
        <button
          className="primary-action place-action"
          disabled={busy || !!replaceBlock}
          onClick={onReplace}
        >
          <span>{busy ? "Saving…" : `Swap for ${replaceName}`}</span>
          <small>{replaceNote}</small>
        </button>
        <button
          className="quiet-action place-action tile-remove-action"
          disabled={busy || !!removeBlock}
          onClick={onRemove}
        >
          <span>Remove tile</span>
          <small>{removeNote}</small>
        </button>
      </div>
      <p className="tile-editor-note" role={note ? "status" : undefined}>
        {note || "Choose a shelf tile to swap in, or tap an open corner to build."}
      </p>
    </aside>
  );
}

export function Overlay({
  children,
  title,
  onClose,
  className="",
  scrollKey,
}: {
  children: React.ReactNode;
  title: string;
  onClose: () => void;
  className?: string;
  scrollKey?: string;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    ref.current?.showModal();
  }, []);
  useLayoutEffect(() => {
    if (ref.current) ref.current.scrollTop=0;
  }, [title,scrollKey]);
  return (
    <dialog
      className={`journey-paper island-dialog ${className}`}
      ref={ref}
      aria-label={title}
      onCancel={onClose}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <button
        className="dialog-close"
        aria-label="Close panel"
        onClick={onClose}
      >
        <X size={22} />
      </button>
      {children}
    </dialog>
  );
}
