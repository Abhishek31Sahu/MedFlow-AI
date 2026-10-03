import { useState } from "react";

import { Box, Typography } from "@mui/material";

import { useNavigate } from "react-router-dom";

import LabOrderForm from "../../components/forms/LabOrderForm";

import { createLabOrder } from "../../services/laboratoryApi";

export default function CreateLabOrder() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (data) => {
    try {
      setLoading(true);

      await createLabOrder(data);

      alert("Laboratory order created successfully.");

      navigate("/laboratory/orders/pending");
    } catch (error) {
      console.error(error);

      alert(
        error.response?.data?.detail || "Unable to create laboratory order.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" fontWeight={700} mb={0.5}>
        Create Lab Order
      </Typography>

      <Typography color="text.secondary" mb={3}>
        Create a laboratory test request.
      </Typography>

      <LabOrderForm onSubmit={handleSubmit} loading={loading} />
    </Box>
  );
}
