import React from "react";

import {
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  Stack,
  Typography,
} from "@mui/material";

export default function AppointmentConfirmation({
  data,
  onConfirm,
  loading = false,
}) {
  if (!data) {
    return null;
  }

  const patient = data.patient || {};
  const practitioner = data.practitioner || {};

  const start = data.start || "";
  const end = data.end || "";

  return (
    <Card
      elevation={0}
      sx={{
        mt: 2,
        border: "1px solid",
        borderColor: "divider",
        borderRadius: 3,
        maxWidth: 520,
      }}
    >
      <CardContent>
        <Typography variant="h6" fontWeight={700} sx={{ mb: 1 }}>
          Appointment Confirmation
        </Typography>

        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          {data.message || "Please review the appointment details."}
        </Typography>

        {/* Patient */}

        <Box sx={{ mb: 2 }}>
          <Typography variant="caption" color="text.secondary">
            Patient
          </Typography>

          <Typography variant="body1" fontWeight={600}>
            {patient.name || "Unknown"}
          </Typography>

          {patient.id && (
            <Typography variant="body2" color="text.secondary">
              Patient ID: {patient.id}
            </Typography>
          )}
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Practitioner */}

        <Box sx={{ mb: 2 }}>
          <Typography variant="caption" color="text.secondary">
            Practitioner
          </Typography>

          <Typography variant="body1" fontWeight={600}>
            {practitioner.name || "Unknown"}
          </Typography>

          {practitioner.id && (
            <Typography variant="body2" color="text.secondary">
              Practitioner ID: {practitioner.id}
            </Typography>
          )}
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Date and Time */}

        <Stack spacing={1.5}>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Start
            </Typography>

            <Typography variant="body2">{start}</Typography>
          </Box>

          <Box>
            <Typography variant="caption" color="text.secondary">
              End
            </Typography>

            <Typography variant="body2">{end}</Typography>
          </Box>

          <Box>
            <Typography variant="caption" color="text.secondary">
              Reason
            </Typography>

            <Typography variant="body2">
              {data.reason || "General Consultation"}
            </Typography>
          </Box>
        </Stack>

        {/* Buttons */}

        <Stack direction="row" spacing={2} sx={{ mt: 3 }}>
          <Button
            variant="outlined"
            color="inherit"
            fullWidth
            disabled={loading}
            onClick={() => onConfirm(false)}
          >
            Cancel
          </Button>

          <Button
            variant="contained"
            fullWidth
            disabled={loading}
            onClick={() => onConfirm(true)}
          >
            {loading ? "Confirming..." : "Confirm Appointment"}
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
}
