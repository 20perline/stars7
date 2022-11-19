import axios from "axios";

const http = axios.create({
  baseURL: "/api",
  withCredentials: true,
  timeout: 3000, // 超时时间
});

http.interceptors.request.use(function (config) {
    return config;
}, function (error) {
    return Promise.reject(error);
});


http.interceptors.response.use(function (response) {
    console.log('response: ', response);
    return response;
}, function (error) {
    return Promise.reject(error);
});


export default http