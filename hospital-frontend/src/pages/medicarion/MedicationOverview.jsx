import React, { useEffect, useMemo, useState } from "react";

import {
  Alert,
  Box,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  InputAdornment,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import MedicationIcon from "@mui/icons-material/Medication";
import SearchIcon from "@mui/icons-material/Search";

import DataTable from "../../components/ui/DataTable";
import Sidebar from "../../components/layout/Sidebar";
import Header from "../../components/layout/Header";
import { getAllActiveMedications } from "../../services/medicationService";

export default function MedicationOverview() {
  const [medications, setMedications] = useState([]);
  const [search, setSearch] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // =====================================================
  // LOAD MEDICATIONS
  // =====================================================

  const loadMedications = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getAllActiveMedications();

      console.log("Medication response:", response);

      setMedications(response?.medications || []);
    } catch (err) {
      console.error("Medication fetch error:", err);

      setError(err.response?.data?.detail || "Unable to load medications.");
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // LOAD WHEN PAGE OPENS
  // =====================================================

  useEffect(() => {
    loadMedications();
  }, []);

  // =====================================================
  // SEARCH
  // =====================================================

  const filteredMedications = useMemo(() => {
    const value = search.trim().toLowerCase();

    if (!value) {
      return medications;
    }

    return medications.filter((medication) => {
      return (
        medication.patient_id?.toLowerCase().includes(value) ||
        medication.medicine?.toLowerCase().includes(value)
      );
    });
  }, [medications, search]);

  // =====================================================
  // TABLE COLUMNS
  // =====================================================

  const columns = [
    {
      field: "patient_id",
      headerName: "Patient",
      minWidth: 130,
    },

    {
      field: "medicine",
      headerName: "Medicine",
      minWidth: 180,
    },

    {
      field: "dosage",
      headerName: "Dosage",
      minWidth: 200,
    },

    {
      field: "status",
      headerName: "Status",
      minWidth: 120,

      render: (row) => (
        <Chip
          label={
            row.status
              ? row.status.charAt(0).toUpperCase() + row.status.slice(1)
              : "Unknown"
          }
          color={row.status === "active" ? "success" : "default"}
          size="small"
        />
      ),
    },
  ];

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
            <MedicationIcon
              sx={{
                fontSize: 34,
                color: "primary.main",
              }}
            />

            <Typography variant="h4" fontWeight={700}>
              Medication Overview
            </Typography>
          </Stack>

          <Typography color="text.secondary" sx={{ mb: 3 }}>
            Overview of active medications across patients.
          </Typography>

          {/* =================================================
          ACTIVE MEDICATION COUNT
      ================================================= */}

          <Card
            sx={{
              mb: 3,
              borderRadius: 3,
            }}
          >
            <CardContent>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                Active Medications
              </Typography>

              <Typography variant="h3" fontWeight={700} color="primary.main">
                {medications.length}
              </Typography>
            </CardContent>
          </Card>

          {/* =================================================
          SEARCH
      ================================================= */}

          <Card
            sx={{
              mb: 3,
              borderRadius: 3,
            }}
          >
            <CardContent>
              <TextField
                fullWidth
                label="Search patient / medicine"
                placeholder="Enter patient ID or medicine name"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
              />
            </CardContent>
          </Card>

          {/* =================================================
          ERROR
      ================================================= */}

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {/* =================================================
          TABLE
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
                    Active Medications
                  </Typography>

                  <Typography variant="body2" color="text.secondary">
                    Showing {filteredMedications.length} of {medications.length}{" "}
                    medications
                  </Typography>
                </Box>
              </Stack>

              {loading ? (
                <Box
                  sx={{
                    minHeight: 250,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <CircularProgress />
                </Box>
              ) : (
                <DataTable
                  columns={columns}
                  rows={filteredMedications}
                  loading={loading}
                  selectable={false}
                  striped={true}
                  stickyHeader={true}
                  dense={false}
                  rowKey="id"
                />
              )}
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Box>
  );
}
