import axios from "axios";
import {
  getAccessToken,
  saveAccessToken,
  getRefreshToken,
} from "../utils/token";
const BASE_URL = import.meta.env.VITE_API_URL;
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 100000,
});

// Attach Access Token
api.interceptors.request.use((config) => {
  const token = getAccessToken();

  console.log("Access Token:", token);

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  console.log("Authorization Header:", config.headers.Authorization);

  return config;
});

// Refresh Token
api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    console.log("API Error:", error.response?.status);

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = getRefreshToken();

        console.log("Refresh Token:", refreshToken);

        const response = await axios.post(`${BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        console.log("Refresh Response:", response.data);

        saveAccessToken(response.data.access_token);

        console.log("New Access Token:", response.data.access_token);

        originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;

        return api(originalRequest);
      } catch (err) {
        console.error("Refresh Failed:", err.response?.data || err);

        localStorage.clear();
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  },
);

export default api;
