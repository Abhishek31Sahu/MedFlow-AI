import { useState } from "react";

import { Box, Button, Card, Stack, TextField, Typography } from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";

import { getPatientLabOrders } from "../../services/laboratoryApi";

import LabStatusChip from "../../components/ui/LabStatusChip";

export default function PatientLabOrders() {
  const [patientId, setPatientId] = useState("");

  const [orders, setOrders] = useState([]);

  const [loading, setLoading] = useState(false);

  const searchOrders = async () => {
    if (!patientId.trim()) {
      alert("Enter patient ID.");
      return;
    }

    try {
      setLoading(true);

      const response = await getPatientLabOrders(patientId.trim());

      setOrders(Array.isArray(response) ? response : response?.data || []);
    } catch (error) {
      console.error(error);

      alert(error.response?.data?.detail || "Unable to load patient orders.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" fontWeight={700} mb={0.5}>
        Patient Laboratory Orders
      </Typography>

      <Typography color="text.secondary" mb={3}>
        View laboratory orders for a patient.
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
            placeholder="Enter Patient ID"
            value={patientId}
            onChange={(e) => setPatientId(e.target.value)}
          />

          <Button
            variant="contained"
            startIcon={<SearchIcon />}
            onClick={searchOrders}
            disabled={loading}
          >
            Search
          </Button>
        </Stack>
      </Card>

      {orders.length > 0 && (
        <Card>
          <Box
            sx={{
              overflowX: "auto",
            }}
          >
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
              }}
            >
              <thead>
                <tr>
                  <th style={thStyle}>Test</th>

                  <th style={thStyle}>Priority</th>

                  <th style={thStyle}>Status</th>

                  <th style={thStyle}>Service Request</th>

                  <th style={thStyle}>Ordered At</th>
                </tr>
              </thead>

              <tbody>
                {orders.map((order) => (
                  <tr key={order.id}>
                    <td style={tdStyle}>
                      {order.test_name || order.test_code || "-"}
                    </td>

                    <td style={tdStyle}>{order.priority || "-"}</td>

                    <td style={tdStyle}>
                      <LabStatusChip status={order.status} />
                    </td>

                    <td style={tdStyle}>{order.service_request_id || "-"}</td>

                    <td style={tdStyle}>
                      {order.ordered_at
                        ? new Date(order.ordered_at).toLocaleString()
                        : "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Box>
        </Card>
      )}
    </Box>
  );
}

const thStyle = {
  textAlign: "left",
  padding: "14px 16px",
  background: "#F8FAFC",
};

const tdStyle = {
  padding: "14px 16px",
  borderBottom: "1px solid #E2E8F0",
};
