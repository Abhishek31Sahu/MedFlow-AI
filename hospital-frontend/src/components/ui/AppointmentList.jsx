import React from "react";
import {
  Card,
  CardContent,
  Divider,
  Stack,
  Typography,
  Box,
} from "@mui/material";

export default function AppointmentList({ appointments = [] }) {
  if (!appointments.length) {
    return (
      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
        No appointments found.
      </Typography>
    );
  }

  return (
    <Stack spacing={2} sx={{ mt: 2 }}>
      {appointments.map((appointment) => (
        <Card
          key={appointment.id}
          variant="outlined"
          sx={{
            borderRadius: 2,
          }}
        >
          <CardContent>
            <Typography variant="subtitle1" fontWeight={700}>
              Appointment #{appointment.id}
            </Typography>

            <Divider sx={{ my: 1.5 }} />

            <Box sx={{ mb: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Status
              </Typography>
              <Typography variant="body2">
                {appointment.status || "N/A"}
              </Typography>
            </Box>

            <Box sx={{ mb: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Type
              </Typography>
              <Typography variant="body2">
                {appointment.appointmentType || "N/A"}
              </Typography>
            </Box>

            <Box sx={{ mb: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Reason
              </Typography>
              <Typography variant="body2">
                {appointment.reason || "N/A"}
              </Typography>
            </Box>

            <Box sx={{ mb: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Start
              </Typography>
              <Typography variant="body2">
                {appointment.start
                  ? new Date(appointment.start).toLocaleString()
                  : "N/A"}
              </Typography>
            </Box>

            <Box>
              <Typography variant="caption" color="text.secondary">
                End
              </Typography>
              <Typography variant="body2">
                {appointment.end
                  ? new Date(appointment.end).toLocaleString()
                  : "N/A"}
              </Typography>
            </Box>
          </CardContent>
        </Card>
      ))}
    </Stack>
  );
}
