import { useEffect, useState } from "react";

import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

const DAYS = [
  "MONDAY",
  "TUESDAY",
  "WEDNESDAY",
  "THURSDAY",
  "FRIDAY",
  "SATURDAY",
  "SUNDAY",
];

const EMPTY_FORM = {
  day_of_week: "",
  start_time: "",
  end_time: "",
};

export default function StaffScheduleForm({
  open,
  staff,
  initialData = null,
  onClose,
  onSubmit,
  loading = false,
}) {
  const [formData, setFormData] = useState(EMPTY_FORM);
  const [error, setError] = useState("");

  /**
   * Load existing schedule when editing
   */
  useEffect(() => {
    if (!open) {
      return;
    }

    setError("");

    if (initialData) {
      setFormData({
        day_of_week: initialData.day_of_week || "",

        start_time: initialData.start_time
          ? String(initialData.start_time).substring(0, 5)
          : "",

        end_time: initialData.end_time
          ? String(initialData.end_time).substring(0, 5)
          : "",
      });
    } else {
      setFormData(EMPTY_FORM);
    }
  }, [open, initialData]);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    setError("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    if (!staff?.practitioner_id) {
      setError("This staff member does not have a practitioner ID.");
      return;
    }

    if (!formData.day_of_week) {
      setError("Please select a day.");
      return;
    }

    if (!formData.start_time) {
      setError("Please select a start time.");
      return;
    }

    if (!formData.end_time) {
      setError("Please select an end time.");
      return;
    }

    if (formData.start_time >= formData.end_time) {
      setError("End time must be after start time.");
      return;
    }

    const payload = {
      practitioner_id: staff.practitioner_id,

      day_of_week: formData.day_of_week,

      start_time: `${formData.start_time}:00`,

      end_time: `${formData.end_time}:00`,
    };

    try {
      await onSubmit(payload);
    } catch (error) {
      console.error(error);

      setError(error?.response?.data?.detail || "Failed to save schedule.");
    }
  };

  const fullName = [staff?.first_name, staff?.last_name]
    .filter(Boolean)
    .join(" ");

  return (
    <Dialog
      open={open}
      onClose={loading ? undefined : onClose}
      fullWidth
      maxWidth="sm"
    >
      <Box component="form" onSubmit={handleSubmit}>
        <DialogTitle>
          {initialData
            ? "Edit Practitioner Schedule"
            : "Add Practitioner Schedule"}
        </DialogTitle>

        <DialogContent>
          <Stack spacing={3} sx={{ mt: 1 }}>
            {/* STAFF */}
            <Box
              sx={{
                p: 2,
                borderRadius: 2,
                bgcolor: "grey.100",
              }}
            >
              <Typography fontWeight={600}>
                {fullName || staff?.username || "Staff"}
              </Typography>

              <Typography variant="body2" color="text.secondary">
                {staff?.designation || "Staff"}

                {staff?.department ? ` • ${staff.department}` : ""}
              </Typography>

              <Typography variant="caption" color="text.secondary">
                Practitioner ID: {staff?.practitioner_id || "Not created"}
              </Typography>
            </Box>

            {/* ERROR */}
            {error && <Alert severity="error">{error}</Alert>}

            {/* DAY */}
            <FormControl fullWidth>
              <InputLabel>Day</InputLabel>

              <Select
                name="day_of_week"
                value={formData.day_of_week}
                label="Day"
                onChange={handleChange}
              >
                {DAYS.map((day) => (
                  <MenuItem key={day} value={day}>
                    {day.charAt(0) + day.slice(1).toLowerCase()}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {/* TIME */}
            <Stack
              direction={{
                xs: "column",
                sm: "row",
              }}
              spacing={2}
            >
              <TextField
                fullWidth
                label="Start Time"
                type="time"
                name="start_time"
                value={formData.start_time}
                onChange={handleChange}
                InputLabelProps={{
                  shrink: true,
                }}
              />

              <TextField
                fullWidth
                label="End Time"
                type="time"
                name="end_time"
                value={formData.end_time}
                onChange={handleChange}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Stack>
          </Stack>
        </DialogContent>

        <DialogActions sx={{ px: 3, pb: 3 }}>
          <Button onClick={onClose} disabled={loading}>
            Cancel
          </Button>

          <Button type="submit" variant="contained" disabled={loading}>
            {loading
              ? "Saving..."
              : initialData
                ? "Update Schedule"
                : "Add Schedule"}
          </Button>
        </DialogActions>
      </Box>
    </Dialog>
  );
}
