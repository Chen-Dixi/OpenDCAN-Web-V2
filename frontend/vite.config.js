import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  css: { 
    preprocessorOptions: { 
      scss: { charset: false },
      sass: { charset: false },
    },
    postcss: {
      plugins: [
          {
              postcssPlugin: 'internal:charset-removal',
              AtRule: {
                  charset: (atRule) => {
                      if (atRule.name === 'charset') {
                          atRule.remove();
                      }
                  }
              }
          }
      ],
    },
  },
  plugins: [
    vue()
  ],
})
