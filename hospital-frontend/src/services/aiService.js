import api from "../api/axios";

/**
 * ============================================
 * AI Hospital Assistant Service
 * ============================================
 */

const aiService = {
  // ============================================
  // Chat
  // ============================================

  chat: async ({ query, practitioner_id, thread_id = null }) => {
    const response = await api.post("/ai/chat", {
      query,
      practitioner_id,
      thread_id,
    });

    return response.data;
  },

  // ============================================
  // Resume Patient Selection
  // ============================================

  resolvePatient: async ({ thread_id, selected_patient_id }) => {
    const response = await api.post("/ai/admission/resolvePatient", {
      thread_id,
      selected_patient_id,
    });

    return response.data;
  },

  // ============================================
  // Resume Bed Selection
  // ============================================

  selectBed: async ({
    thread_id,
    action,
    selected_bed = null,
    bed_id = null,
    reason = null,
  }) => {
    const response = await api.post("/ai/admission/bed-selection", {
      thread_id,
      action,
      selected_bed,
      bed_id,
      reason,
    });

    return response.data;
  },

  confirmAppointment: async ({ thread_id, confirmed }) => {
    const response = await api.post("/ai/appointment/confirm", {
      thread_id,
      confirmed,
    });

    return response.data;
  },

  // ============================================
  // New Chat
  // ============================================

  newChat: () => ({
    thread_id: null,
    messages: [],
  }),
};

export default aiService;
