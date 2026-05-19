import type { Config } from "tailwindcss";
import { getIconCollections, iconsPlugin } from "@egoist/tailwindcss-icons";
import cssMacro from "weapp-tailwindcss/css-macro";
import { isMp } from "./platform";

export default <Config>{
  content: ["./index.html", "./src/**/*.{html,js,ts,jsx,tsx,vue}"],
  theme: {
    extend: {
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'ui-serif', 'serif'],
        sans: ['Outfit', 'system-ui', 'sans-serif'],
      },
      colors: {
        drama: {
          950: '#050608',
          900: '#0a0c12',
          850: '#12151f',
          800: '#1a1e2a',
          accent: '#d4a853',
          'accent-soft': 'rgba(212, 168, 83, 0.14)',
          muted: '#8b93a7',
        },
      },
      boxShadow: {
        drama: '0 22px 44px -14px rgba(0, 0, 0, 0.75)',
        glow: '0 0 42px -8px rgba(212, 168, 83, 0.35)',
      },
      // colors: {
      // // 你可以在这里进行颜色的扩展
      // primary: {
      //   'DEFAULT': 'var(--color-primary, #0089FF)',
      //   'light-3': 'var(--color-primary-light-3, rgb(85, 199, 255))',
      //   'light-5': 'var(--color-primary-light-5, rgb(130, 217, 255))',
      //   'light-7': 'var(--color-primary-light-7, rgb(175, 235, 255))',
      //   'light-9': 'var(--color-primary-light-9, rgb(219, 252, 255))',
      //   'dark-2': 'var(--color-primary-dark-2, rgb(0, 135, 204))',
      // },
      // },
    },
  },
  // https://tw.icebreaker.top/docs/quick-start/uni-app-css-macro
  plugins: [
    cssMacro({
      variantsMap: {
        wx: "MP-WEIXIN",
        "-wx": {
          value: "MP-WEIXIN",
          negative: true,
        },
        // 定义多个条件判断
        // mv: {
        //   value: 'H5 || MP-WEIXIN'
        // },
        // '-mv': {
        //   value: 'H5 || MP-WEIXIN',
        //   negative: true
        // }
      },
    }),
    iconsPlugin({
      // 在这里可以选择你要使用的 icon, 更多详见:
      // https://icon-sets.iconify.design/
      collections: getIconCollections(["svg-spinners", "mdi"]),
    }),
  ],
  corePlugins: {
    // 小程序去使用 h5 的 preflight 和响应式 container 没有意义
    preflight: !isMp,
    container: !isMp,
  },
};
