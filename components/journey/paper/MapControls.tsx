import React, { useEffect, useRef, useState } from "react";
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
export const defaultCamera = { x: 0, y: -75, zoom: 1 };
export type Camera = typeof defaultCamera;
const bound = (camera: Camera): Camera => ({
  x: Number.isFinite(camera.x) ? camera.x : 0,
  y: Number.isFinite(camera.y) ? camera.y : 0,
  zoom: Math.max(0.8, Math.min(1.8, camera.zoom)),
});
export function IslandMap({
  world,
  building,
  chosen,
  candidate,
  onCandidate,
  onInspect,
  onDiscover,
  onTreasure,
  camera,
  setCamera,
}: {
  world: IslandState;
  building: boolean;
  chosen: TileKind;
  candidate: string | null;
  onCandidate: (key: string) => void;
  onInspect: (kind: TileKind) => void;
  onDiscover: (id: LegendId) => void;
  onTreasure: (id: string) => void;
  camera: Camera;
  setCamera: React.Dispatch<React.SetStateAction<Camera>>;
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
  const drag = useRef<{
      x: number;
      y: number;
      px: number;
      py: number;
      scale: number;
    } | null>(null),
    slots = frontier(world.placed),
    preview = building ? slots.find((c) => c.key === candidate) : undefined,
    seen = visibleDiscoveries(world.placed),
    ghost = preview ? piece(preview.q, preview.r, chosen) : null;
  const view = {
    x: camera.x - 920 / renderZoom,
    y: renderY - 620 / renderZoom,
    width: 1840 / renderZoom,
    height: 1240 / renderZoom,
  };
  return (
    <div className="island-map-container">
      <PaintedWorld placed={world.placed} style="pencilatlas" view={view} />
      <svg
        className="student-map"
        viewBox={`${camera.x - 920 / renderZoom} ${renderY - 620 / renderZoom} ${1840 / renderZoom} ${1240 / renderZoom}`}
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
            scale: Math.min(
              1840 / renderZoom / rect.width,
              1240 / renderZoom / rect.height,
            ),
          };
          e.currentTarget.setPointerCapture(e.pointerId);
        }}
        onPointerMove={(e) => {
          const p = drag.current;
          if (p)
            setCamera((c) =>
              bound({
                ...c,
                x: p.px - (e.clientX - p.x) * p.scale,
                y: p.py - (e.clientY - p.y) * p.scale,
              }),
            );
        }}
        onPointerUp={() => (drag.current = null)}
        onPointerCancel={() => (drag.current = null)}
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
              aria-label={`Preview ${tileById[chosen].name} at open corner ${index + 1}`}
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
        </g>
        {[...world.placed, ...(ghost ? [ghost] : [])]
          .sort((a, b) => a.y - b.y || a.x - b.x)
          .map((cell) => (
            <g
              key={cell.key}
              data-island-tile={cell.key === ghost?.key ? undefined : cell.kind}
              data-cell={cell.key}
              data-ink-edge={cell.inkEdge.variant}
              pointerEvents={building ? "none" : undefined}
              opacity={cell.key === ghost?.key ? 0.68 : 1}
            >
              <Scenery kind={cell.kind} x={cell.x} y={cell.y} />
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
              aria-label={`Inspect ${tileById[cell.kind].name}`}
              onClick={() => {
                const cache = PAPER_LANDMARKS.find(
                  (d) =>
                    d.q === cell.q && d.r === cell.r && d.kind === "treasure",
                );
                if (cache) onTreasure(cache.id);
                else onInspect(cell.kind);
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  onInspect(cell.kind);
                }
              }}
            />
          ))}
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
      </svg>
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
  onChoose,
  balance,
  credits = 0,
  group,
  setGroup,
  orientation,
}: {
  chosen: TileKind;
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
    );
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
          {shelfGroups.map((name) => (
            <button
              key={name}
              aria-pressed={group === name}
              onClick={() => setGroup(name)}
            >
              {name}
            </button>
          ))}
        </nav>
        <span>{items.length} tiles</span>
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
              aria-pressed={chosen === t.id}
              onClick={() => onChoose(t.id)}
            >
              <ShelfPortrait kind={t.id} />
              <strong>{t.name}</strong>
              <span className={t.price > balance ? "over-budget" : ""}>
                {t.id === "meadow" && credits > 0
                  ? `${credits} earned tiles`
                  : `${t.price} JP`}
                {t.price > balance ? " · save a little more" : ""}
              </span>
            </button>
          );
        })}
      </div>
    </section>
  );
}

export function Placement({
  world,
  chosen,
  candidate,
  onPlace,
  onUndo,
  busy = false,
  full = false,
}: {
  world: IslandState;
  chosen: TileKind;
  candidate: string | null;
  onPlace: () => void;
  onUndo: () => void;
  busy?: boolean;
  full?: boolean;
}) {
  const item = tileById[chosen],
    t = {
      ...item,
      price: chosen === "meadow" && world.credits > 0 ? 0 : item.price,
    },
    canPay = world.balance >= t.price;
  return (
    <aside
      className={`placement-inspector ${full ? "full" : ""}`}
      aria-label="Your selected tile"
    >
      {full && <TilePortrait kind={chosen} />}
      <div className="placement-title">
        <h3>{t.name}</h3>
        <span>{t.price} JP</span>
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
              ? "Place this tile"
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
            ? `${world.balance - t.price} JP left after placing`
            : ""}
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

export function Overlay({
  children,
  title,
  onClose,
}: {
  children: React.ReactNode;
  title: string;
  onClose: () => void;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    ref.current?.showModal();
  }, []);
  return (
    <dialog
      className="journey-paper island-dialog"
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
