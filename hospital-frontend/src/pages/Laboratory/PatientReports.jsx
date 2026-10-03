import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, Card, Stack, TextField, Typography } from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";

import { getPatientReports } from "../../services/laboratoryApi";

export default function PatientReports() {
  const navigate = useNavigate();
  const [patientId, setPatientId] = useState("");

  const [reports, setReports] = useState([]);

  const searchReports = async () => {
    if (!patientId.trim()) {
      alert("Enter patient ID.");
      return;
    }

    try {
      const response = await getPatientReports(patientId);

      console.log("Patient Reports Bundle:", response);

      const reportList = Array.isArray(response?.entry)
        ? response.entry
            .map((entry) => entry.resource)
            .filter((resource) => resource?.resourceType === "DiagnosticReport")
        : [];

      console.log("Reports:", reportList);

      setReports(reportList);
    } catch (error) {
      console.error(error);

      alert(error.response?.data?.detail || "Unable to load reports.");
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" fontWeight={700} mb={3}>
        Patient Reports
      </Typography>

      <Card
        sx={{
          p: 3,
          mb: 3,
        }}
      >
        <Stack
          direction={{
            xs: "column",
            md: "row",
          }}
          spacing={2}
        >
          <TextField
            fullWidth
            label="Patient ID"
            value={patientId}
            onChange={(e) => setPatientId(e.target.value)}
          />

          <Button
            variant="contained"
            startIcon={<SearchIcon />}
            onClick={searchReports}
          >
            Search
          </Button>
        </Stack>
      </Card>

      <Stack spacing={2}>
        {reports.map((report) => (
          <Card
            key={report.id}
            sx={{
              p: 3,
              cursor: "pointer",
              "&:hover": {
                boxShadow: 4,
              },
            }}
            onClick={() =>
              navigate(`/laboratory/reports/${encodeURIComponent(report.id)}`)
            }
          >
            <Typography variant="h6" fontWeight={700}>
              {report.code?.text || "Diagnostic Report"}
            </Typography>

            <Typography color="text.secondary">
              Report ID: {report.id || "-"}
            </Typography>

            <Typography>Status: {report.status || "-"}</Typography>

            <Typography>Patient: {report.subject?.reference || "-"}</Typography>

            <Typography>
              Report Date:{" "}
              {report.meta?.lastUpdated
                ? new Date(report.meta.lastUpdated).toLocaleString()
                : "-"}
            </Typography>

            <Typography
              sx={{
                mt: 1,
                color: "primary.main",
              }}
            >
              View Full Report →
            </Typography>
          </Card>
        ))}
      </Stack>
    </Box>
  );
}
