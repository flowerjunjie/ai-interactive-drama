<script setup lang="ts">
import { onLaunch } from '@dcloudio/uni-app'

onLaunch(() => {
  // MVP：不做强制登录
})
</script>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

page,
body {
  height: 100%;
  font-family:
    Outfit,
    system-ui,
    -apple-system,
    sans-serif;
  color: #e8eaef;
  background-color: #050608;
  background-image:
    radial-gradient(ellipse 100% 55% at 50% -18%, rgba(212, 168, 83, 0.14), transparent 52%),
    radial-gradient(ellipse 70% 45% at 100% 40%, rgba(90, 76, 140, 0.06), transparent 45%),
    linear-gradient(180deg, #080a10 0%, #050608 38%, #050608 100%);
  background-attachment: fixed;
}
</style>
