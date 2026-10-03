import React, { useEffect, useState } from "react";

import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import PersonIcon from "@mui/icons-material/Person";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import DeleteIcon from "@mui/icons-material/Delete";
import RefreshIcon from "@mui/icons-material/Refresh";
import Sidebar from "../../components/layout/Sidebar";
import Header from "../../components/layout/Header";
import DataTable from "../../components/ui/DataTable";
import { useNavigate } from "react-router-dom";

import {
  getPatient,
  getAllPatients,
  deletePatient,
} from "../../services/patientService";

export default function Patients() {
  const [patientId, setPatientId] = useState("");
  const [rows, setRows] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate();

  // =====================================================
  // CONVERT ALL-PATIENT API DATA
  // =====================================================

  const convertAllPatientToRow = (patient) => {
    return {
      id: patient.id,
      patient_id: patient.id,
      name: patient.name || "-",
      gender: patient.gender || "-",
      birth_date: patient.birth_date || "-",
      active: patient.active ?? false,
      originalPatient: patient,
    };
  };

  // =====================================================
  // CONVERT SINGLE FHIR PATIENT DATA
  // =====================================================

  const convertFHIRPatientToRow = (patient) => {
    const nameData = patient.name?.[0];

    const givenName = nameData?.given?.join(" ") || "";
    const familyName = nameData?.family || "";

    const fullName = `${givenName} ${familyName}`.trim();

    return {
      id: patient.id,
      patient_id: patient.id,
      name: fullName || "-",
      gender: patient.gender || "-",
      birth_date: patient.birthDate || "-",
      active: patient.active ?? false,
      originalPatient: patient,
    };
  };

  // =====================================================
  // TABLE COLUMNS
  // =====================================================

  const columns = [
    {
      field: "patient_id",
      headerName: "Patient ID",
      minWidth: 130,
    },

    {
      field: "name",
      headerName: "Name",
      minWidth: 180,
    },

    {
      field: "gender",
      headerName: "Gender",
      minWidth: 100,
    },

    {
      field: "birth_date",
      headerName: "Date of Birth",
      minWidth: 150,
    },

    {
      field: "active",
      headerName: "Status",
      minWidth: 100,

      render: (row) => (
        <Typography
          sx={{
            color: row.active ? "success.main" : "error.main",
            fontWeight: 600,
          }}
        >
          {row.active ? "Active" : "Inactive"}
        </Typography>
      ),
    },

    {
      field: "actions",
      headerName: "Actions",
      sortable: false,
      minWidth: 180,

      render: (row) => (
        <Stack direction="row" spacing={1}>
          <Button
            size="small"
            variant="outlined"
            startIcon={<VisibilityOutlinedIcon />}
            onClick={(event) => {
              event.stopPropagation();
              handleViewPatient(row);
            }}
          >
            View
          </Button>

          <Button
            size="small"
            color="error"
            variant="outlined"
            startIcon={<DeleteIcon />}
            onClick={(event) => {
              event.stopPropagation();
              handleDeletePatient(row);
            }}
          >
            Delete
          </Button>
        </Stack>
      ),
    },
  ];

  // =====================================================
  // LOAD ALL PATIENTS
  // =====================================================

  const loadAllPatients = async () => {
    try {
      setLoading(true);
      setError("");
      setSuccess("");

      const response = await getAllPatients();

      console.log("All patients response:", response);

      const patientRows = (response?.patients || []).map(
        convertAllPatientToRow,
      );

      setRows(patientRows);
    } catch (err) {
      console.error("Get all patients error:", err);

      setRows([]);

      setError(err.response?.data?.detail || "Unable to fetch patients.");
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // LOAD ALL PATIENTS ON PAGE LOAD
  // =====================================================

  useEffect(() => {
    loadAllPatients();
  }, []);

  // =====================================================
  // SEARCH PATIENT
  // =====================================================

  const handleSearch = async () => {
    const id = patientId.trim();

    // Empty search = show all patients
    if (!id) {
      loadAllPatients();
      return;
    }

    try {
      setLoading(true);
      setError("");
      setSuccess("");

      const patient = await getPatient(id);

      console.log("Single patient response:", patient);

      const row = convertFHIRPatientToRow(patient);

      setRows([row]);
    } catch (err) {
      console.error("Get patient error:", err);

      setRows([]);

      setError(err.response?.data?.detail || "Patient not found.");
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // VIEW PATIENT
  // =====================================================

  const handleViewPatient = (row) => {
    console.log("Selected patient:", row.originalPatient);

    navigate(`/patients/${row.patient_id}`);
  };

  // =====================================================
  // DELETE PATIENT
  // =====================================================

  const handleDeletePatient = async (row) => {
    const id = row.patient_id;

    const confirmed = window.confirm(
      `Are you sure you want to delete patient ${id}?`,
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setSuccess("");

      await deletePatient(id);

      setRows((previousRows) =>
        previousRows.filter((item) => item.patient_id !== id),
      );

      setSuccess(`Patient ${id} deleted successfully.`);
    } catch (err) {
      console.error("Delete patient error:", err);

      setError(err.response?.data?.detail || "Unable to delete patient.");
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
        display: "grid",
        gridTemplateColumns: "280px 1fr",
        minHeight: "100vh",
        bgcolor: "#f5f7fb",
      }}
    >
      {/* Sidebar - fixed column width, part of grid flow (not position:fixed) */}
      <Box
        component="aside"
        sx={{
          gridColumn: "1",
          position: "sticky",
          top: 0,
          height: "100vh",
          overflowY: "auto",
          zIndex: 10,
        }}
      >
        <Sidebar />
      </Box>

      {/* Main Content */}
      <Box
        sx={{
          gridColumn: "2",
          display: "flex",
          flexDirection: "column",
          minWidth: 0, // prevents content from pushing grid wider than 1fr
        }}
      >
        {/* Header */}
        <Header />
        <Box sx={{ p: 3 }}>
          {/* =================================================
          HEADER
      ================================================= */}

          <Stack direction="row" spacing={1.5} alignItems="center" mb={1}>
            <PersonIcon
              sx={{
                fontSize: 34,
                color: "primary.main",
              }}
            />

            <Typography variant="h4" fontWeight={700}>
              Patients
            </Typography>
          </Stack>

          <Typography color="text.secondary" mb={3}>
            View and manage patient information.
          </Typography>

          {/* =================================================
          SEARCH CARD
      ================================================= */}

          <Card
            sx={{
              mb: 3,
              borderRadius: 3,
            }}
          >
            <CardContent>
              <Typography variant="h6" fontWeight={700} mb={2}>
                Find Patient
              </Typography>

              <Stack
                direction={{
                  xs: "column",
                  sm: "row",
                }}
                spacing={2}
              >
                <TextField
                  fullWidth
                  label="Patient ID"
                  placeholder="Enter patient ID"
                  value={patientId}
                  onChange={(event) => setPatientId(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter") {
                      handleSearch();
                    }
                  }}
                />

                <Button
                  variant="contained"
                  startIcon={<SearchIcon />}
                  onClick={handleSearch}
                  disabled={loading}
                  sx={{
                    minWidth: 140,
                  }}
                >
                  Search
                </Button>

                <Button
                  variant="outlined"
                  startIcon={<RefreshIcon />}
                  onClick={loadAllPatients}
                  disabled={loading}
                  sx={{
                    minWidth: 140,
                  }}
                >
                  Show All
                </Button>
              </Stack>
            </CardContent>
          </Card>

          {/* =================================================
          ALERTS
      ================================================= */}

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mb: 3 }}>
              {success}
            </Alert>
          )}

          {/* =================================================
          PATIENT TABLE
      ================================================= */}

          <Card
            sx={{
              borderRadius: 3,
            }}
          >
            <CardContent>
              <Stack
                direction="row"
                justifyContent="space-between"
                alignItems="center"
                mb={2}
              >
                <Box>
                  <Typography variant="h6" fontWeight={700}>
                    Patient Information
                  </Typography>

                  <Typography variant="body2" color="text.secondary">
                    {rows.length} patient
                    {rows.length !== 1 ? "s" : ""}
                  </Typography>
                </Box>
              </Stack>

              <DataTable
                columns={columns}
                rows={rows}
                loading={loading}
                selectable={false}
                striped={true}
                stickyHeader={true}
                dense={false}
                rowKey="id"
                onRowClick={(row) => {
                  handleViewPatient(row);
                }}
              />
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Box>
  );
}
