import api from "../api/axios";

// Get all templates
export const getTemplates = async () => {
  const response = await api.get("/laboratory/templates");
  return response.data;
};

// Get one template by test code
export const getTemplate = async (testCode) => {
  const response = await api.get(
    `/laboratory/templates/${encodeURIComponent(testCode)}`,
  );

  return response.data;
};

// Create template
export const createTemplate = async (data) => {
  const response = await api.post("/laboratory/templates", data);

  return response.data;
};

// Update template
export const updateTemplate = async (testCode, data) => {
  const response = await api.put(
    `/laboratory/templates/${encodeURIComponent(testCode)}`,
    data,
  );

  return response.data;
};

// Delete template
export const deleteTemplate = async (testCode) => {
  const response = await api.delete(
    `/laboratory/templates/${encodeURIComponent(testCode)}`,
  );

  return response.data;
};
