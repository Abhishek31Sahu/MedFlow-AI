import api from "../api/axios";

// ==========================================
// Create User
// ==========================================
export async function createUser(data) {
  const response = await api.post("/users", data);
  return response.data;
}

// ==========================================
// Get All Users
// ==========================================
export async function getUsers() {
  const response = await api.get("/users");
  return response.data;
}

// ==========================================
// Get User By ID
// ==========================================
export async function getUser(userId) {
  const response = await api.get(`/users/${userId}`);
  return response.data;
}

// ==========================================
// Update User
// ==========================================
export async function updateUser(userId, data) {
  const response = await api.put(`/users/${userId}`, data);
  return response.data;
}

// ==========================================
// Delete User
// ==========================================
export async function deleteUser(userId) {
  const response = await api.delete(`/users/${userId}`);
  return response.data;
}

// ==========================================
// Change Password
// ==========================================
export async function changePassword(userId, newPassword) {
  const response = await api.patch(`/users/${userId}/password`, {
    new_password: newPassword,
  });

  return response.data;
}

// ==========================================
// Activate User
// ==========================================
export async function activateUser(userId) {
  const response = await api.patch(`/users/${userId}/activate`);

  return response.data;
}

// ==========================================
// Deactivate User
// ==========================================
export async function deactivateUser(userId) {
  const response = await api.patch(`/users/${userId}/deactivate`);

  return response.data;
}
