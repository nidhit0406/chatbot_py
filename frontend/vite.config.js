// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react-swc'
// import tailwindcss from '@tailwindcss/vite'

// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [react(), tailwindcss()],
// })

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import { resolve } from 'path';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    lib: {
      entry: resolve(__dirname, 'src/widget.jsx'),
      name: 'ChatbotWidget',
      fileName: () => 'widget-bundle.js',
      formats: ['iife'],
    },
    rollupOptions: {
      external: [],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
  },
  server: {
    port: 5173,
    open: true,
  },
  publicDir: 'public', // Ensures public/ is included in deployment
});

// vite.config.js
// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react-swc'
// import tailwindcss from '@tailwindcss/vite'
// import path from 'path'

// export default defineConfig({
//   plugins: [react(), tailwindcss()],
//   build: {
//     lib: {
//       entry: path.resolve(__dirname, 'widget.jsx'),
//       name: 'ChatbotWidget',
//       fileName: () => 'widget.js',
//       formats: ['iife'], // Needed for Shopify
//     },
//     rollupOptions: {
//       external: [],
//       output: {
//         globals: {
//           react: 'React',
//           'react-dom': 'ReactDOM'
//         }
//       }
//     }
//   }
// })



