import { bestResult, resultsFor, shareText, type Game } from "./game";
import type { CertleQuestion } from "./data";

export const PUBLIC_CERTLE_URL = "https://nextstepuni.com/certle";
export type SharePlatform = "Facebook" | "LinkedIn" | "X" | "WhatsApp";

/** Never put the question, answer or scheme in a public share URL. */
export function socialShareUrl(platform: SharePlatform, text: string): string {
  switch (platform) {
    case "Facebook":
      return `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(PUBLIC_CERTLE_URL)}`;
    case "LinkedIn":
      return `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(PUBLIC_CERTLE_URL)}`;
    case "X":
      return `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
    case "WhatsApp":
      return `https://wa.me/?text=${encodeURIComponent(text)}`;
  }
}

export function resultShareData(
  n: number,
  game: Game,
  question: CertleQuestion,
) {
  if (!game.finished)
    throw new Error("Finish the question before sharing a result.");
  const results = resultsFor(game, question);
  const best = bestResult(results);
  const total = question.points.reduce((sum, point) => sum + point.marks, 0);
  return {
    number: n,
    day: game.day,
    subject: question.subject,
    earned: best?.earned ?? 0,
    total,
    attempts: game.answers.length,
    rows: results.map((result) =>
      result.hits.flatMap((hit) =>
        Array.from({ length: hit.marks }, () => hit.matched),
      ),
    ),
    text: shareText(n, game, question, "https://nextstepuni.com"),
  };
}
export type ResultShareData = ReturnType<typeof resultShareData>;

/** A real image attachment for phone share sheets, Stories and social uploads.
 * This draws only the public score payload, never the player's response. */
export async function createResultImage(data: ResultShareData): Promise<File> {
  await Promise.race([
    document.fonts.ready,
    new Promise<void>((resolve) => window.setTimeout(resolve, 2000)),
  ]);
  const canvas = document.createElement("canvas");
  canvas.width = 1080;
  canvas.height = 1080;
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("Image export is unavailable.");
  const ink = "#1a1a1a",
    orange = "#f26b1f";
  ctx.fillStyle = orange;
  ctx.fillRect(0, 0, 1080, 1080);
  ctx.fillStyle = "#fff";
  ctx.fillRect(40, 40, 1000, 1000);
  ctx.fillStyle = ink;
  ctx.fillRect(40, 40, 1000, 13);
  ctx.fillStyle = ink;
  ctx.font = '600 24px "DM Sans", sans-serif';
  ctx.fillText(
    `DAILY CHALLENGE / No. ${String(data.number).padStart(3, "0")}`,
    90,
    108,
  );
  ctx.textAlign = "right";
  ctx.fillText(data.day, 990, 108);
  ctx.textAlign = "left";
  const tile = 83,
    gap = 10,
    logoLeft = (1080 - 6 * tile - 5 * gap) / 2;
  for (let i = 0; i < 6; i++) {
    const left = logoLeft + i * (tile + gap);
    ctx.fillStyle = ink;
    ctx.beginPath();
    ctx.roundRect(left, 152, tile, 92, 10);
    ctx.fill();
    ctx.fillStyle = i === 0 || i === 3 ? orange : i === 2 ? "#fff" : ink;
    ctx.beginPath();
    ctx.roundRect(left, 148, tile, 90, 10);
    ctx.fill();
    ctx.strokeStyle = ink;
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.fillStyle = i === 0 || i === 2 || i === 3 ? ink : "#fff";
    ctx.font = '750 58px "DM Sans", sans-serif';
    ctx.textAlign = "center";
    ctx.fillText("CERTLE"[i], left + tile / 2, 213);
  }
  ctx.fillStyle = ink;
  ctx.font = '500 29px "DM Sans", sans-serif';
  ctx.fillText(data.subject, 540, 304);
  ctx.font = '750 180px "DM Sans", sans-serif';
  ctx.fillText(`${data.earned}/${data.total}`, 540, 497);
  ctx.font = '500 30px "DM Sans", sans-serif';
  ctx.fillText(`marks · ${data.attempts} of 3 attempts`, 540, 551);
  const size = Math.min(52, (810 - (data.total - 1) * 8) / data.total);
  const boardLeft = (1080 - data.total * size - (data.total - 1) * 8) / 2;
  data.rows.forEach((row, i) =>
    row.forEach((hit, j) => {
      ctx.fillStyle = hit ? orange : "#fff";
      ctx.strokeStyle = ink;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(boardLeft + j * (size + 8), 601 + i * 65, size, size, 5);
      ctx.fill();
      ctx.stroke();
    }),
  );
  // Use the actual brand character; a failed image does not prevent score export.
  try {
    const mascot = await new Promise<HTMLImageElement>((resolve, reject) => {
      const img = new Image();
      const timeout = window.setTimeout(
        () => reject(new Error("Character image unavailable")),
        3000,
      );
      img.onload = () => {
        window.clearTimeout(timeout);
        resolve(img);
      };
      img.onerror = () => {
        window.clearTimeout(timeout);
        reject(new Error("Character image unavailable"));
      };
      img.src = "/assets/landing/starguy-512.png";
    });
    ctx.drawImage(mascot, 840, 810, 100, 116);
  } catch {
    /* the score card remains complete without the decoration */
  }
  ctx.fillStyle = ink;
  ctx.textAlign = "left";
  ctx.font = '650 35px "DM Sans", sans-serif';
  ctx.fillText("Your turn.", 90, 864);
  ctx.font = '400 25px "DM Sans", sans-serif';
  ctx.fillText("Same question. See how you do.", 90, 903);
  ctx.beginPath();
  ctx.moveTo(90, 947);
  ctx.lineTo(990, 947);
  ctx.lineWidth = 1;
  ctx.stroke();
  ctx.font = '700 25px "DM Sans", sans-serif';
  ctx.fillText("nextstepuni", 90, 992);
  ctx.font = '400 23px "DM Sans", sans-serif';
  ctx.textAlign = "right";
  ctx.fillText("nextstepuni.com/certle", 990, 992);
  const blob = await new Promise<Blob>((resolve, reject) =>
    canvas.toBlob(
      (value) =>
        value ? resolve(value) : reject(new Error("Image export failed.")),
      "image/png",
    ),
  );
  return new File([blob], `certle-${data.day}.png`, { type: "image/png" });
}
