import { useEffect, useState } from "react";

import {
  Box,
  Button,
  Card,
  CircularProgress,
  IconButton,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import ScienceOutlinedIcon from "@mui/icons-material/ScienceOutlined";
import SearchIcon from "@mui/icons-material/Search";

import { useNavigate } from "react-router-dom";

import { getPendingLabOrders } from "../../services/laboratoryApi";

import LabStatusChip from "../../components/ui/LabStatusChip";

export default function PendingLabOrders() {
  const navigate = useNavigate();

  const [orders, setOrders] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const loadOrders = async () => {
    try {
      setLoading(true);

      const response = await getPendingLabOrders();

      setOrders(Array.isArray(response) ? response : response?.data || []);
    } catch (error) {
      console.error(error);

      alert("Unable to load pending laboratory orders.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOrders();
  }, []);

  const filteredOrders = orders.filter((order) => {
    const text = `
        ${order.patient_id || ""}
        ${order.test_name || ""}
        ${order.test_code || ""}
        ${order.service_request_id || ""}
      `.toLowerCase();

    return text.includes(search.toLowerCase());
  });

  return (
    <Box sx={{ p: 3 }}>
      <Stack
        direction={{
          xs: "column",
          md: "row",
        }}
        justifyContent="space-between"
        alignItems={{
          xs: "flex-start",
          md: "center",
        }}
        gap={2}
        mb={3}
      >
        <Box>
          <Typography variant="h4" fontWeight={700}>
            Pending Laboratory Orders
          </Typography>

          <Typography color="text.secondary">
            Orders waiting for laboratory processing
          </Typography>
        </Box>

        <Button variant="outlined" onClick={loadOrders}>
          Refresh
        </Button>
      </Stack>

      <TextField
        fullWidth
        placeholder="Search by patient, test or ServiceRequest..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        InputProps={{
          startAdornment: (
            <SearchIcon
              sx={{
                mr: 1,
                color: "text.secondary",
              }}
            />
          ),
        }}
        sx={{ mb: 3 }}
      />

      {loading ? (
        <Box display="flex" justifyContent="center" py={10}>
          <CircularProgress />
        </Box>
      ) : filteredOrders.length === 0 ? (
        <Card
          sx={{
            p: 8,
            textAlign: "center",
          }}
        >
          <ScienceOutlinedIcon
            sx={{
              fontSize: 50,
              color: "text.secondary",
            }}
          />

          <Typography variant="h6" mt={2}>
            No pending orders
          </Typography>

          <Typography color="text.secondary">
            All laboratory orders have been processed.
          </Typography>
        </Card>
      ) : (
        <Card
          sx={{
            borderRadius: 3,
            overflow: "hidden",
          }}
        >
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
                  <th style={thStyle}>Patient</th>

                  <th style={thStyle}>Test</th>

                  <th style={thStyle}>Priority</th>

                  <th style={thStyle}>Status</th>

                  <th style={thStyle}>Service Request</th>

                  <th style={thStyle}>Action</th>
                </tr>
              </thead>

              <tbody>
                {filteredOrders.map((order) => (
                  <tr key={order.id}>
                    <td style={tdStyle}>{order.patient_id}</td>

                    <td style={tdStyle}>
                      {order.test_name || order.test_code || "-"}
                    </td>

                    <td style={tdStyle}>{order.priority || "-"}</td>

                    <td style={tdStyle}>
                      <LabStatusChip status={order.status} />
                    </td>

                    <td style={tdStyle}>{order.service_request_id || "-"}</td>

                    <td style={tdStyle}>
                      <Stack direction="row" spacing={1}>
                        <IconButton
                          title="View"
                          onClick={() => console.log(order)}
                        >
                          <VisibilityOutlinedIcon />
                        </IconButton>

                        <Button
                          size="small"
                          variant="contained"
                          onClick={() =>
                            navigate(
                              `/laboratory/results/${encodeURIComponent(
                                order.service_request_id,
                              )}`,
                            )
                          }
                        >
                          Enter Results
                        </Button>
                      </Stack>
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
  borderBottom: "1px solid #E2E8F0",
  fontWeight: 600,
};

const tdStyle = {
  padding: "14px 16px",
  borderBottom: "1px solid #E2E8F0",
};
