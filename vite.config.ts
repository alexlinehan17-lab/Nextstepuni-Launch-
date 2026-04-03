import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, '.', '');
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
            background_color: '#131311',
            display: 'standalone',
            icons: [
              { src: '/icons/icon-192x192.png', sizes: '192x192', type: 'image/png' },
              { src: '/icons/icon-512x512.png', sizes: '512x512', type: 'image/png' },
              { src: '/icons/apple-touch-icon.png', sizes: '180x180', type: 'image/png', purpose: 'apple touch icon' },
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
            ],
          },
        }),
      ],
      build: {
        rollupOptions: {
          output: {
            manualChunks: {
              'vendor-react': ['react', 'react-dom'],
              'vendor-firebase': ['firebase/app', 'firebase/auth', 'firebase/firestore'],
              'vendor-framer': ['framer-motion'],
              'vendor-three': ['three', '@react-three/fiber', '@react-three/drei'],
            },
          },
        },
      },
      define: {
        'process.env.API_KEY': JSON.stringify(env.GEMINI_API_KEY),
        'process.env.GEMINI_API_KEY': JSON.stringify(env.GEMINI_API_KEY)
      },
      resolve: {
        alias: {
          '@': path.resolve(__dirname, '.'),
        }
      }
    };
});
