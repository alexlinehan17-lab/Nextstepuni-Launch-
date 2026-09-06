import React, { useEffect, useRef, useState } from 'react';
import type { PDFDocumentLoadingTask, RenderTask } from 'pdfjs-dist';
import { loadPdfjs } from './pdfjsLoader';

// Cache only small rendered covers, never keep a PDF worker document alive.
const covers = new Map<string, string>();

/** The actual first page of this paper. A failed preview never blocks opening. */
export default function PaperCover({ url, image = false }: { url: string; image?: boolean }) {
  const target = useRef<HTMLSpanElement>(null);
  const [cover, setCover] = useState<{ url: string; src: string } | null>(null);

  useEffect(() => {
    if (image || !target.current) return;
    let disposed = false;
    let task: PDFDocumentLoadingTask | undefined;
    let render: RenderTask | undefined;
    let timeout: number | undefined;
    const load = async () => {
      const cached = covers.get(url);
      if (cached) { setCover({ url, src: cached }); return; }
      try {
        const pdfjs = await loadPdfjs();
        if (disposed) return;
        // Use range requests and disable prefetch: a 50px cover should not
        // download a whole multi-megabyte paper on a student's mobile data.
        task = pdfjs.getDocument({ url, disableAutoFetch: true, disableStream: true });
        timeout = window.setTimeout(() => { void task?.destroy().catch(() => {}); }, 15000);
        const pdf = await task.promise;
        if (disposed) return;
        const page = await pdf.getPage(1);
        if (disposed) return;
        const viewport = page.getViewport({ scale: 100 / page.getViewport({ scale: 1 }).width });
        const canvas = document.createElement('canvas');
        canvas.width = Math.ceil(viewport.width);
        canvas.height = Math.ceil(viewport.height);
        render = page.render({ canvas, viewport });
        await render.promise;
        if (disposed) return;
        const src = canvas.toDataURL('image/png');
        if (covers.size >= 48) covers.delete(covers.keys().next().value!);
        covers.set(url, src);
        setCover({ url, src });
      } catch {
        // Keep the neutral PDF label if offline or the preview is unavailable.
      } finally {
        window.clearTimeout(timeout);
        await task?.destroy().catch(() => {});
      }
    };
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        observer.disconnect();
        void load();
      }
    });
    observer.observe(target.current);
    return () => {
      disposed = true;
      observer.disconnect();
      window.clearTimeout(timeout);
      render?.cancel();
      void task?.destroy().catch(() => {});
    };
  }, [url, image]);

  const src = image ? url : cover?.url === url ? cover.src : covers.get(url);
  return <span ref={target} className="pt-cover" aria-hidden="true">
    {src ? <img src={src} alt="" loading="lazy" /> : <span>PDF</span>}
  </span>;
}
