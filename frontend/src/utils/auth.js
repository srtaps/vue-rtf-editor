import { jwtDecode } from "jwt-decode";

export function isTokenExpired() {
  const token = localStorage.getItem("access_token");

  if (!token) return true;

  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    return decoded.exp < currentTime;
  } catch (error) {
    return true;
  }
}
