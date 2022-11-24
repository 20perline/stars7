import { fileURLToPath, URL } from "node:url";

import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";


// https://vitejs.dev/config/
export default ({ mode }) => {

  const env = loadEnv(mode, process.cwd());
  console.log(env)

  return defineConfig({
    plugins: [vue()],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    server: {
      host: env.VITE_HOST,
      proxy: {
        "/api": {
          target: env.VITE_API_HOST,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
  });
};
