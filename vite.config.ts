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
            maximumFileSizeToCacheInBytes: 3 * 1024 * 1024,
            navigateFallback: 'index.html',
            runtimeCaching: [
              // App JS/CSS chunks — network first, fall back to cache
              {
                urlPattern: /\/assets\/.*\.(js|css)$/i,
                handler: 'NetworkFirst',
                options: { cacheName: 'app-chunks', expiration: { maxAgeSeconds: 60 * 60 * 24 * 7 } },
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
              // Tailwind CSS CDN — stale-while-revalidate for offline support
              {
                urlPattern: /^https:\/\/cdn\.tailwindcss\.com\/.*/i,
                handler: 'StaleWhileRevalidate',
                options: { cacheName: 'tailwind-cdn', expiration: { maxAgeSeconds: 60 * 60 * 24 * 30 } },
              },
            ],
          },
        }),
      ],
      build: {
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
