import api from "../api/axios";

export const getAllActiveMedications = async () => {
  const response = await api.get("/medications/all");

  return response.data;
};
