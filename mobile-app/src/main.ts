import { createSSRApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import { initLicense } from './services/licenseService'

export function createApp() {
  const app = createSSRApp(App)
  const pinia = createPinia()
  app.use(pinia)
  app.config.globalProperties.$license = { init: initLicense }
  return { app }
}
