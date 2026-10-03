import api from "../api/axios";

export const addPatient = async (data) => {
  const response = await api.post("/patients/", data);
  return response.data;
};

export const getPatient = async (patientId) => {
  const response = await api.get(`/patients/${encodeURIComponent(patientId)}`);
  return response.data;
};

export const getAllPatients = async () => {
  const response = await api.get("/patients/all");
  return response.data;
};

export const deletePatient = async (patientId) => {
  const response = await api.delete(
    `/patients/${encodeURIComponent(patientId)}`,
  );
  return response.data;
};
