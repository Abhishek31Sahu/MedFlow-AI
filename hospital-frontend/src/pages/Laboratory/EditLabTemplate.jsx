import { useEffect, useState } from "react";

import { Box, CircularProgress, Typography } from "@mui/material";

import { useNavigate, useParams } from "react-router-dom";

import TemplateForm from "../../components/forms/TemplateForm";

import { getTemplate, updateTemplate } from "../../services/labTemplateApi";

export default function EditLabTemplate() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [template, setTemplate] = useState(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadTemplate = async () => {
      try {
        const response = await getTemplate(id);

        setTemplate(response?.data || response);
      } catch (error) {
        console.error(error);

        alert("Unable to load template.");

        navigate("/laboratory/templates");
      } finally {
        setLoading(false);
      }
    };

    loadTemplate();
  }, [id, navigate]);

  const handleSubmit = async (payload) => {
    await updateTemplate(id, payload);

    alert("Laboratory template updated successfully.");

    navigate("/laboratory/templates");
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          py: 10,
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (!template) {
    return null;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" fontWeight={700} mb={0.5}>
        Edit Laboratory Template
      </Typography>

      <Typography color="text.secondary" mb={3}>
        Update test details and parameters.
      </Typography>

      <TemplateForm
        initialData={template}
        onSubmit={handleSubmit}
        submitText="Update Template"
        onCancel={() => navigate("/laboratory/templates")}
      />
    </Box>
  );
}
