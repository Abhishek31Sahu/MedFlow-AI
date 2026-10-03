import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Button,
} from "@mui/material";
import { FaFilter, FaUndo } from "react-icons/fa";

export default function FilterBar({
  role,
  status,
  department,
  onRoleChange,
  onStatusChange,
  onDepartmentChange,
  onReset,
}) {
  return (
    <div className="flex flex-wrap items-center gap-4 rounded-2xl bg-white p-5 shadow-md">
      {/* Role */}

      <FormControl size="small" sx={{ minWidth: 180 }}>
        <InputLabel>Role</InputLabel>

        <Select value={role} label="Role" onChange={onRoleChange}>
          <MenuItem value="">All Roles</MenuItem>
          <MenuItem value="ADMIN">Admin</MenuItem>
          <MenuItem value="DOCTOR">Doctor</MenuItem>
          <MenuItem value="NURSE">Nurse</MenuItem>
          <MenuItem value="RECEPTIONIST">Receptionist</MenuItem>
          <MenuItem value="LAB_TECHNICIAN">Lab Technician</MenuItem>
          <MenuItem value="PHARMACIST">Pharmacist</MenuItem>
        </Select>
      </FormControl>

      {/* Status */}

      <FormControl size="small" sx={{ minWidth: 180 }}>
        <InputLabel>Status</InputLabel>

        <Select value={status} label="Status" onChange={onStatusChange}>
          <MenuItem value="">All Status</MenuItem>
          <MenuItem value="ACTIVE">Active</MenuItem>
          <MenuItem value="INACTIVE">Inactive</MenuItem>
        </Select>
      </FormControl>

      {/* Department */}

      <FormControl size="small" sx={{ minWidth: 200 }}>
        <InputLabel>Department</InputLabel>

        <Select
          value={department}
          label="Department"
          onChange={onDepartmentChange}
        >
          <MenuItem value="">All Departments</MenuItem>
          <MenuItem value="Emergency">Emergency</MenuItem>
          <MenuItem value="ICU">ICU</MenuItem>
          <MenuItem value="Cardiology">Cardiology</MenuItem>
          <MenuItem value="Neurology">Neurology</MenuItem>
          <MenuItem value="Orthopedics">Orthopedics</MenuItem>
          <MenuItem value="Radiology">Radiology</MenuItem>
          <MenuItem value="Laboratory">Laboratory</MenuItem>
          <MenuItem value="Pharmacy">Pharmacy</MenuItem>
        </Select>
      </FormControl>

      {/* Reset */}

      <Button
        variant="outlined"
        color="secondary"
        startIcon={<FaUndo />}
        onClick={onReset}
        sx={{
          height: 40,
        }}
      >
        Reset
      </Button>

      {/* Filter */}

      <Button
        variant="contained"
        startIcon={<FaFilter />}
        sx={{
          height: 40,
          ml: "auto",
        }}
      >
        Apply Filters
      </Button>
    </div>
  );
}
