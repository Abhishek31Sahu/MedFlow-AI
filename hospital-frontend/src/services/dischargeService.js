import api from "../api/axios";

export const submitMedicationReview = async (data) => {
  const response = await api.post("/discharge/medication-review", data);

  return response.data;
};
