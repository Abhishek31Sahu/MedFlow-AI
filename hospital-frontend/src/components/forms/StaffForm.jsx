import { useEffect, useState } from "react";

import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Switch,
  CircularProgress,
  Typography,
} from "@mui/material";

const roles = [
  "admin",
  "doctor",
  "nurse",
  "receptionist",
  "lab_technician",
  "pharmacist",
];

const initialFormData = {
  username: "",
  email: "",
  password: "",
  confirmPassword: "",

  first_name: "",
  last_name: "",
  phone: "",
  department: "",
  designation: "",

  role: "doctor",
  is_active: true,
};

export default function StaffForm({
  open,
  onClose,
  onSubmit,
  initialData = null,
  loading = false,
}) {
  const isEdit = Boolean(initialData);

  const [formData, setFormData] = useState(initialFormData);
  const [errors, setErrors] = useState({});

  // ================= INITIALIZE FORM =================
  useEffect(() => {
    if (initialData) {
      setFormData({
        username: initialData.username || "",
        email: initialData.email || "",
        password: "",
        confirmPassword: "",

        first_name: initialData.first_name || "",
        last_name: initialData.last_name || "",
        phone: initialData.phone || "",
        department: initialData.department || "",
        designation: initialData.designation || "",

        role: initialData.role || "doctor",
        is_active: initialData.is_active ?? true,
      });
    } else {
      setFormData(initialFormData);
    }

    setErrors({});
  }, [initialData, open]);

  // ================= HANDLE INPUT =================
  const handleChange = (event) => {
    const { name, value, checked, type } = event.target;

    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));

    // Clear field error when user starts correcting it
    setErrors((prev) => ({
      ...prev,
      [name]: "",
    }));
  };

  // ================= VALIDATION =================
  const validate = () => {
    const newErrors = {};

    // Username
    if (!formData.username.trim()) {
      newErrors.username = "Username is required";
    }

    // Email
    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (
      !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(formData.email)
    ) {
      newErrors.email = "Invalid email address";
    }

    // First name
    if (!formData.first_name.trim()) {
      newErrors.first_name = "First name is required";
    }

    // Password only required while creating
    if (!isEdit) {
      if (!formData.password) {
        newErrors.password = "Password is required";
      } else if (formData.password.length < 6) {
        newErrors.password = "Password must be at least 6 characters";
      }

      if (!formData.confirmPassword) {
        newErrors.confirmPassword = "Confirm password is required";
      }

      if (
        formData.password &&
        formData.confirmPassword &&
        formData.password !== formData.confirmPassword
      ) {
        newErrors.confirmPassword = "Passwords do not match";
      }
    }

    // Role
    if (!formData.role) {
      newErrors.role = "Role is required";
    }

    // Phone
    if (formData.phone.trim()) {
      const phoneRegex = /^[0-9+\-\s()]{7,20}$/;

      if (!phoneRegex.test(formData.phone.trim())) {
        newErrors.phone = "Invalid phone number";
      }
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  // ================= SUBMIT =================
  const handleSubmit = () => {
    if (!validate()) {
      return;
    }

    const payload = {
      username: formData.username.trim(),
      email: formData.email.trim(),

      first_name: formData.first_name.trim(),
      last_name: formData.last_name.trim(),
      phone: formData.phone.trim(),
      department: formData.department.trim(),
      designation: formData.designation.trim(),

      role: formData.role,
      is_active: formData.is_active,
    };

    // Password is only sent while creating a user
    if (!isEdit) {
      payload.password = formData.password;
    }

    console.log("Staff form payload:", payload);

    onSubmit(payload);
  };

  return (
    <Dialog
      open={open}
      onClose={loading ? undefined : onClose}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>{isEdit ? "Edit User" : "Create User"}</DialogTitle>

      <DialogContent dividers>
        <Grid container spacing={2} sx={{ mt: 0.5 }}>
          {/* ================= PERSONAL INFORMATION ================= */}
          <Grid size={{ xs: 12 }}>
            <Typography variant="subtitle1" fontWeight={600}>
              Personal Information
            </Typography>
          </Grid>

          {/* First Name */}
          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="First Name"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              error={Boolean(errors.first_name)}
              helperText={errors.first_name}
              required
            />
          </Grid>

          {/* Last Name */}
          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="Last Name"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
            />
          </Grid>

          {/* Phone */}
          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="Phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              error={Boolean(errors.phone)}
              helperText={errors.phone}
            />
          </Grid>

          {/* Email */}
          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="Email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              error={Boolean(errors.email)}
              helperText={errors.email}
              required
            />
          </Grid>

          {/* ================= ACCOUNT INFORMATION ================= */}
          <Grid size={{ xs: 12 }} sx={{ mt: 1 }}>
            <Typography variant="subtitle1" fontWeight={600}>
              Account Information
            </Typography>
          </Grid>

          {/* Username */}
          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="Username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              error={Boolean(errors.username)}
              helperText={errors.username}
              required
            />
          </Grid>

          {/* Role */}
          <Grid size={{ xs: 12, md: 6 }}>
            <FormControl fullWidth error={Boolean(errors.role)} required>
              <InputLabel>Role</InputLabel>

              <Select
                name="role"
                value={formData.role}
                label="Role"
                onChange={handleChange}
              >
                {roles.map((role) => (
                  <MenuItem key={role} value={role}>
                    {role
                      .split("_")
                      .map(
                        (word) => word.charAt(0).toUpperCase() + word.slice(1),
                      )
                      .join(" ")}
                  </MenuItem>
                ))}
              </Select>

              {errors.role && (
                <Typography
                  variant="caption"
                  color="error"
                  sx={{ mt: 0.5, ml: 1.5 }}
                >
                  {errors.role}
                </Typography>
              )}
            </FormControl>
          </Grid>

          {/* Password */}
          {!isEdit && (
            <>
              <Grid size={{ xs: 12, md: 6 }}>
                <TextField
                  fullWidth
                  type="password"
                  label="Password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  error={Boolean(errors.password)}
                  helperText={errors.password}
                  required
                />
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <TextField
                  fullWidth
                  type="password"
                  label="Confirm Password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  error={Boolean(errors.confirmPassword)}
                  helperText={errors.confirmPassword}
                  required
                />
              </Grid>
            </>
          )}

          {/* ================= PROFESSIONAL INFORMATION ================= */}
          <Grid size={{ xs: 12 }} sx={{ mt: 1 }}>
            <Typography variant="subtitle1" fontWeight={600}>
              Professional Information
            </Typography>
          </Grid>

          {/* Department */}
          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="Department"
              name="department"
              value={formData.department}
              onChange={handleChange}
              placeholder="e.g. Cardiology"
            />
          </Grid>

          {/* Designation */}
          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="Designation"
              name="designation"
              value={formData.designation}
              onChange={handleChange}
              placeholder="e.g. Senior Doctor"
            />
          </Grid>

          {/* ================= STATUS ================= */}
          <Grid size={{ xs: 12 }} sx={{ mt: 1 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={formData.is_active}
                  onChange={handleChange}
                  name="is_active"
                />
              }
              label="Active User"
            />
          </Grid>
        </Grid>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} color="inherit" disabled={loading}>
          Cancel
        </Button>

        <Button variant="contained" onClick={handleSubmit} disabled={loading}>
          {loading ? (
            <CircularProgress size={22} color="inherit" />
          ) : isEdit ? (
            "Update User"
          ) : (
            "Create User"
          )}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
