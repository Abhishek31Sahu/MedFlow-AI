import api from "../api/axios";

// ==========================================
// Create Lab Order
// ==========================================

export const createLabOrder = async (data) => {
  const response = await api.post("/laboratory/orders", data);

  return response.data;
};

// ==========================================
// Pending Orders
// ==========================================

export const getPendingLabOrders = async () => {
  const response = await api.get("/laboratory/orders/pending");

  return response.data;
};

// ==========================================
// Patient Orders
// ==========================================

export const getPatientLabOrders = async (patientId) => {
  const response = await api.get(
    `/laboratory/orders/patient/${encodeURIComponent(patientId)}`,
  );

  return response.data;
};

// ==========================================
// Submit Results
// ==========================================

export const submitLabResults = async (data) => {
  const response = await api.post("/laboratory/results", data);

  return response.data;
};

// ==========================================
// Get Report by ID
// ==========================================

export const getLabReport = async (reportId) => {
  const response = await api.get(
    `/laboratory/reports/${encodeURIComponent(reportId)}`,
  );

  return response.data;
};

export const getObservation = async (observationId) => {
  const response = await api.get(
    `/observations/${encodeURIComponent(observationId)}`,
  );

  return response.data;
};

// ==========================================
// Patient Reports
// ==========================================

export const getPatientReports = async (patientId) => {
  const response = await api.get(
    `/laboratory/reports/patient/${encodeURIComponent(patientId)}`,
  );

  return response.data;
};

// ==========================================
// Report by ServiceRequest
// ==========================================

export const getReportByServiceRequest = async (serviceRequestId) => {
  const response = await api.get(
    `/laboratory/reports/service_request/${encodeURIComponent(
      serviceRequestId,
    )}`,
  );

  return response.data;
};

// ==========================================
// Pending FHIR Orders
// ==========================================

export const getPendingFHIROrders = async () => {
  const response = await api.get("/laboratory/fhir/pending");

  return response.data;
};

export const getTemplate = async (testCode) => {
  const response = await api.get(
    `/laboratory/templates/${encodeURIComponent(testCode)}`,
  );

  return response.data;
};

export const getLabOrder = async (serviceRequestId) => {
  const response = await api.get(
    `/laboratory/orders/service_request/${encodeURIComponent(serviceRequestId)}`,
  );

  return response.data;
};
