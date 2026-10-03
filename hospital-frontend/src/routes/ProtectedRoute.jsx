import { Navigate, useLocation } from "react-router-dom";
import { getAccessToken } from "../utils/token";

export default function ProtectedRoute({ children, allowedRoles = [] }) {
  const location = useLocation();

  // ==========================================================
  // Check Login
  // ==========================================================

  const token = getAccessToken();

  if (!token) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  // ==========================================================
  // Get Logged-in User
  // ==========================================================

  const storedUser = localStorage.getItem("user");

  let user = null;

  try {
    user = storedUser ? JSON.parse(storedUser) : null;
  } catch (error) {
    console.error("Failed to parse logged-in user:", error);

    localStorage.removeItem("user");
  }

  // ==========================================================
  // User information not available
  // ==========================================================

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  // ==========================================================
  // Role Check
  // ==========================================================

  const userRole = user.role?.toLowerCase();

  // No roles specified means:
  // any authenticated user can access the page.
  if (allowedRoles.length === 0) {
    return children;
  }

  const normalizedAllowedRoles = allowedRoles.map((role) => role.toLowerCase());

  // ==========================================================
  // Unauthorized
  // ==========================================================

  if (!normalizedAllowedRoles.includes(userRole)) {
    return <Navigate to="/unauthorized" replace />;
  }

  // ==========================================================
  // Authorized
  // ==========================================================

  return children;
}
