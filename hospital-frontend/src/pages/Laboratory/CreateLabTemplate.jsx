import { Box, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

import TemplateForm from "../../components/forms/TemplateForm";

import { createTemplate } from "../../services/labTemplateApi";

export default function CreateLabTemplate() {
  const navigate = useNavigate();

  const handleSubmit = async (payload) => {
    await createTemplate(payload);

    alert("Laboratory template created successfully.");

    navigate("/laboratory/templates");
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" fontWeight={700} mb={0.5}>
        Create Laboratory Template
      </Typography>

      <Typography color="text.secondary" mb={3}>
        Create a new laboratory test and define its parameters.
      </Typography>

      <TemplateForm
        onSubmit={handleSubmit}
        submitText="Create Template"
        onCancel={() => navigate("/laboratory/templates")}
      />
    </Box>
  );
}
