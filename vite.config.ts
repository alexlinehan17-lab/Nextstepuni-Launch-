import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig(() => {
    return {
      server: {
        port: 3000,
        host: '0.0.0.0',
      },
      plugins: [
        react(),
        VitePWA({
          registerType: 'autoUpdate',
          // Don't auto-inject the SW registration. We register manually in
          // index.tsx, gated on !Capacitor.isNativePlatform(), so the service
          // worker never runs inside the native WebView where its
          // navigateFallback can serve a stale/white screen. (audit item 12)
          injectRegister: false,
          includeAssets: ['icons/*.png', 'fonts/*.otf'],
          manifest: {
            name: 'Nextstep Learning Lab',
            short_name: 'Nextstep',
            description: 'Science-backed learning strategies for exam success',
            theme_color: '#131311',
            background_color: '#FAFBF6',
            display: 'standalone',
            icons: [
              { src: '/icons/icon-192x192.png', sizes: '192x192', type: 'image/png' },
              { src: '/icons/icon-512x512.png', sizes: '512x512', type: 'image/png' },
              { src: '/icons/apple-touch-icon.png', sizes: '180x180', type: 'image/png', purpose: 'any' },
            ],
          },
          workbox: {
        // pdf.js is Paper-Trail-only: keep its ~1.8MB (vendor chunk + worker)
        // out of the SW precache so non-users never download it.
        globIgnores: ['**/pdf.worker*.js', '**/vendor-pdfjs*.js'],
            maximumFileSizeToCacheInBytes: 3 * 1024 * 1024,
            navigateFallback: 'index.html',
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
