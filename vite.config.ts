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
            runtimeCaching: [
              {
                urlPattern: /^https:\/\/cdn\.tailwindcss\.com\/.*/i,
                handler: 'CacheFirst',
                options: { cacheName: 'tailwind-cdn', expiration: { maxAgeSeconds: 60 * 60 * 24 * 30 } },
              },
              {
                urlPattern: /^https:\/\/fonts\.(googleapis|gstatic)\.com\/.*/i,
                handler: 'CacheFirst',
                options: { cacheName: 'google-fonts', expiration: { maxAgeSeconds: 60 * 60 * 24 * 365 } },
              },
              {
                urlPattern: /^https:\/\/api\.dicebear\.com\/.*/i,
                handler: 'CacheFirst',
                options: { cacheName: 'dicebear-avatars', expiration: { maxAgeSeconds: 60 * 60 * 24 * 30 } },
              },
            ],
          },
        }),
      ],
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
