import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.aiplayers.drama',
  appName: 'AI互动短剧',
  webDir: 'dist/build/app',
  server: {
    androidScheme: 'https'
  }
};

export default config;
