import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    rollupOptions: {
      input: {
        main: './index.html', // Main app
        chatbot: './src/chatbot.js' // Script for Shopify
      },
      output: {
        entryFileNames: '[name].js', // Output chatbot.js
      }
    }
  }
})
