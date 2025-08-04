// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react-swc'
// import tailwindcss from '@tailwindcss/vite'

// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [react(), tailwindcss()],
// })
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

// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    outDir: 'dist',
    lib: {
      entry: './src/main.jsx',
      name: 'ChatbotWidget',
      fileName: 'chatbot-widget', // Generates chatbot-widget.js
      formats: ['iife']
    },
    rollupOptions: {
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM'
        },
        // Ensures consistent filenames
        entryFileNames: 'chatbot-widget.js',
        assetFileNames: 'chatbot-widget.[ext]'
      }
    }
  }
});



