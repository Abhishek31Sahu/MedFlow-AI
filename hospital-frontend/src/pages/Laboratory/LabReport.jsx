import React, { useEffect, useState } from "react";
import {
  Box,
  CircularProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import { useParams } from "react-router-dom";

import { getLabReport, getObservation } from "../../services/laboratoryApi";

const LabReport = () => {
  const { reportId } = useParams();

  const [report, setReport] = useState(null);
  const [observations, setObservations] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadReport();
  }, [reportId]);

  const loadReport = async () => {
    try {
      setLoading(true);
      setError("");

      // 1. Get DiagnosticReport
      const reportData = await getLabReport(reportId);

      console.log("DiagnosticReport:", reportData);

      setReport(reportData);

      // 2. Make sure result exists
      if (!Array.isArray(reportData.result) || reportData.result.length === 0) {
        setObservations([]);
        return;
      }

      // 3. Extract Observation IDs
      const observationPromises = reportData.result.map(async (result) => {
        const reference = result.reference;

        // "Observation/1251" -> "1251"
        const observationId = reference.split("/")[1];

        console.log("Fetching Observation:", observationId);

        return getObservation(observationId);
      });

      // 4. Fetch all observations
      const observationData = await Promise.all(observationPromises);

      console.log("All Observations:", observationData);

      setObservations(observationData);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail || "Failed to load laboratory report",
      );
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          mt: 5,
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Typography color="error" sx={{ p: 3 }}>
        {error}
      </Typography>
    );
  }

  if (!report) {
    return <Typography sx={{ p: 3 }}>Laboratory report not found.</Typography>;
  }

  return (
    <Box sx={{ maxWidth: 1100, mx: "auto", p: 3 }}>
      {/* =========================
          REPORT DETAILS
      ========================= */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Laboratory Report
        </Typography>

        <Typography>Report ID: {report.id}</Typography>

        <Typography>Test: {report.code?.text || "-"}</Typography>

        <Typography>Status: {report.status || "-"}</Typography>

        <Typography>Patient: {report.subject?.reference || "-"}</Typography>

        <Typography>Encounter: {report.encounter?.reference || "-"}</Typography>

        <Typography>
          Technician: {report.performer?.[0]?.reference || "-"}
        </Typography>
      </Paper>

      {/* =========================
          RESULTS
      ========================= */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Test Results
        </Typography>

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Parameter</TableCell>

                <TableCell>Result</TableCell>

                <TableCell>Unit</TableCell>

                <TableCell>Reference Range</TableCell>

                <TableCell>Interpretation</TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {observations.map((observation) => {
                const resultValue =
                  observation.valueQuantity?.value ??
                  observation.valueString ??
                  "-";

                const unit = observation.valueQuantity?.unit ?? "-";

                const referenceRange =
                  observation.referenceRange?.[0]?.text ?? "-";

                const interpretation =
                  observation.interpretation?.[0]?.coding?.[0]?.code ?? "-";

                return (
                  <TableRow key={observation.id}>
                    <TableCell>{observation.code?.text || "-"}</TableCell>

                    <TableCell>{resultValue}</TableCell>

                    <TableCell>{unit}</TableCell>

                    <TableCell>{referenceRange}</TableCell>

                    <TableCell>{interpretation}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
};

export default LabReport;
