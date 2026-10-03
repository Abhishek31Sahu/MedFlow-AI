import { useState } from "react";

import {
  Button,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";

const emptyTest = {
  code: "",
  name: "",
};

export default function LabOrderForm({ onSubmit, loading = false }) {
  const [form, setForm] = useState({
    patient_id: "",
    encounter_id: "",
    practitioner_id: "",
    priority: "ROUTINE",
    clinical_note: "",
    tests: [],
  });

  const updateField = (name, value) => {
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const addTest = () => {
    setForm((prev) => ({
      ...prev,
      tests: [...prev.tests, { ...emptyTest }],
    }));
  };

  const updateTest = (index, field, value) => {
    setForm((prev) => {
      const tests = [...prev.tests];

      tests[index] = {
        ...tests[index],
        [field]: value,
      };

      return {
        ...prev,
        tests,
      };
    });
  };

  const removeTest = (index) => {
    setForm((prev) => ({
      ...prev,
      tests: prev.tests.filter((_, i) => i !== index),
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (form.tests.length === 0) {
      alert("Add at least one laboratory test.");
      return;
    }

    onSubmit(form);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Card
        sx={{
          borderRadius: 3,
          mb: 3,
        }}
      >
        <CardContent>
          <Typography variant="h6" fontWeight={700} mb={3}>
            Patient Information
          </Typography>

          <Stack spacing={2}>
            <TextField
              label="Patient ID"
              value={form.patient_id}
              onChange={(e) => updateField("patient_id", e.target.value)}
              required
              fullWidth
            />

            <TextField
              label="Encounter ID"
              value={form.encounter_id}
              onChange={(e) => updateField("encounter_id", e.target.value)}
              fullWidth
            />

            <TextField
              label="Practitioner ID"
              value={form.practitioner_id}
              onChange={(e) => updateField("practitioner_id", e.target.value)}
              required
              fullWidth
            />

            <FormControl fullWidth>
              <InputLabel>Priority</InputLabel>

              <Select
                value={form.priority}
                label="Priority"
                onChange={(e) => updateField("priority", e.target.value)}
              >
                <MenuItem value="ROUTINE">Routine</MenuItem>

                <MenuItem value="URGENT">Urgent</MenuItem>

                <MenuItem value="STAT">STAT</MenuItem>
              </Select>
            </FormControl>

            <TextField
              label="Clinical Note"
              multiline
              rows={4}
              value={form.clinical_note}
              onChange={(e) => updateField("clinical_note", e.target.value)}
              fullWidth
            />
          </Stack>
        </CardContent>
      </Card>

      {/* Tests */}

      <Card
        sx={{
          borderRadius: 3,
          mb: 3,
        }}
      >
        <CardContent>
          <Stack
            direction="row"
            justifyContent="space-between"
            alignItems="center"
            mb={3}
          >
            <Typography variant="h6" fontWeight={700}>
              Laboratory Tests
            </Typography>

            <Button
              variant="outlined"
              startIcon={<AddIcon />}
              onClick={addTest}
            >
              Add Test
            </Button>
          </Stack>

          {form.tests.length === 0 && (
            <Typography color="text.secondary">No tests added.</Typography>
          )}

          <Stack spacing={2}>
            {form.tests.map((test, index) => (
              <Stack
                key={index}
                direction={{
                  xs: "column",
                  md: "row",
                }}
                spacing={2}
                alignItems={{
                  xs: "stretch",
                  md: "center",
                }}
              >
                <TextField
                  label="Test Code"
                  value={test.code}
                  onChange={(e) => updateTest(index, "code", e.target.value)}
                  required
                  fullWidth
                />

                <TextField
                  label="Test Name"
                  value={test.name}
                  onChange={(e) => updateTest(index, "name", e.target.value)}
                  required
                  fullWidth
                />

                <Button
                  color="error"
                  onClick={() => removeTest(index)}
                  startIcon={<DeleteIcon />}
                >
                  Remove
                </Button>
              </Stack>
            ))}
          </Stack>
        </CardContent>
      </Card>

      <Stack direction="row" justifyContent="flex-end">
        <Button type="submit" variant="contained" disabled={loading}>
          {loading ? "Creating..." : "Create Lab Order"}
        </Button>
      </Stack>
    </form>
  );
}
