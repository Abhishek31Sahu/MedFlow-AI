import api from "../api/axios";

/**
 * Bed Management Service
 */
const bedService = {
  // ============================================================
  // CRUD
  // ============================================================

  createBed: async (data) => {
    const response = await api.post("/beds", data);
    return response.data;
  },

  getBeds: async () => {
    const response = await api.get("/beds");
    return response.data;
  },

  getBed: async (bedId) => {
    const response = await api.get(`/beds/${bedId}`);
    return response.data;
  },

  updateBed: async (bedId, data) => {
    const response = await api.put(`/beds/${bedId}`, data);
    return response.data;
  },

  deleteBed: async (bedId) => {
    const response = await api.delete(`/beds/${bedId}`);
    return response.data;
  },

  // ============================================================
  // Recommendation
  // ============================================================

  recommendBeds: async (data) => {
    const response = await api.post("/beds/recommend", data);
    return response.data;
  },

  // ============================================================
  // Assignment
  // ============================================================

  assignBed: async (data) => {
    const response = await api.post("/beds/assign", data);
    return response.data;
  },

  // ============================================================
  // Transfer
  // ============================================================

  transferBed: async (data) => {
    const response = await api.post("/beds/transfer", data);
    return response.data;
  },

  // ============================================================
  // Release
  // ============================================================

  releaseBed: async (bedId) => {
    const response = await api.post(`/beds/${bedId}/release`);
    return response.data;
  },

  // ============================================================
  // Reservation
  // ============================================================

  reserveBed: async (bedId) => {
    const response = await api.post(`/beds/${bedId}/reserve`);
    return response.data;
  },

  cancelReservation: async (bedId) => {
    const response = await api.post(`/beds/${bedId}/cancel-reservation`);
    return response.data;
  },

  // ============================================================
  // Cleaning
  // ============================================================

  markCleaning: async (bedId) => {
    const response = await api.post(`/beds/${bedId}/cleaning`);
    return response.data;
  },

  markAvailable: async (bedId) => {
    const response = await api.post(`/beds/${bedId}/available`);
    return response.data;
  },

  // ============================================================
  // Dashboard
  // ============================================================

  getStatistics: async () => {
    const response = await api.get("/beds/dashboard/statistics");
    return response.data;
  },

  getAvailableBeds: async () => {
    const response = await api.get("/beds/dashboard/available");
    return response.data;
  },

  getOccupiedBeds: async () => {
    const response = await api.get("/beds/dashboard/occupied");
    return response.data;
  },
};

export default bedService;
