import { useEffect, useState } from "react";

import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  Paper,
  Stack,
  Typography,
} from "@mui/material";
import Sidebar from "../../components/layout/Sidebar";
import Header from "../../components/layout/Header";
import AddCircleOutlineOutlinedIcon from "@mui/icons-material/AddCircleOutlineOutlined";
import PendingActionsOutlinedIcon from "@mui/icons-material/PendingActionsOutlined";
import ScienceOutlinedIcon from "@mui/icons-material/ScienceOutlined";
import AssessmentOutlinedIcon from "@mui/icons-material/AssessmentOutlined";
import CloudDoneOutlinedIcon from "@mui/icons-material/CloudDoneOutlined";
import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";
import AutoAwesomeOutlinedIcon from "@mui/icons-material/AutoAwesomeOutlined";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import BiotechOutlinedIcon from "@mui/icons-material/BiotechOutlined";

import { useNavigate } from "react-router-dom";

import {
  getPendingLabOrders,
  getPendingFHIROrders,
} from "../../services/laboratoryApi";

export default function LaboratoryDashboard() {
  const navigate = useNavigate();

  const [pendingOrders, setPendingOrders] = useState([]);
  const [pendingFHIR, setPendingFHIR] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);

      const [pendingResult, fhirResult] = await Promise.allSettled([
        getPendingLabOrders(),
        getPendingFHIROrders(),
      ]);

      if (pendingResult.status === "fulfilled") {
        const data = pendingResult.value;

        setPendingOrders(Array.isArray(data) ? data : data?.data || []);
      } else {
        console.error("Pending orders error:", pendingResult.reason);
        setPendingOrders([]);
      }

      if (fhirResult.status === "fulfilled") {
        const data = fhirResult.value;

        setPendingFHIR(Array.isArray(data) ? data : data?.data || []);
      } else {
        console.error("FHIR pending error:", fhirResult.reason);
        setPendingFHIR([]);
      }
    } catch (error) {
      console.error("Laboratory dashboard error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

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
        <Box
          sx={{
            minHeight: "100vh",
            bgcolor: "#f7f9fc",
            p: {
              xs: 2,
              md: 4,
            },
          }}
        >
          {/* =====================================================
          HEADER
      ===================================================== */}

          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: {
                xs: "flex-start",
                md: "center",
              },
              flexDirection: {
                xs: "column",
                md: "row",
              },
              gap: 2,
              mb: 4,
            }}
          >
            <Box>
              <Stack direction="row" alignItems="center" spacing={1.5}>
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: 2.5,
                    bgcolor: "#eaf3ff",
                    color: "#1976d2",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <BiotechOutlinedIcon fontSize="large" />
                </Box>

                <Box>
                  <Typography variant="h4" fontWeight={800}>
                    Laboratory Dashboard
                  </Typography>

                  <Typography color="text.secondary" sx={{ mt: 0.5 }}>
                    Manage laboratory orders, results and diagnostic reports.
                  </Typography>
                </Box>
              </Stack>
            </Box>

            <Typography color="text.secondary" fontSize={14}>
              {new Date().toLocaleDateString(undefined, {
                weekday: "long",
                day: "numeric",
                month: "long",
                year: "numeric",
              })}
            </Typography>
          </Box>

          {/* =====================================================
          STATISTICS
      ===================================================== */}

          <Grid container spacing={2.5} mb={4}>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                label="Pending Orders"
                value={loading ? "..." : pendingOrders.length}
                icon={<PendingActionsOutlinedIcon />}
                bg="#edf5ff"
                iconBg="#dcecff"
                onClick={() => navigate("/laboratory/orders/pending")}
                action="View Pending"
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                label="FHIR Pending"
                value={loading ? "..." : pendingFHIR.length}
                icon={<CloudDoneOutlinedIcon />}
                bg="#fff8e8"
                iconBg="#ffedbd"
                onClick={() => navigate("/laboratory/fhir/pending")}
                action="View Queue"
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                label="Lab Status"
                value="Active"
                icon={<ScienceOutlinedIcon />}
                bg="#edf9f3"
                iconBg="#d7f2e5"
                action="Operational"
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                label="Reporting"
                value="FHIR"
                icon={<AssessmentOutlinedIcon />}
                bg="#fff0f2"
                iconBg="#ffdfe4"
                action="Standardized"
              />
            </Grid>
          </Grid>

          {/* =====================================================
          QUICK ACTIONS
      ===================================================== */}

          <Typography variant="h6" fontWeight={800} mb={2}>
            Quick Actions
          </Typography>

          <Grid container spacing={2.5} mb={4}>
            <Grid item xs={12} sm={6} md={3}>
              <ActionCard
                icon={<AddCircleOutlineOutlinedIcon />}
                title="Create Lab Order"
                subtitle="Create a new test request"
                onClick={() => navigate("/laboratory/orders/create")}
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <ActionCard
                icon={<PendingActionsOutlinedIcon />}
                title="Enter Results"
                subtitle="Fill results for pending tests"
                onClick={() => navigate("/laboratory/orders/pending")}
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <ActionCard
                icon={<AssessmentOutlinedIcon />}
                title="Patient Reports"
                subtitle="Search completed reports"
                onClick={() => navigate("/laboratory/reports/patient")}
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <ActionCard
                icon={<DescriptionOutlinedIcon />}
                title="Manage Templates"
                subtitle="Configure laboratory tests"
                onClick={() => navigate("/laboratory/templates")}
              />
            </Grid>
          </Grid>

          {/* =====================================================
          RECENT ORDERS + ACTIVITY
      ===================================================== */}

          <Grid container spacing={3}>
            {/* Recent Orders */}

            <Grid item xs={12} md={8}>
              <Paper
                sx={{
                  borderRadius: 3,
                  overflow: "hidden",
                  height: "100%",
                  margin: "15px 0px",
                }}
              >
                <Box
                  sx={{
                    p: 2.5,
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <Box>
                    <Typography variant="h6" fontWeight={800}>
                      Recent Pending Orders
                    </Typography>

                    <Typography variant="body2" color="text.secondary">
                      Tests waiting for result entry
                    </Typography>
                  </Box>

                  <Button
                    size="small"
                    endIcon={<ArrowForwardIcon />}
                    onClick={() => navigate("/laboratory/orders/pending")}
                  >
                    View All
                  </Button>
                </Box>

                <Divider />

                {pendingOrders.length === 0 ? (
                  <Box sx={{ p: 5 }}>
                    <Typography textAlign="center" color="text.secondary">
                      No pending laboratory orders.
                    </Typography>
                  </Box>
                ) : (
                  <Box
                    sx={{
                      overflowX: "auto",
                    }}
                  >
                    <Box
                      component="table"
                      sx={{
                        width: "100%",
                        borderCollapse: "collapse",
                        minWidth: 650,

                        "& th": {
                          textAlign: "left",
                          p: 2,
                          bgcolor: "#f7f9fc",
                          fontSize: 13,
                          color: "text.secondary",
                        },

                        "& td": {
                          p: 2,
                          borderTop: "1px solid #edf0f4",
                          fontSize: 14,
                        },
                      }}
                    >
                      <thead>
                        <tr>
                          <th>Patient</th>
                          <th>Test</th>
                          <th>Status</th>
                          <th>Action</th>
                        </tr>
                      </thead>

                      <tbody>
                        {pendingOrders.slice(0, 5).map((order, index) => (
                          <tr key={order.id || index}>
                            <td>{order.patient_id || "-"}</td>

                            <td>{order.test_name || order.test_code || "-"}</td>

                            <td>
                              <Chip
                                label={order.status || "PENDING"}
                                size="small"
                                sx={{
                                  bgcolor: "#fff1ce",
                                  color: "#8a6200",
                                  fontWeight: 600,
                                }}
                              />
                            </td>

                            <td>
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
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </Box>
                  </Box>
                )}
              </Paper>
            </Grid>

            {/* Activity */}

            <Grid item xs={12} md={4}>
              <Paper
                sx={{
                  p: 2.5,
                  borderRadius: 3,
                  height: "100%",
                  margin: "15px 0px",
                }}
              >
                <Typography variant="h6" fontWeight={800} mb={3}>
                  Laboratory Overview
                </Typography>

                <Stack spacing={2.5}>
                  <OverviewRow
                    icon={<PendingActionsOutlinedIcon />}
                    label="Pending Orders"
                    value={loading ? "..." : pendingOrders.length}
                  />

                  <Divider />

                  <OverviewRow
                    icon={<CloudDoneOutlinedIcon />}
                    label="FHIR Queue"
                    value={loading ? "..." : pendingFHIR.length}
                  />

                  <Divider />

                  <OverviewRow
                    icon={<DescriptionOutlinedIcon />}
                    label="Workflow"
                    value="Active"
                  />

                  <Divider />

                  <OverviewRow
                    icon={<ScienceOutlinedIcon />}
                    label="Result Entry"
                    value="Template Based"
                  />
                </Stack>

                <Button
                  fullWidth
                  variant="outlined"
                  sx={{ mt: 4 }}
                  onClick={() => navigate("/laboratory/reports")}
                >
                  View Laboratory Reports
                </Button>
              </Paper>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Box>
  );
}

/* ============================================================
   STAT CARD
============================================================ */

function StatCard({ label, value, icon, bg, iconBg, onClick, action }) {
  return (
    <Card
      onClick={onClick}
      sx={{
        borderRadius: 3,
        bgcolor: bg,
        boxShadow: "none",
        border: "1px solid rgba(0,0,0,0.04)",
        cursor: onClick ? "pointer" : "default",
        transition: "0.2s",

        "&:hover": onClick
          ? {
              transform: "translateY(-2px)",
              boxShadow: 3,
            }
          : {},
      }}
    >
      <CardContent>
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Box>
            <Typography color="text.secondary" fontSize={14}>
              {label}
            </Typography>

            <Typography variant="h4" fontWeight={800} sx={{ mt: 0.5 }}>
              {value}
            </Typography>

            <Typography fontSize={13} color="primary" sx={{ mt: 0.5 }}>
              {action}
            </Typography>
          </Box>

          <Box
            sx={{
              width: 58,
              height: 58,
              borderRadius: "50%",
              bgcolor: iconBg,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "primary.main",
            }}
          >
            {icon}
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
}

/* ============================================================
   ACTION CARD
============================================================ */

function ActionCard({ icon, title, subtitle, onClick }) {
  return (
    <Card
      onClick={onClick}
      sx={{
        borderRadius: 3,
        height: "100%",
        cursor: "pointer",
        border: "1px solid #e5eaf0",
        transition: "0.2s",

        "&:hover": {
          transform: "translateY(-3px)",
          boxShadow: 4,
        },
      }}
    >
      <CardContent
        sx={{
          minHeight: 150,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
        }}
      >
        <Box
          sx={{
            width: 58,
            height: 58,
            borderRadius: "50%",
            bgcolor: "#eef5ff",
            color: "primary.main",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            mb: 1.5,
          }}
        >
          {icon}
        </Box>

        <Typography variant="h6" fontWeight={800}>
          {title}
        </Typography>

        <Typography color="text.secondary" fontSize={14} sx={{ mt: 0.5 }}>
          {subtitle}
        </Typography>

        <ArrowForwardIcon
          sx={{
            mt: 1.5,
            color: "primary.main",
            fontSize: 20,
          }}
        />
      </CardContent>
    </Card>
  );
}

/* ============================================================
   FEATURE CARD
============================================================ */

function FeatureCard({ icon, title, description, buttonText, onClick }) {
  return (
    <Card
      sx={{
        borderRadius: 3,
        height: "100%",
        border: "1px solid #e5eaf0",
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Stack direction="row" spacing={2} alignItems="flex-start">
          <Box
            sx={{
              width: 56,
              height: 56,
              flexShrink: 0,
              borderRadius: 2,
              bgcolor: "#eef5ff",
              color: "primary.main",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {icon}
          </Box>

          <Box sx={{ flex: 1 }}>
            <Typography variant="h6" fontWeight={800}>
              {title}
            </Typography>

            <Typography
              color="text.secondary"
              fontSize={14}
              sx={{
                mt: 1,
                lineHeight: 1.7,
              }}
            >
              {description}
            </Typography>

            <Button
              size="small"
              endIcon={<ArrowForwardIcon />}
              sx={{ mt: 1.5 }}
              onClick={onClick}
            >
              {buttonText}
            </Button>
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
}

/* ============================================================
   OVERVIEW ROW
============================================================ */

function OverviewRow({ icon, label, value }) {
  return (
    <Stack direction="row" alignItems="center" justifyContent="space-between">
      <Stack direction="row" alignItems="center" spacing={1.5}>
        <Box
          sx={{
            color: "primary.main",
            display: "flex",
          }}
        >
          {icon}
        </Box>

        <Typography fontWeight={600}>{label}</Typography>
      </Stack>

      <Typography fontWeight={700} color="text.secondary">
        {value}
      </Typography>
    </Stack>
  );
}
