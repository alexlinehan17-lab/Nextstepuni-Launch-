import { fixedInkEdge, type InkStamp } from "./inkVariants";
import { centre } from "./geometry";
import { tileGround, type TileKind } from "./catalogue";
import type { PaperVisitorId } from "../../../functions/src/paperVisitors";
export type StudioPiece = {
  key: string;
  q: number;
  r: number;
  kind: TileKind;
  x: number;
  y: number;
  inkEdge: InkStamp;
  groundColor: string;
  wonderId?: PaperVisitorId;
};
export function piece(
  q: number,
  r: number,
  kind: TileKind,
  inkEdge: InkStamp = fixedInkEdge(`${q},${r}`),
  wonderId?: PaperVisitorId,
): StudioPiece {
  return {
    inkEdge,
    groundColor: tileGround(kind),
    key: `${q},${r}`,
    q,
    r,
    kind,
    ...centre(q, r),
    ...(wonderId ? { wonderId } : {}),
  };
}
