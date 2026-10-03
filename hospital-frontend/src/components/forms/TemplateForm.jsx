import { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Checkbox,
  Divider,
  FormControl,
  FormControlLabel,
  Grid,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import SaveOutlinedIcon from "@mui/icons-material/SaveOutlined";

const emptyParameter = {
  code: "",
  name: "",
  unit: "",
  value_type: "number",
  reference_low: "",
  reference_high: "",
  required: true,
};

const emptyTemplate = {
  test_code: "",
  test_name: "",
  category: "",
  description: "",
  parameters: [],
};

export default function TemplateForm({
  initialData = emptyTemplate,
  onSubmit,
  submitText = "Create Template",
  onCancel,
}) {
  const [form, setForm] = useState({
    ...emptyTemplate,
    ...initialData,
    parameters: initialData?.parameters || [],
  });

  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setForm({
      ...emptyTemplate,
      ...initialData,
      parameters: initialData?.parameters || [],
    });
  }, [initialData]);

  // -----------------------------------------
  // Basic information
  // -----------------------------------------

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // -----------------------------------------
  // Parameter
  // -----------------------------------------

  const updateParameter = (index, field, value) => {
    setForm((prev) => {
      const parameters = [...prev.parameters];

      parameters[index] = {
        ...parameters[index],
        [field]: value,
      };

      return {
        ...prev,
        parameters,
      };
    });
  };

  const addParameter = () => {
    setForm((prev) => ({
      ...prev,
      parameters: [
        ...prev.parameters,
        {
          ...emptyParameter,
        },
      ],
    }));
  };

  const removeParameter = (index) => {
    setForm((prev) => ({
      ...prev,
      parameters: prev.parameters.filter((_, i) => i !== index),
    }));
  };

  // -----------------------------------------
  // Submit
  // -----------------------------------------

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!form.test_code.trim()) {
      alert("Test code is required.");
      return;
    }

    if (!form.test_name.trim()) {
      alert("Test name is required.");
      return;
    }

    if (!form.category.trim()) {
      alert("Category is required.");
      return;
    }

    if (form.parameters.length === 0) {
      alert("Add at least one parameter.");
      return;
    }

    for (let index = 0; index < form.parameters.length; index++) {
      const parameter = form.parameters[index];

      if (!parameter.code.trim()) {
        alert(`Parameter ${index + 1}: code is required.`);
        return;
      }

      if (!parameter.name.trim()) {
        alert(`Parameter ${index + 1}: name is required.`);
        return;
      }
    }

    const payload = {
      test_code: form.test_code.trim(),
      test_name: form.test_name.trim(),
      category: form.category.trim(),
      description: form.description?.trim() || null,

      parameters: form.parameters.map((parameter) => ({
        ...(parameter.id ? { id: parameter.id } : {}),

        code: parameter.code.trim(),
        name: parameter.name.trim(),
        unit: parameter.unit?.trim() || null,

        value_type: parameter.value_type || "number",

        reference_low:
          parameter.reference_low === ""
            ? null
            : Number(parameter.reference_low),

        reference_high:
          parameter.reference_high === ""
            ? null
            : Number(parameter.reference_high),

        required: parameter.required ?? true,
      })),
    };

    try {
      setSaving(true);

      await onSubmit(payload);
    } catch (error) {
      console.error(error);

      alert(error.response?.data?.detail || "Unable to save template.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      {/* =======================================
          TEST INFORMATION
      ======================================== */}

      <Card
        elevation={0}
        sx={{
          mb: 3,
          border: "1px solid #E2E8F0",
          borderRadius: 3,
        }}
      >
        <CardContent sx={{ p: 3 }}>
          <Typography variant="h6" fontWeight={700} mb={3}>
            Test Information
          </Typography>

          <Grid container spacing={2.5}>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Test Code"
                name="test_code"
                value={form.test_code}
                onChange={handleChange}
                placeholder="CBC"
                required
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Test Name"
                name="test_name"
                value={form.test_name}
                onChange={handleChange}
                placeholder="Complete Blood Count"
                required
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Category</InputLabel>

                <Select
                  name="category"
                  label="Category"
                  value={form.category}
                  onChange={handleChange}
                  required
                >
                  <MenuItem value="Hematology">Hematology</MenuItem>

                  <MenuItem value="Biochemistry">Biochemistry</MenuItem>

                  <MenuItem value="Microbiology">Microbiology</MenuItem>

                  <MenuItem value="Immunology">Immunology</MenuItem>

                  <MenuItem value="Pathology">Pathology</MenuItem>

                  <MenuItem value="Other">Other</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          <TextField
            fullWidth
            multiline
            rows={4}
            label="Description"
            name="description"
            value={form.description || ""}
            onChange={handleChange}
            placeholder="Describe this laboratory test..."
            sx={{ mt: 2.5 }}
          />
        </CardContent>
      </Card>

      {/* =======================================
          PARAMETERS
      ======================================== */}

      <Card
        elevation={0}
        sx={{
          border: "1px solid #E2E8F0",
          borderRadius: 3,
        }}
      >
        <CardContent sx={{ p: 3 }}>
          <Stack
            direction="row"
            justifyContent="space-between"
            alignItems="center"
            mb={3}
          >
            <Box>
              <Typography variant="h6" fontWeight={700}>
                Parameters
              </Typography>

              <Typography variant="body2" color="text.secondary">
                Define the values measured for this laboratory test.
              </Typography>
            </Box>

            <Button
              variant="outlined"
              startIcon={<AddIcon />}
              onClick={addParameter}
            >
              Add Parameter
            </Button>
          </Stack>

          {form.parameters.map((parameter, index) => (
            <Box
              key={parameter.id || index}
              sx={{
                border: "1px solid #E2E8F0",
                borderRadius: 2,
                p: 2.5,
                mb: 2,
                background: "#FAFCFF",
              }}
            >
              <Stack direction="row" justifyContent="space-between" mb={2}>
                <Typography fontWeight={600}>Parameter {index + 1}</Typography>

                <IconButton
                  color="error"
                  onClick={() => removeParameter(index)}
                >
                  <DeleteIcon />
                </IconButton>
              </Stack>

              <Grid container spacing={2}>
                <Grid item xs={12} md={2}>
                  <TextField
                    fullWidth
                    size="small"
                    label="Code"
                    value={parameter.code}
                    onChange={(e) =>
                      updateParameter(index, "code", e.target.value)
                    }
                    required
                  />
                </Grid>

                <Grid item xs={12} md={3}>
                  <TextField
                    fullWidth
                    size="small"
                    label="Name"
                    value={parameter.name}
                    onChange={(e) =>
                      updateParameter(index, "name", e.target.value)
                    }
                    required
                  />
                </Grid>

                <Grid item xs={12} md={2}>
                  <TextField
                    fullWidth
                    size="small"
                    label="Unit"
                    value={parameter.unit || ""}
                    onChange={(e) =>
                      updateParameter(index, "unit", e.target.value)
                    }
                  />
                </Grid>

                <Grid item xs={12} md={2}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Value Type</InputLabel>

                    <Select
                      label="Value Type"
                      value={parameter.value_type || "number"}
                      onChange={(e) =>
                        updateParameter(index, "value_type", e.target.value)
                      }
                    >
                      <MenuItem value="number">Number</MenuItem>

                      <MenuItem value="text">Text</MenuItem>

                      <MenuItem value="boolean">Boolean</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12} md={1.5}>
                  <TextField
                    fullWidth
                    size="small"
                    type="number"
                    label="Ref. Low"
                    value={parameter.reference_low ?? ""}
                    onChange={(e) =>
                      updateParameter(index, "reference_low", e.target.value)
                    }
                  />
                </Grid>

                <Grid item xs={12} md={1.5}>
                  <TextField
                    fullWidth
                    size="small"
                    type="number"
                    label="Ref. High"
                    value={parameter.reference_high ?? ""}
                    onChange={(e) =>
                      updateParameter(index, "reference_high", e.target.value)
                    }
                  />
                </Grid>
              </Grid>

              <FormControlLabel
                sx={{ mt: 1 }}
                control={
                  <Checkbox
                    checked={parameter.required ?? true}
                    onChange={(e) =>
                      updateParameter(index, "required", e.target.checked)
                    }
                  />
                }
                label="Required parameter"
              />
            </Box>
          ))}

          {form.parameters.length === 0 && (
            <Box
              sx={{
                py: 7,
                textAlign: "center",
                border: "1px dashed #CBD5E1",
                borderRadius: 2,
              }}
            >
              <Typography color="text.secondary" mb={2}>
                No parameters added yet.
              </Typography>

              <Button
                variant="outlined"
                startIcon={<AddIcon />}
                onClick={addParameter}
              >
                Add First Parameter
              </Button>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* =======================================
          ACTIONS
      ======================================== */}

      <Stack direction="row" justifyContent="flex-end" spacing={2} mt={3}>
        {onCancel && (
          <Button variant="outlined" onClick={onCancel}>
            Cancel
          </Button>
        )}

        <Button
          type="submit"
          variant="contained"
          startIcon={<SaveOutlinedIcon />}
          disabled={saving}
          sx={{
            px: 3,
            borderRadius: 2,
          }}
        >
          {saving ? "Saving..." : submitText}
        </Button>
      </Stack>
    </Box>
  );
}
