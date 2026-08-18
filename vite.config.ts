import path from 'path';
import type { IncomingMessage, ServerResponse } from 'http';
import { defineConfig, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import {
  PRIVACY_NOTICE,
  TERMS_OF_USE,
  LEGAL_TITLES,
  PRIVACY_POLICY_VERSION,
  LEGAL_LAST_UPDATED,
  SUPPORT_EMAIL,
  LEGAL_URL_RE,
  type LegalDoc,
  type Section,
} from './components/legal/legalContent';

// ── Public legal pages ──────────────────────────────────────────────────────
// Emit /privacy.html + /terms.html from the SAME source the in-app modal uses
// (components/legal/legalContent.ts), so the published policy can never drift
// from what students accept in-app. Apple App Review requires a publicly
// reachable privacy-policy URL — Firebase Hosting serves these straight from
// dist (canonical URL: <your-domain>/privacy.html).
const escHtml = (s: string) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Escape first, then turn bare source URLs into anchors. Order matters: doing
 *  it the other way round would escape the markup we just generated. */
const escHtmlLinked = (s: string) => {
  LEGAL_URL_RE.lastIndex = 0;
  return escHtml(s).replace(
    LEGAL_URL_RE,
    (url) => `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`,
  );
};

function renderSections(sections: Section[]): string {
  return sections
    .map((section) => {
      const parts: string[] = [];
      let bullets: string[] = [];
      const flush = () => {
        if (bullets.length) {
          parts.push(
            `<ul>${bullets.map((b) => `<li>${escHtmlLinked(b.replace(/^•\s*/, ''))}</li>`).join('')}</ul>`,
          );
          bullets = [];
        }
      };
      for (const line of section.body) {
        if (line.startsWith('• ')) bullets.push(line);
        else {
          flush();
          parts.push(`<p>${escHtmlLinked(line)}</p>`);
        }
      }
      flush();
      return `<section><h2>${escHtml(section.heading)}</h2>${parts.join('')}</section>`;
    })
    .join('\n');
}

function renderLegalPage(doc: LegalDoc): string {
  const title = LEGAL_TITLES[doc];
  const sections = doc === 'privacy' ? PRIVACY_NOTICE : TERMS_OF_USE;
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="index, follow" />
<title>${escHtml(title)} · NextStepUni</title>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body { margin: 0; background: #FAFBF6; color: #1a1a1a; line-height: 1.6;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    -webkit-font-smoothing: antialiased; }
  main { max-width: 720px; margin: 0 auto; padding: 48px 22px 80px; }
  .brand { font-size: 11px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: #7a7068; margin: 0 0 14px; }
  h1 { font-family: Georgia, "Source Serif 4", serif; font-size: 30px; font-weight: 600; margin: 0 0 6px; letter-spacing: -0.01em; }
  .meta { color: #9e9186; font-size: 13px; margin: 0 0 36px; }
  h2 { font-family: Georgia, "Source Serif 4", serif; font-size: 19px; font-weight: 600; margin: 32px 0 8px; }
  p, li { color: #3a3530; font-size: 15px; }
  p { margin: 0 0 10px; }
  ul { margin: 0 0 10px; padding-left: 20px; }
  li { margin: 0 0 6px; }
  a { color: #F26B1F; }
  footer { margin-top: 48px; padding-top: 22px; border-top: 1px solid #e5e2dd; color: #7a7068; font-size: 13px; }
  footer p { color: #7a7068; font-size: 13px; margin: 0 0 6px; }
</style>
</head>
<body>
<main>
  <p class="brand">NextStepUni</p>
  <h1>${escHtml(title)}</h1>
  <p class="meta">Version ${escHtml(PRIVACY_POLICY_VERSION)} · Last updated ${escHtml(LEGAL_LAST_UPDATED)}</p>
  ${renderSections(sections)}
  <footer>
    <p>Questions? Contact <a href="mailto:${escHtml(SUPPORT_EMAIL)}">${escHtml(SUPPORT_EMAIL)}</a>.</p>
    <p>NextStepUni Ltd</p>
    <p><a href="/privacy.html">Privacy Notice</a> &middot; <a href="/terms.html">Terms of Use</a></p>
  </footer>
</main>
</body>
</html>`;
}

function legalStaticPages(): Plugin {
  const routes: Record<string, LegalDoc> = {
    '/privacy.html': 'privacy',
    '/privacy': 'privacy',
    '/terms.html': 'terms',
    '/terms': 'terms',
  };
  return {
    name: 'legal-static-pages',
    configureServer(server) {
      server.middlewares.use((req: IncomingMessage, res: ServerResponse, next: () => void) => {
        const url = (req.url || '').split('?')[0];
        const doc = routes[url];
        if (!doc) return next();
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.end(renderLegalPage(doc));
      });
    },
    generateBundle() {
      this.emitFile({ type: 'asset', fileName: 'privacy.html', source: renderLegalPage('privacy') });
      this.emitFile({ type: 'asset', fileName: 'terms.html', source: renderLegalPage('terms') });
    },
  };
}

export default defineConfig(() => {
    return {
      server: {
        port: 3000,
        host: '0.0.0.0',
      },
      plugins: [
        react(),
        legalStaticPages(),
        VitePWA({
          registerType: 'autoUpdate',
          // Don't auto-inject the SW registration. We register manually in
          // index.tsx, gated on !Capacitor.isNativePlatform(), so the service
          // worker never runs inside the native WebView where its
          // navigateFallback can serve a stale/white screen. (audit item 12)
          injectRegister: false,
          includeAssets: [
            'icons/north-star-favicon-32x32.png',
            'icons/north-star-apple-touch-icon.png',
            'icons/north-star-icon-192x192.png',
            'icons/north-star-icon-512x512.png',
            'fonts/*.otf',
          ],
          manifest: {
            name: 'Nextstep Learning Lab',
            short_name: 'Nextstep',
            description: 'Science-backed learning strategies for exam success',
            theme_color: '#131311',
            background_color: '#FAFBF6',
            display: 'standalone',
            icons: [
              { src: '/icons/north-star-icon-192x192.png', sizes: '192x192', type: 'image/png' },
              { src: '/icons/north-star-icon-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'any maskable' },
              { src: '/icons/north-star-apple-touch-icon.png', sizes: '180x180', type: 'image/png', purpose: 'any' },
            ],
          },
          workbox: {
        // pdf.js and Diagram Vault are lazy-tool-only: keep their large chunks
        // out of the SW precache so non-users never download them. The runtime
        // app-chunks rule still caches each chunk after a student opens the tool.
        globIgnores: ['**/pdf.worker*.js', '**/vendor-pdfjs*.js', '**/DiagramVault*.js'],
            maximumFileSizeToCacheInBytes: 3 * 1024 * 1024,
            navigateFallback: 'index.html',
            // Legal pages are real static files (privacy.html / terms.html) emitted
            // by legalStaticPages(). Keep them OUT of the SPA navigate-fallback so an
            // installed PWA serves the actual page (not the app shell) — the public
            // Privacy Policy URL Apple/users hit must resolve to the notice itself.
            navigateFallbackDenylist: [/\/privacy(\.html)?$/, /\/terms(\.html)?$/],
            runtimeCaching: [
              // Paper Trail answer sidecars — small per-paper coordinate JSON on
              // Firebase Storage. SWR: serve cache instantly, refetch in the
              // background so a re-generated map self-updates. Must precede the
              // PDF rule (both are firebasestorage.googleapis.com origins).
              {
                urlPattern: /^https:\/\/firebasestorage\.googleapis\.com\/.*answers.*\.json(\?|$)/i,
                handler: 'StaleWhileRevalidate',
                options: { cacheName: 'paper-trail-answers', expiration: { maxEntries: 200, maxAgeSeconds: 60 * 60 * 24 * 30 } },
              },
              // Paper Trail marking-scheme/paper PDFs on Firebase Storage.
              // CacheFirst + rangeRequests so pdf.js range reads (206) are served
              // from a full cached copy when offline. cacheableResponse statuses
              // [200] means ONLY a full-file GET (the explicit scheme prefetch the
              // viewer fires on "Answers") is ever stored — never a partial 206 —
              // so the offline copy is always complete. Capped + purgeOnQuotaError
              // because schemes are multi-MB and the device floor is cheap phones.
              {
                urlPattern: /^https:\/\/firebasestorage\.googleapis\.com\/.*\.pdf(\?|$)/i,
                handler: 'CacheFirst',
                options: {
                  cacheName: 'paper-trail-pdfs',
                  rangeRequests: true,
                  cacheableResponse: { statuses: [200] },
                  expiration: { maxEntries: 40, maxAgeSeconds: 60 * 60 * 24 * 30, purgeOnQuotaError: true },
                },
              },
              // App JS/CSS chunks — network first, fall back to cache
              {
                urlPattern: /\/assets\/.*\.(js|css)$/i,
                handler: 'NetworkFirst',
                options: { cacheName: 'app-chunks', expiration: { maxAgeSeconds: 60 * 60 * 24 * 7 } },
              },
              // Tool icons — small PNGs that get re-arted occasionally. Must come
              // BEFORE the broad CacheFirst rule below: CacheFirst pins the first
              // cached copy forever, so a re-deployed icon at the same URL never
              // updated. StaleWhileRevalidate serves cache instantly but refetches
              // in the background, so new icon art self-updates on the next load.
              {
                urlPattern: /\/assets\/tools\/.*\.png$/i,
                handler: 'StaleWhileRevalidate',
                options: { cacheName: 'tool-icons-v1', expiration: { maxEntries: 60, maxAgeSeconds: 60 * 60 * 24 * 30 } },
              },
              // Static assets and 3D models — cache first
              {
                urlPattern: /\/(assets|models)\/.*\.(glb|png|jpg|svg|webp|woff2?)$/i,
                handler: 'CacheFirst',
                options: { cacheName: 'app-assets', expiration: { maxAgeSeconds: 60 * 60 * 24 * 30 } },
              },
              // Google Fonts CSS — stale-while-revalidate
              {
                urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
                handler: 'StaleWhileRevalidate',
                options: { cacheName: 'google-fonts-css', expiration: { maxAgeSeconds: 60 * 60 * 24 * 365 } },
              },
              // Google Fonts files — cache first (immutable)
              {
                urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
                handler: 'CacheFirst',
                options: { cacheName: 'google-fonts-files', expiration: { maxAgeSeconds: 60 * 60 * 24 * 365 } },
              },
              // DiceBear avatars
              {
                urlPattern: /^https:\/\/api\.dicebear\.com\/.*/i,
                handler: 'CacheFirst',
                options: { cacheName: 'dicebear-avatars', expiration: { maxAgeSeconds: 60 * 60 * 24 * 30 } },
              },
            ],
          },
        }),
      ],
      build: {
        // The eager entry is ~470KB; the >500KB chunks (vendor-firebase, and
        // the lazy-only vendor-three / InnovationZone) are intentional, so
        // document the accepted ceiling rather than emit a warning. (item 18)
        chunkSizeWarningLimit: 1200,
        rollupOptions: {
          output: {
            // Function form (not the object/array form) so EVERY module id is
            // classified deterministically. Audit 2026-06-01: the old object
            // form folded React into vendor-three (because @react-three/fiber
            // depends on React), leaving vendor-react a 1-byte empty chunk and
            // forcing the entry to eagerly download the 1.1MB vendor-three
            // (and vendor-jspdf) at boot just to get React. Matching React
            // first keeps it in vendor-react; three/jspdf then stay in their
            // own chunks, reachable only via the lazy Journey / PDF routes.
            manualChunks(id) {
              // Vite's __vitePreload helper and Rollup's CJS interop helpers are
              // used by EVERY lazy import()/CJS dep in the eager entry. If they
              // land inside a heavy lazy vendor chunk (they were ending up in
              // vendor-jspdf), the entry statically imports that chunk and the
              // whole 422KB jspdf bundle loads at boot. Pin them to the
              // always-eager vendor-react chunk instead. (audit 2026-06-01)
              if (id.includes('vite/preload-helper') || id.includes('commonjsHelpers')) return 'vendor-react';
              if (!id.includes('node_modules')) return;
              // React core only (NOT react-reconciler — that's three-only and
              // should ride along in the lazy vendor-three graph).
              if (/node_modules\/(react|react-dom|scheduler)\//.test(id)) return 'vendor-react';
              if (/node_modules\/(firebase|@firebase)\//.test(id)) return 'vendor-firebase';
              if (id.includes('node_modules/framer-motion')) return 'vendor-framer';
              if (/node_modules\/(three|@react-three)\//.test(id)) return 'vendor-three';
              if (id.includes('node_modules/jspdf')) return 'vendor-jspdf';
              if (id.includes('node_modules/pdfjs-dist')) return 'vendor-pdfjs';
            },
          },
        },
      },
      resolve: {
        alias: {
          '@': path.resolve(__dirname, '.'),
        }
      }
    };
});
