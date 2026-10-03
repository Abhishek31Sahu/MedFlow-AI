import api from "../api/axios";

import {
  saveAccessToken,
  saveRefreshToken,
  removeTokens,
} from "../utils/token";

// ==============================
// Login
// ==============================

export async function login(data) {
  const response = await api.post("/auth/login", data);

  const loginData = response.data;

  // Save tokens
  saveAccessToken(loginData.tokens.access_token);

  saveRefreshToken(loginData.tokens.refresh_token);

  // Save logged-in user information
  localStorage.setItem("user", JSON.stringify(loginData.user));

  console.log("Logged-in user:", loginData.user);

  console.log("Role:", loginData.user?.role);

  console.log("Practitioner ID:", loginData.user?.practitioner_id);

  return loginData;
}

// ==============================
// Logout
// ==============================

export async function logout() {
  try {
    await api.post("/auth/logout");
  } finally {
    removeTokens();

    // Remove user information
    localStorage.removeItem("user");
  }
}

// ==============================
// Current Logged-in User
// ==============================

export async function getCurrentUser() {
  const response = await api.get("/auth/me");

  // Keep localStorage synchronized
  localStorage.setItem("user", JSON.stringify(response.data));

  return response.data;
}

// ==============================
// Refresh Token
// ==============================

export async function refreshToken(refreshToken) {
  const response = await api.post("/auth/refresh", {
    refresh_token: refreshToken,
  });

  saveAccessToken(response.data.access_token);

  return response.data;
}
