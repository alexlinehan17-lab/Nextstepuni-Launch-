import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.nextstepuni.app',
  appName: 'NextStepUni',
  webDir: 'dist',
  ios: {
    backgroundColor: '#FFFFFF',
    // The web app owns safe-area padding; native insets would apply it twice.
    contentInset: 'never',
  },
  plugins: {
    StatusBar: {
      overlaysWebView: true,
      style: 'LIGHT',
    },
  },
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
