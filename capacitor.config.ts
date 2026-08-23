import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.nextstepuni.app',
  appName: 'NextStepUni',
  webDir: 'dist',
  experimental: {
    ios: {
      spm: {
        packageOptions: {
          // Avoid the Firebase SwiftPM identity collision documented by the
          // Capacitor Firebase plugin. Requires Capacitor CLI 8.4+.
          '@capacitor-firebase/app-check': { symlink: true },
        },
      },
    },
  },
};

export default config;
