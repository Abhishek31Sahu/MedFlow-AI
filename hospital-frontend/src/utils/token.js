const ACCESS_TOKEN = "access_token";
const REFRESH_TOKEN = "refresh_token";

export function saveAccessToken(token) {
  localStorage.setItem(ACCESS_TOKEN, token);
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN);
}

export function saveRefreshToken(token) {
  localStorage.setItem(REFRESH_TOKEN, token);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN);
}

export function removeTokens() {
  localStorage.removeItem(ACCESS_TOKEN);
  localStorage.removeItem(REFRESH_TOKEN);
}
