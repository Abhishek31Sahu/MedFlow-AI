import React, { useEffect, useMemo, useState } from "react";

import {
  Alert,
  Box,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Grid,
  InputAdornment,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import LocalHospitalIcon from "@mui/icons-material/LocalHospital";

import Sidebar from "../../components/layout/Sidebar";
import Header from "../../components/layout/Header";
import DataTable from "../../components/ui/DataTable";

import api from "../../api/axios";

export default function EncounterDashboard() {
  const [encounters, setEncounters] = useState([]);
  const [search, setSearch] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // =====================================================
  // LOAD ENCOUNTERS
  // =====================================================

  const loadEncounters = async () => {
    try {
      setLoading(true);
      setError("");

      // Change this endpoint if your actual encounter
      // listing endpoint is different.
      const response = await api.get("/encounters");

      console.log("Encounter response:", response.data);

      const data = response.data;

      // Supports either:
      // { encounters: [...] }
      // OR directly [...]
      const encounterList = Array.isArray(data) ? data : data?.encounters || [];

      setEncounters(encounterList);
    } catch (err) {
      console.error("Encounter fetch error:", err);

      setError(err.response?.data?.detail || "Unable to load encounters.");
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // LOAD WHEN PAGE OPENS
  // =====================================================

  useEffect(() => {
    loadEncounters();
  }, []);

  // =====================================================
  // SEARCH
  // =====================================================

  const filteredEncounters = useMemo(() => {
    const value = search.trim().toLowerCase();

    if (!value) {
      return encounters;
    }

    return encounters.filter((encounter) => {
      return (
        String(encounter.id || "")
          .toLowerCase()
          .includes(value) ||
        String(encounter.patient_id || "")
          .toLowerCase()
          .includes(value) ||
        String(encounter.practitioner_id || "")
          .toLowerCase()
          .includes(value) ||
        String(encounter.status || "")
          .toLowerCase()
          .includes(value) ||
        String(encounter.location_id || "")
          .toLowerCase()
          .includes(value)
      );
    });
  }, [encounters, search]);

  // =====================================================
  // STATUS COUNTS
  // =====================================================

  const activeCount = useMemo(() => {
    return encounters.filter(
      (encounter) => String(encounter.status || "").toLowerCase() === "active",
    ).length;
  }, [encounters]);

  const completedCount = useMemo(() => {
    return encounters.filter(
      (encounter) =>
        String(encounter.status || "").toLowerCase() === "finished" ||
        String(encounter.status || "").toLowerCase() === "completed",
    ).length;
  }, [encounters]);

  // =====================================================
  // TABLE COLUMNS
  // =====================================================

  const columns = [
    {
      field: "id",
      headerName: "Encounter ID",
      minWidth: 150,
    },

    {
      field: "patient_id",
      headerName: "Patient",
      minWidth: 140,
    },

    {
      field: "practitioner_id",
      headerName: "Practitioner",
      minWidth: 140,

      render: (row) => row.practitioner_id || "-",
    },

    {
      field: "status",
      headerName: "Status",
      minWidth: 130,

      render: (row) => {
        const status = String(row.status || "unknown").toLowerCase();

        let color = "default";

        if (status === "active") {
          color = "success";
        } else if (status === "finished" || status === "completed") {
          color = "primary";
        } else if (status === "cancelled") {
          color = "error";
        }

        return (
          <Chip
            label={status.charAt(0).toUpperCase() + status.slice(1)}
            color={color}
            size="small"
          />
        );
      },
    },

    {
      field: "location_id",
      headerName: "Location",
      minWidth: 140,

      render: (row) => row.location_id || "-",
    },

    {
      field: "encounter_type",
      headerName: "Type",
      minWidth: 140,

      render: (row) => row.encounter_type || "-",
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

        {/* =================================================
            CONTENT
        ================================================= */}

        <Box
          component="main"
          sx={{
            p: {
              xs: 2,
              sm: 3,
              lg: 4,
            },

            overflow: "auto",
          }}
        >
          {/* =================================================
              PAGE HEADER
          ================================================= */}

          <Box sx={{ mb: 4 }}>
            <Stack
              direction="row"
              spacing={1.5}
              alignItems="center"
              sx={{ mb: 1 }}
            >
              <Box
                sx={{
                  width: 48,
                  height: 48,
                  borderRadius: 3,

                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",

                  backgroundColor: "#E3F2FD",

                  color: "#1976D2",
                }}
              >
                <LocalHospitalIcon />
              </Box>

              <Box>
                <Typography variant="h4" fontWeight={700}>
                  Encounter Overview
                </Typography>

                <Typography variant="body2" color="text.secondary">
                  Manage and monitor patient encounters.
                </Typography>
              </Box>
            </Stack>
          </Box>

          {/* =================================================
              SUMMARY CARDS
          ================================================= */}

          <Grid container spacing={3} sx={{ mb: 3 }}>
            {/* Total */}

            <Grid
              size={{
                xs: 12,
                sm: 6,
                md: 4,
              }}
            >
              <Card
                sx={{
                  borderRadius: 4,

                  border: "1px solid #E5E7EB",
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="body2" color="text.secondary">
                    Total Encounters
                  </Typography>

                  <Typography
                    variant="h3"
                    fontWeight={800}
                    color="primary.main"
                  >
                    {encounters.length}
                  </Typography>

                  <Typography variant="caption" color="text.secondary">
                    Patient encounters
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Active */}

            <Grid
              size={{
                xs: 12,
                sm: 6,
                md: 4,
              }}
            >
              <Card
                sx={{
                  borderRadius: 4,

                  border: "1px solid #E5E7EB",
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="body2" color="text.secondary">
                    Active Encounters
                  </Typography>

                  <Typography
                    variant="h3"
                    fontWeight={800}
                    color="success.main"
                  >
                    {activeCount}
                  </Typography>

                  <Typography variant="caption" color="text.secondary">
                    Currently active
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Completed */}

            <Grid
              size={{
                xs: 12,
                sm: 6,
                md: 4,
              }}
            >
              <Card
                sx={{
                  borderRadius: 4,

                  border: "1px solid #E5E7EB",
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="body2" color="text.secondary">
                    Completed
                  </Typography>

                  <Typography
                    variant="h3"
                    fontWeight={800}
                    color="warning.main"
                  >
                    {completedCount}
                  </Typography>

                  <Typography variant="caption" color="text.secondary">
                    Finished encounters
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* =================================================
              SEARCH
          ================================================= */}

          <Card
            sx={{
              mb: 3,
              borderRadius: 4,

              border: "1px solid #E5E7EB",
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <TextField
                fullWidth
                label="Search encounters"
                placeholder="Search by patient, encounter, practitioner or status"
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
            <Alert
              severity="error"
              sx={{
                mb: 3,
                borderRadius: 3,
              }}
            >
              {error}
            </Alert>
          )}

          {/* =================================================
              TABLE
          ================================================= */}

          <Card
            sx={{
              borderRadius: 4,

              border: "1px solid #E5E7EB",
            }}
          >
            <CardContent sx={{ p: 3 }}>
              <Stack
                direction={{
                  xs: "column",
                  sm: "row",
                }}
                justifyContent="space-between"
                alignItems={{
                  xs: "flex-start",
                  sm: "center",
                }}
                spacing={1}
                sx={{ mb: 2 }}
              >
                <Box>
                  <Typography variant="h6" fontWeight={700}>
                    Patient Encounters
                  </Typography>

                  <Typography variant="body2" color="text.secondary">
                    Showing {filteredEncounters.length} of {encounters.length}
                  </Typography>
                </Box>

                <Chip
                  label={`${encounters.length} Encounters`}
                  variant="outlined"
                  color="primary"
                />
              </Stack>

              {loading ? (
                <Box
                  sx={{
                    minHeight: 300,

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
                  rows={filteredEncounters}
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
