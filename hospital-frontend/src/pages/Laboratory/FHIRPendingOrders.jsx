import { useEffect, useState } from "react";

import { Box, Card, CircularProgress, Typography } from "@mui/material";

import { getPendingFHIROrders } from "../../services/laboratoryApi";

export default function FHIRPendingOrders() {
  const [orders, setOrders] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const response = await getPendingFHIROrders();

        setOrders(Array.isArray(response) ? response : response?.data || []);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" fontWeight={700} mb={0.5}>
        Pending FHIR Orders
      </Typography>

      <Typography color="text.secondary" mb={3}>
        ServiceRequests currently pending on the FHIR server.
      </Typography>

      {loading ? (
        <Box display="flex" justifyContent="center" py={10}>
          <CircularProgress />
        </Box>
      ) : (
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
                  <th style={thStyle}>ID</th>

                  <th style={thStyle}>Patient</th>

                  <th style={thStyle}>Code</th>

                  <th style={thStyle}>Status</th>

                  <th style={thStyle}>Priority</th>
                </tr>
              </thead>

              <tbody>
                {orders.map((order) => (
                  <tr key={order.id}>
                    <td style={tdStyle}>{order.id}</td>

                    <td style={tdStyle}>{order.subject?.reference || "-"}</td>

                    <td style={tdStyle}>
                      {order.code?.text ||
                        order.code?.coding?.[0]?.display ||
                        "-"}
                    </td>

                    <td style={tdStyle}>{order.status || "-"}</td>

                    <td style={tdStyle}>{order.priority || "-"}</td>
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
  padding: "14px 16px",
  textAlign: "left",
  background: "#F8FAFC",
};

const tdStyle = {
  padding: "14px 16px",
  borderBottom: "1px solid #E2E8F0",
};
