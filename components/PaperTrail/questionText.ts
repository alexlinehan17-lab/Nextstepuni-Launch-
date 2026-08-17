import type { PDFDocumentProxy } from 'pdfjs-dist';
import type { PaperAnswerSeg } from '../../types/paperTrail';

interface TextSpan {
  text: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface ExtractedQuestionText {
  text: string;
  lines: string[];
  confidence: 'pdf-text' | 'image-only';
}

const apply = (matrix: number[], x: number, y: number): [number, number] => [
  matrix[0] * x + matrix[2] * y + matrix[4],
  matrix[1] * x + matrix[3] * y + matrix[5],
];

const joinLine = (spans: TextSpan[]): string => {
  const ordered = [...spans].sort((a, b) => a.x - b.x);
  let out = '';
  let right: number | null = null;
  for (const span of ordered) {
    const gap = right === null ? 0 : span.x - right;
    if (out && !out.endsWith(' ') && !span.text.startsWith(' ') && gap > span.height * 0.25) out += ' ';
    out += span.text;
    right = span.x + span.width;
  }
  return out.replace(/\s+/g, ' ').trim();
};

/**
 * Read only the searchable PDF text whose baselines fall inside a verified
 * question crop. This is not OCR and never rewrites the extracted wording.
 * Image-only papers return an honest empty result so the UI keeps the crop as
 * the source rather than guessing what it says.
 */
export async function extractQuestionText(
  pdf: PDFDocumentProxy,
  region: PaperAnswerSeg[],
): Promise<ExtractedQuestionText> {
  const lines: string[] = [];
  for (const segment of region) {
    const page = await pdf.getPage(segment.p);
    try {
      const viewport = page.getViewport({ scale: 1 });
      const width = viewport.width || 1;
      const height = viewport.height || 1;
      const rect = segment.r ?? [0, 0, 1, 1];
      const content = await page.getTextContent();
      const spans: TextSpan[] = [];
      for (const raw of content.items as unknown[]) {
        const item = raw as { str?: string; width?: number; height?: number; transform?: number[] };
        if (!item.str?.trim() || !item.transform) continue;
        const [x, baseline] = apply(viewport.transform, item.transform[4], item.transform[5]);
        const glyphHeight = Math.hypot(item.transform[1], item.transform[3]) || item.height || 10;
        const top = baseline - glyphHeight;
        const centreX = (x + (item.width ?? 0) / 2) / width;
        const centreY = (top + glyphHeight / 2) / height;
        if (centreX < rect[0] || centreX > rect[2] || centreY < rect[1] || centreY > rect[3]) continue;
        spans.push({ text: item.str, x, y: top, width: item.width ?? 0, height: glyphHeight });
      }
      spans.sort((a, b) => a.y - b.y || a.x - b.x);
      const groups: TextSpan[][] = [];
      for (const span of spans) {
        const last = groups[groups.length - 1];
        if (!last) {
          groups.push([span]);
          continue;
        }
        const baseline = last.reduce((sum, item) => sum + item.y, 0) / last.length;
        const tolerance = Math.max(3, span.height * 0.62);
        if (Math.abs(span.y - baseline) <= tolerance) last.push(span);
        else groups.push([span]);
      }
      for (const group of groups) {
        const line = joinLine(group);
        if (line) lines.push(line);
      }
    } finally {
      page.cleanup();
    }
  }
  const text = lines.join('\n').trim();
  return { text, lines, confidence: text.length >= 8 ? 'pdf-text' : 'image-only' };
}
