import React, { useEffect, useMemo, useRef, useState } from "react";
import type { StudioPiece } from "./studioModel";
import { centre } from "./geometry";
import { coastalMap } from "./collection";
import { exploredCells } from "./model";
import { paintedById, type PaintedStyle } from "./paintedDirections";

const images = new Map<string, Promise<HTMLImageElement>>();
function loadImage(src: string) {
  let result = images.get(src);
  if (!result) {
    result = new Promise<HTMLImageElement>((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = () => {
        images.delete(src);
        reject(new Error(`Could not load ${src}`));
      };
      img.src = src;
    });
    images.set(src, result);
  }
  return result;
}
type View = { x: number; y: number; width: number; height: number };
type Cell = { key: string; x: number; y: number };

const paperStamps = new WeakMap<HTMLImageElement, HTMLCanvasElement>();
/** Overlap softly faded paper edges without reflecting the drawn geography. */
function paperStamp(img: HTMLImageElement) {
  const existing = paperStamps.get(img);
  if (existing) return existing;
  const stamp = document.createElement("canvas");
  stamp.width = img.naturalWidth;
  stamp.height = img.naturalHeight;
  const ctx = stamp.getContext("2d")!,
    w = stamp.width,
    h = stamp.height;
  ctx.drawImage(img, 0, 0);
  ctx.globalCompositeOperation = "destination-in";
  for (const [x1, y1, x2, y2] of [
    [0, 0, w, 0],
    [0, 0, 0, h],
  ]) {
    const gradient = ctx.createLinearGradient(x1, y1, x2, y2);
    gradient.addColorStop(0, "#0000");
    gradient.addColorStop(0.045, "#000");
    gradient.addColorStop(0.955, "#000");
    gradient.addColorStop(1, "#0000");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, w, h);
  }
  paperStamps.set(img, stamp);
  return stamp;
}
function tilePaper(
  ctx: CanvasRenderingContext2D,
  img: HTMLImageElement,
  view: View,
  base: string,
) {
  const stamp = paperStamp(img),
    w = 2140,
    h = (w * img.naturalHeight) / img.naturalWidth,
    sx = w * 0.91,
    sy = h * 0.91,
    ox = -w / 2,
    oy = -75 - h / 2;
  ctx.fillStyle = base;
  ctx.fillRect(view.x, view.y, view.width, view.height);
  for (
    let row = Math.floor((view.y - oy - h) / sy);
    row <= Math.floor((view.y + view.height - oy) / sy);
    row++
  )
    for (
      let col = Math.floor((view.x - ox - w) / sx);
      col <= Math.floor((view.x + view.width - ox) / sx);
      col++
    ) {
      ctx.drawImage(stamp, ox + col * sx, oy + row * sy, w, h);
    }
}

/** A raster alpha field joins explored cells into a single irregular reveal. */
function clearingMask(
  width: number,
  height: number,
  view: View,
  cells: Cell[],
  feather: number,
) {
  const mask = document.createElement("canvas");
  mask.width = Math.max(1, Math.ceil(width / 2));
  mask.height = Math.max(1, Math.ceil(height / 2));
  const ctx = mask.getContext("2d")!,
    rx = 150,
    ry = 121;
  ctx.fillStyle = "#fff";
  ctx.fillRect(0, 0, mask.width, mask.height);
  ctx.globalCompositeOperation = "destination-out";
  const sx = mask.width / view.width,
    sy = mask.height / view.height;
  for (const cell of cells) {
    if (
      cell.x < view.x - rx ||
      cell.x > view.x + view.width + rx ||
      cell.y < view.y - ry ||
      cell.y > view.y + view.height + ry
    )
      continue;
    ctx.save();
    ctx.translate((cell.x - view.x) * sx, (cell.y - view.y) * sy);
    ctx.scale(rx * sx, ry * sy);
    const gradient = ctx.createRadialGradient(0, 0, 1 - feather, 0, 0, 1);
    gradient.addColorStop(0, "#000");
    gradient.addColorStop(1, "#0000");
    ctx.fillStyle = gradient;
    ctx.fillRect(-1, -1, 2, 2);
    ctx.restore();
  }
  return mask;
}

export function PaintedWorld({
  placed,
  style,
  view,
}: {
  placed: StudioPiece[];
  style: PaintedStyle;
  view: View;
}) {
  const ref = useRef<HTMLCanvasElement>(null),
    [size, setSize] = useState({ width: 0, height: 0 }),
    [failure, setFailure] = useState(false);
  const previous = useRef<Cell[]>([]),
    cells = useMemo(
      () =>
        exploredCells(placed).map((c) => ({ key: c.key, ...centre(c.q, c.r) })),
      [placed],
    );
  const treatment = paintedById[style];
  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    let timer: ReturnType<typeof setTimeout>;
    const observer = new ResizeObserver(([entry]) => {
      clearTimeout(timer);
      const next = {
        width: Math.round(entry.contentRect.width),
        height: Math.round(entry.contentRect.height),
      };
      timer = setTimeout(() => setSize(next), 100);
    });
    observer.observe(canvas);
    return () => {
      clearTimeout(timer);
      observer.disconnect();
    };
  }, []);
  useEffect(() => {
    const canvas = ref.current;
    if (!canvas || !size.width || !size.height) return;
    let disposed = false,
      animation = 0;
    const before = previous.current,
      added = cells.length > before.length && before.length > 0;
    previous.current = cells;
    const ratio = Math.min(window.devicePixelRatio || 1, 1.5),
      w = Math.round(size.width * ratio),
      h = Math.round(size.height * ratio);
    canvas.width = w;
    canvas.height = h;
    const zoom = Math.max(w / view.width, h / view.height),
      visible = {
        x: view.x + (view.width - w / zoom) / 2,
        y: view.y + (view.height - h / zoom) / 2,
        width: w / zoom,
        height: h / zoom,
      };
    const ctx = canvas.getContext("2d")!;
    ctx.fillStyle = treatment.base;
    ctx.fillRect(0, 0, w, h);
    const mask = clearingMask(w, h, visible, cells, treatment.feather);
    const oldMask = added
      ? clearingMask(w, h, visible, before, treatment.feather)
      : null;
    const sea = document.createElement("canvas"),
      cover = document.createElement("canvas"),
      veil = document.createElement("canvas");
    for (const c of [sea, cover, veil]) {
      c.width = w;
      c.height = h;
    }
    const seaCtx = sea.getContext("2d")!,
      coverCtx = cover.getContext("2d")!,
      veilCtx = veil.getContext("2d")!;
    const worldTransform = (context: CanvasRenderingContext2D) =>
      context.setTransform(
        zoom,
        0,
        0,
        zoom,
        -visible.x * zoom,
        -visible.y * zoom,
      );
    Promise.all([loadImage(coastalMap), loadImage(treatment.src)])
      .then(([water, art]) => {
        if (disposed) return;
        setFailure(false);
        worldTransform(seaCtx);
        const step = 950;
        for (
          let y = Math.floor(visible.y / step) * step;
          y < visible.y + visible.height;
          y += step
        )
          for (
            let x = Math.floor(visible.x / step) * step;
            x < visible.x + visible.width;
            x += step
          )
            seaCtx.drawImage(water, 500, 230, 510, 510, x, y, step, step);
        if ("paperRepeat" in treatment) {
          seaCtx.fillStyle = "#cee5e9";
          seaCtx.globalAlpha = 0.25;
          seaCtx.fillRect(visible.x, visible.y, visible.width, visible.height);
          seaCtx.globalAlpha = 1;
        }
        worldTransform(coverCtx);
        tilePaper(coverCtx, art, visible, treatment.base);
        const duration =
            added && !matchMedia("(prefers-reduced-motion: reduce)").matches
              ? 700
              : 0,
          start = performance.now();
        const draw = (now: number) => {
          if (disposed) return;
          const progress = duration ? Math.min(1, (now - start) / duration) : 1;
          veilCtx.globalCompositeOperation = "source-over";
          veilCtx.clearRect(0, 0, w, h);
          veilCtx.drawImage(cover, 0, 0);
          veilCtx.globalCompositeOperation = "destination-in";
          veilCtx.drawImage(mask, 0, 0, w, h);
          ctx.globalAlpha = 1;
          ctx.drawImage(sea, 0, 0);
          ctx.drawImage(veil, 0, 0);
          if (oldMask && progress < 1) {
            veilCtx.globalCompositeOperation = "source-over";
            veilCtx.clearRect(0, 0, w, h);
            veilCtx.drawImage(cover, 0, 0);
            veilCtx.globalCompositeOperation = "destination-in";
            veilCtx.drawImage(oldMask, 0, 0, w, h);
            ctx.globalAlpha = 1 - progress * progress * (3 - 2 * progress);
            ctx.drawImage(veil, 0, 0);
            ctx.globalAlpha = 1;
            animation = requestAnimationFrame(draw);
          }
        };
        draw(performance.now());
      })
      .catch(() => {
        if (!disposed) setFailure(true);
      });
    return () => {
      disposed = true;
      cancelAnimationFrame(animation);
    };
  }, [
    cells,
    style,
    size.width,
    size.height,
    view.x,
    view.y,
    view.width,
    view.height,
    treatment,
  ]);
  return (
    <>
      <canvas
        ref={ref}
        className="painted-world"
        aria-hidden="true"
        data-painted-world={style}
        data-explored-count={cells.length}
      />
      {failure && (
        <div className="painted-load-error" role="status">
          The artwork could not load. Please refresh to try again.
        </div>
      )}
    </>
  );
}
