// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react-swc'
// import tailwindcss from '@tailwindcss/vite'

// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [react(), tailwindcss()],
// })
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/widget.jsx'), // ✅ correct entry
      name: 'ChatbotWidget',
      fileName: () => 'widget.js',
      formats: ['iife'] // ✅ for <script src="...">
    },
    rollupOptions: {
      external: [], // ✅ include React inside
    }
  }
});


