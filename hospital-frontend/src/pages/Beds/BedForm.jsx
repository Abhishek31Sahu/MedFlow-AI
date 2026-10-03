import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Paper,
  Card,
  CardContent,
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  FormControlLabel,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
  Chip,
} from "@mui/material";
import { AddLocationAlt, LocationOn } from "@mui/icons-material";

import { useNavigate, useParams } from "react-router-dom";

import bedService from "../../services/bedService";
import locationService from "../../services/locationService";

const initialForm = {
  bed_number: "",
  ward: "",
  room_number: "",
  department: "",
  floor: "",
  location_id: "",

  bed_type: "GENERAL",
  status: "AVAILABLE",
  gender_policy: "ANY",

  oxygen: false,
  ventilator: false,
  isolation: false,
  cardiac_monitor: false,
  dialysis: false,
  pediatric: false,
  maternity: false,
  cleaning_required: false,
};

export default function BedForm({ mode = "add" }) {
  const navigate = useNavigate();

  const { id } = useParams();

  // =====================================================
  // BED FORM
  // =====================================================

  const [form, setForm] = useState(initialForm);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  // =====================================================
  // LOCATION DIALOG
  // =====================================================

  const [openLocationDialog, setOpenLocationDialog] = useState(false);

  const [locationLoading, setLocationLoading] = useState(false);

  const [locationError, setLocationError] = useState("");

  const [locationForm, setLocationForm] = useState({
    name: "",
    description: "",
  });

  // =====================================================
  // LOAD BED
  // =====================================================

  useEffect(() => {
    if (mode === "edit") {
      loadBed();
    }
  }, [mode, id]);

  const loadBed = async () => {
    try {
      setLoading(true);

      const data = await bedService.getBed(id);

      setForm({
        ...initialForm,
        ...data,
      });
    } catch (err) {
      console.error(err);

      setError(err?.response?.data?.detail || "Failed to load bed.");
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // BED FORM CHANGE
  // =====================================================

  const handleChange = (e) => {
    const { name, value, checked, type } = e.target;

    setForm((prev) => ({
      ...prev,

      [name]: type === "checkbox" ? checked : value,
    }));
  };

  // =====================================================
  // LOCATION FORM CHANGE
  // =====================================================

  const handleLocationChange = (e) => {
    const { name, value } = e.target;

    setLocationForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // =====================================================
  // OPEN LOCATION DIALOG
  // =====================================================

  const handleOpenLocationDialog = () => {
    setLocationError("");

    setLocationForm({
      name: "",
      description: "",
    });

    setOpenLocationDialog(true);
  };

  // =====================================================
  // CLOSE LOCATION DIALOG
  // =====================================================

  const handleCloseLocationDialog = () => {
    if (locationLoading) {
      return;
    }

    setOpenLocationDialog(false);
  };

  // =====================================================
  // CREATE LOCATION
  // =====================================================

  const handleCreateLocation = async () => {
    if (!locationForm.name.trim()) {
      setLocationError("Location name is required.");

      return;
    }

    try {
      setLocationLoading(true);

      setLocationError("");

      const response = await locationService.createLocation({
        name: locationForm.name.trim(),

        description: locationForm.description.trim(),
      });

      console.log("Created location:", response);

      /*
       * Depending on your backend response,
       * the ID may be:
       *
       * response.id
       *
       * or
       *
       * response.location_id
       */

      const locationId = response?.id || response?.location_id;

      if (!locationId) {
        throw new Error(
          "Location created but location ID was not returned by the server.",
        );
      }

      // Automatically put location ID
      // into the bed form.

      setForm((prev) => ({
        ...prev,
        location_id: locationId,
      }));

      // Close dialog

      setOpenLocationDialog(false);

      // Reset location form

      setLocationForm({
        name: "",
        description: "",
      });
    } catch (err) {
      console.error("Failed to create location:", err);

      setLocationError(
        err?.response?.data?.detail ||
          err?.message ||
          "Failed to create location.",
      );
    } finally {
      setLocationLoading(false);
    }
  };

  // =====================================================
  // CREATE / UPDATE BED
  // =====================================================

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");

    // Location is required

    if (!form.location_id) {
      setError("Please create or provide a Location before creating the bed.");

      return;
    }

    try {
      setLoading(true);

      if (mode === "add") {
        await bedService.createBed(form);
      } else {
        await bedService.updateBed(id, form);
      }

      navigate("/beds");
    } catch (err) {
      console.error(err);

      setError(err?.response?.data?.detail || "Failed to save bed.");
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // UI
  // =====================================================

  return (
    <Box
      sx={{
        maxWidth: 1100,
        mx: "auto",
        mt: 3,
        mb: 5,
      }}
    >
      <Card
        elevation={2}
        sx={{
          borderRadius: 3,
        }}
      >
        <CardContent
          sx={{
            p: {
              xs: 2,
              md: 4,
            },
          }}
        >
          {/* =================================================
              HEADER
          ================================================= */}

          <Typography variant="h5" fontWeight={700} mb={0.5}>
            {mode === "add" ? "Add New Bed" : "Edit Bed"}
          </Typography>

          <Typography variant="body2" color="text.secondary" mb={3}>
            Configure bed information, location, status and available equipment.
          </Typography>

          {/* =================================================
              ERROR
          ================================================= */}

          {error && (
            <Alert
              severity="error"
              sx={{
                mb: 3,
                borderRadius: 2,
              }}
            >
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit}>
            {/* =================================================
                BASIC INFORMATION
            ================================================= */}

            <Typography variant="h6" fontWeight={600} mb={2}>
              Bed Information
            </Typography>

            <Grid container spacing={2}>
              {/* BED NUMBER */}

              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Bed Number"
                  name="bed_number"
                  value={form.bed_number}
                  onChange={handleChange}
                  required
                />
              </Grid>

              {/* WARD */}

              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Ward"
                  name="ward"
                  value={form.ward}
                  onChange={handleChange}
                  required
                />
              </Grid>

              {/* ROOM */}

              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Room Number"
                  name="room_number"
                  value={form.room_number}
                  onChange={handleChange}
                  required
                />
              </Grid>

              {/* DEPARTMENT */}

              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Department"
                  name="department"
                  value={form.department}
                  onChange={handleChange}
                  required
                />
              </Grid>

              {/* FLOOR */}

              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Floor"
                  name="floor"
                  value={form.floor}
                  onChange={handleChange}
                />
              </Grid>
            </Grid>

            {/* =================================================
                LOCATION
            ================================================= */}

            <Box
              sx={{
                mt: 4,
                mb: 3,
              }}
            >
              <Stack
                direction="row"
                justifyContent="space-between"
                alignItems="center"
                mb={2}
              >
                <Box>
                  <Stack direction="row" spacing={1} alignItems="center">
                    <LocationOn color="primary" />

                    <Typography variant="h6" fontWeight={600}>
                      Location
                    </Typography>
                  </Stack>

                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ mt: 0.5 }}
                  >
                    Select or create the hospital location for this bed.
                  </Typography>
                </Box>

                <Button
                  variant="outlined"
                  startIcon={<AddLocationAlt />}
                  onClick={handleOpenLocationDialog}
                >
                  Create Location
                </Button>
              </Stack>

              <Paper
                elevation={0}
                sx={{
                  p: 2,
                  borderRadius: 2,
                  border: "1px solid #e0e0e0",
                  backgroundColor: form.location_id ? "#f5fff7" : "#fafafa",
                }}
              >
                <Stack
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
                    fullWidth
                    label="Location ID"
                    name="location_id"
                    value={form.location_id}
                    onChange={handleChange}
                    required
                    helperText={
                      form.location_id
                        ? "Location selected"
                        : "Create a location to generate an ID"
                    }
                  />

                  {form.location_id && (
                    <Chip
                      label="Location Ready"
                      color="success"
                      sx={{
                        alignSelf: {
                          xs: "flex-start",
                          md: "center",
                        },
                      }}
                    />
                  )}
                </Stack>
              </Paper>
            </Box>

            {/* =================================================
                BED CONFIGURATION
            ================================================= */}

            <Typography variant="h6" fontWeight={600} mb={2}>
              Bed Configuration
            </Typography>

            <Grid container spacing={2}>
              {/* BED TYPE */}

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Bed Type</InputLabel>

                  <Select
                    name="bed_type"
                    value={form.bed_type}
                    label="Bed Type"
                    onChange={handleChange}
                  >
                    <MenuItem value="GENERAL">GENERAL</MenuItem>

                    <MenuItem value="ICU">ICU</MenuItem>

                    <MenuItem value="PRIVATE">PRIVATE</MenuItem>

                    <MenuItem value="ISOLATION">ISOLATION</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              {/* STATUS */}

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>

                  <Select
                    name="status"
                    value={form.status}
                    label="Status"
                    onChange={handleChange}
                  >
                    <MenuItem value="AVAILABLE">AVAILABLE</MenuItem>

                    <MenuItem value="OCCUPIED">OCCUPIED</MenuItem>

                    <MenuItem value="RESERVED">RESERVED</MenuItem>

                    <MenuItem value="CLEANING">CLEANING</MenuItem>

                    <MenuItem value="MAINTENANCE">MAINTENANCE</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              {/* GENDER POLICY */}

              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Gender Policy</InputLabel>

                  <Select
                    name="gender_policy"
                    value={form.gender_policy}
                    label="Gender Policy"
                    onChange={handleChange}
                  >
                    <MenuItem value="ANY">ANY</MenuItem>

                    <MenuItem value="MALE">MALE</MenuItem>

                    <MenuItem value="FEMALE">FEMALE</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>

            {/* =================================================
                EQUIPMENT
            ================================================= */}

            <Typography variant="h6" fontWeight={600} mt={4} mb={2}>
              Equipment & Capabilities
            </Typography>

            <Paper
              elevation={0}
              sx={{
                p: 2,
                border: "1px solid #e5e7eb",
                borderRadius: 2,
              }}
            >
              <Grid container spacing={1}>
                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={form.oxygen}
                        name="oxygen"
                        onChange={handleChange}
                      />
                    }
                    label="Oxygen"
                  />
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={form.ventilator}
                        name="ventilator"
                        onChange={handleChange}
                      />
                    }
                    label="Ventilator"
                  />
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={form.isolation}
                        name="isolation"
                        onChange={handleChange}
                      />
                    }
                    label="Isolation"
                  />
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={form.cardiac_monitor}
                        name="cardiac_monitor"
                        onChange={handleChange}
                      />
                    }
                    label="Cardiac Monitor"
                  />
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={form.dialysis}
                        name="dialysis"
                        onChange={handleChange}
                      />
                    }
                    label="Dialysis"
                  />
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={form.pediatric}
                        name="pediatric"
                        onChange={handleChange}
                      />
                    }
                    label="Pediatric"
                  />
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={form.maternity}
                        name="maternity"
                        onChange={handleChange}
                      />
                    }
                    label="Maternity"
                  />
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={form.cleaning_required}
                        name="cleaning_required"
                        onChange={handleChange}
                      />
                    }
                    label="Cleaning Required"
                  />
                </Grid>
              </Grid>
            </Paper>

            {/* =================================================
                ACTIONS
            ================================================= */}

            <Stack direction="row" spacing={2} justifyContent="flex-end" mt={4}>
              <Button
                variant="outlined"
                onClick={() => navigate("/beds")}
                disabled={loading}
              >
                Cancel
              </Button>

              <Button
                type="submit"
                variant="contained"
                disabled={loading || !form.location_id}
              >
                {loading
                  ? "Saving..."
                  : mode === "add"
                    ? "Create Bed"
                    : "Update Bed"}
              </Button>
            </Stack>
          </Box>
        </CardContent>
      </Card>

      {/* =====================================================
          CREATE LOCATION DIALOG
      ===================================================== */}

      <Dialog
        open={openLocationDialog}
        onClose={handleCloseLocationDialog}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle>Create Hospital Location</DialogTitle>

        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Create a location first. The generated Location ID will
            automatically be assigned to this bed.
          </Typography>

          {locationError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {locationError}
            </Alert>
          )}

          <Stack spacing={2}>
            <TextField
              fullWidth
              label="Location Name"
              name="name"
              value={locationForm.name}
              onChange={handleLocationChange}
              placeholder="e.g. ICU Ward A"
              required
              autoFocus
            />

            <TextField
              fullWidth
              label="Description"
              name="description"
              value={locationForm.description}
              onChange={handleLocationChange}
              placeholder="e.g. Intensive Care Unit - First Floor"
              multiline
              rows={3}
            />
          </Stack>
        </DialogContent>

        <DialogActions
          sx={{
            px: 3,
            pb: 2,
          }}
        >
          <Button
            onClick={handleCloseLocationDialog}
            disabled={locationLoading}
          >
            Cancel
          </Button>

          <Button
            variant="contained"
            startIcon={<AddLocationAlt />}
            onClick={handleCreateLocation}
            disabled={locationLoading}
          >
            {locationLoading ? "Creating..." : "Create Location"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
