import axios from "axios";
import Constants from "expo-constants";

const API_BASE = Constants.expoConfig?.extra?.API_BASE_URL || "http://localhost:8000";
const axiosClient = axios.create({ baseURL: API_BASE, timeout: 10000 });

axiosClient.interceptors.request.use(
  config => { console.log("Request:", config.url); return config; },
  error => Promise.reject(error)
);

axiosClient.interceptors.response.use(
  response => response,
  error => { console.error("API Error:", error.response?.data || error.message); return Promise.reject(error); }
);

export default axiosClient;
