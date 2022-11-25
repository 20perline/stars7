import axios from "axios";

const env = import.meta.env;

const http = axios.create({
  //   baseURL: "/api",
  baseURL: env.VITE_API_HOST,
  withCredentials: true,
  timeout: 3000, // 超时时间
});

http.interceptors.request.use(
  function (config) {
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

http.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    return Promise.reject(error);
  }
);

export default http;
