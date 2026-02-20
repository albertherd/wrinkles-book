import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        artist: resolve(__dirname, 'paul-caruana.html')
      }
    }
  }
});
