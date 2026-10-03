import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  CircularProgress,
  Paper,
  TextField,
  Typography,
} from "@mui/material";

import { useParams, useNavigate } from "react-router-dom";

import { getLabOrder, submitLabResults } from "../../services/laboratoryApi";

import { getTemplate } from "../../services/labTemplateApi";

const SubmitLabResults = () => {
  const { serviceRequestId } = useParams();
  const navigate = useNavigate();

  const [order, setOrder] = useState(null);
  const [template, setTemplate] = useState(null);

  const [results, setResults] = useState({});

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (serviceRequestId) {
      loadData();
    }
  }, [serviceRequestId]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      // 1. Get laboratory order using service request ID
      const orderData = await getLabOrder(serviceRequestId);

      console.log("Order Data:", orderData);

      setOrder(orderData);

      // 2. Get template using test code from order
      const templateData = await getTemplate(orderData.test_code);

      console.log("Template Data:", templateData);

      setTemplate(templateData);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail || "Failed to load laboratory report data",
      );
    } finally {
      setLoading(false);
    }
  };

  // Store entered value
  const handleChange = (code, value) => {
    setResults((prev) => ({
      ...prev,
      [code]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!template || !Array.isArray(template.parameters)) {
      setError("Laboratory template parameters are not available");
      return;
    }

    try {
      setSubmitting(true);
      setError("");

      // -----------------------------
      // Validate required parameters
      // -----------------------------
      for (const parameter of template.parameters) {
        const value = results[parameter.code];

        if (parameter.required && (value === undefined || value === "")) {
          setError(`${parameter.name} is required`);
          setSubmitting(false);
          return;
        }
      }

      // -----------------------------
      // Technician ID
      // -----------------------------
      //   const technicianId = localStorage.getItem("technician_id");
      const technicianId = "1053";
      if (!technicianId) {
        setError("Technician ID not found");
        setSubmitting(false);
        return;
      }

      // -----------------------------
      // Build EXACT backend payload
      // -----------------------------
      const payload = {
        service_request_id: serviceRequestId,

        technician_id: technicianId,

        parameters: template.parameters.map((parameter) => ({
          code: parameter.code,

          name: parameter.name,

          value:
            parameter.value_type === "number"
              ? Number(results[parameter.code])
              : results[parameter.code],

          unit: parameter.unit || "",

          reference_range:
            parameter.reference_low != null && parameter.reference_high != null
              ? `${parameter.reference_low} - ${parameter.reference_high}`
              : "",
        })),
      };

      console.log("Final Payload:", payload);

      try {
        console.log("Before submit");

        const response = await submitLabResults(payload);

        console.log("Submit Response:", response);
        console.log("Response ID:", response?.id);

        const reportId = response?.id;

        if (!reportId) {
          console.error("No report ID returned");
          return;
        }

        const reportUrl = `/laboratory/reports/${encodeURIComponent(reportId)}`;

        console.log("Navigating to:", reportUrl);

        navigate(reportUrl);
      } catch (err) {
        console.error("Submit/navigate error:", err);
      }
    } catch (err) {
      console.error("FULL ERROR:", err);
      console.error("STATUS:", err.response?.status);
      console.error("BACKEND RESPONSE:", err.response?.data);

      setError(
        err.response?.data?.detail || "Failed to submit laboratory report",
      );
    } finally {
      setSubmitting(false);
    }
  };

  // -----------------------------
  // Loading
  // -----------------------------
  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          mt: 5,
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  // -----------------------------
  // Error
  // -----------------------------
  if (error && !template) {
    return (
      <Typography color="error" sx={{ p: 3 }}>
        {error}
      </Typography>
    );
  }

  // -----------------------------
  // No template
  // -----------------------------
  if (!template) {
    return (
      <Typography sx={{ p: 3 }}>Laboratory template not found.</Typography>
    );
  }

  // -----------------------------
  // Render
  // -----------------------------
  return (
    <Box
      sx={{
        maxWidth: 900,
        mx: "auto",
        p: 3,
      }}
    >
      <Typography variant="h4" gutterBottom>
        Create Laboratory Report
      </Typography>

      {/* =========================
          ORDER INFORMATION
      ========================= */}
      {order && (
        <Paper
          sx={{
            p: 3,
            mb: 3,
          }}
        >
          <Typography variant="h6">Patient ID: {order.patient_id}</Typography>

          <Typography>Test: {order.test_name}</Typography>

          <Typography>Test Code: {order.test_code}</Typography>

          <Typography>Service Request ID: {serviceRequestId}</Typography>

          <Typography>Order ID: {order.id}</Typography>
        </Paper>
      )}

      {/* =========================
          TEMPLATE / PARAMETERS
      ========================= */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          {template.test_name}
        </Typography>

        <Typography color="text.secondary" sx={{ mb: 3 }}>
          {template.description}
        </Typography>

        <form onSubmit={handleSubmit}>
          {Array.isArray(template.parameters) &&
            template.parameters.map((parameter) => (
              <Box key={parameter.code} sx={{ mb: 3 }}>
                <TextField
                  fullWidth
                  label={parameter.name}
                  type={parameter.value_type === "number" ? "number" : "text"}
                  value={results[parameter.code] ?? ""}
                  required={parameter.required}
                  onChange={(e) => handleChange(parameter.code, e.target.value)}
                />

                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{ mt: 0.5 }}
                >
                  Code: {parameter.code}
                  {" | "}
                  Unit: {parameter.unit || "-"}
                  {" | "}
                  Reference: {parameter.reference_low ?? "-"}
                  {" - "}
                  {parameter.reference_high ?? "-"}
                </Typography>
              </Box>
            ))}

          {error && (
            <Typography color="error" sx={{ mb: 2 }}>
              {error}
            </Typography>
          )}

          <Button type="submit" variant="contained" disabled={submitting}>
            {submitting ? "Submitting..." : "Submit Laboratory Report"}
          </Button>
        </form>
      </Paper>
    </Box>
  );
};

export default SubmitLabResults;
