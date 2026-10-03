import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";

import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  Box,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Divider,
  Grid,
  LinearProgress,
  Stack,
  Typography,
  Button,
  Avatar,
} from "@mui/material";

import PeopleIcon from "@mui/icons-material/People";
import AssignmentIcon from "@mui/icons-material/Assignment";
import DescriptionIcon from "@mui/icons-material/Description";
import VisibilityIcon from "@mui/icons-material/Visibility";
import MedicationIcon from "@mui/icons-material/Medication";
import BedIcon from "@mui/icons-material/Bed";
import ScienceIcon from "@mui/icons-material/Science";
import LocalHospitalIcon from "@mui/icons-material/LocalHospital";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import EventIcon from "@mui/icons-material/Event";
import LocalPharmacyIcon from "@mui/icons-material/LocalPharmacy";
import PendingActionsIcon from "@mui/icons-material/PendingActions";
import SettingsIcon from "@mui/icons-material/Settings";

import api from "../api/axios";

// ==========================================================
// ROLE INFORMATION
// ==========================================================

const roleInfo = {
  admin: {
    title: "Hospital Administrator",
    subtitle: "Hospital operations and system overview",
    greeting: "Welcome back",
  },

  doctor: {
    title: "Doctor Workspace",
    subtitle: "Clinical workflow and patient management",
    greeting: "Good to see you",
  },

  nurse: {
    title: "Nursing Dashboard",
    subtitle: "Patient care and ward operations",
    greeting: "Welcome back",
  },

  receptionist: {
    title: "Front Desk Dashboard",
    subtitle: "Patient and appointment operations",
    greeting: "Welcome back",
  },

  lab_technician: {
    title: "Laboratory Dashboard",
    subtitle: "Laboratory workflow and diagnostic processing",
    greeting: "Welcome back",
  },

  pharmacist: {
    title: "Pharmacy Dashboard",
    subtitle: "Medication and prescription management",
    greeting: "Welcome back",
  },
};

// ==========================================================
// ROLE QUICK ACTIONS
// ==========================================================

const roleActions = {
  admin: [
    {
      label: "Add Staff",
      description: "Create a hospital user",
      path: "/staff",
      icon: <PersonAddIcon />,
    },
    {
      label: "Manage Beds",
      description: "View hospital beds",
      path: "/beds",
      icon: <BedIcon />,
    },
    {
      label: "Laboratory",
      description: "Monitor laboratory workflow",
      path: "/laboratory",
      icon: <ScienceIcon />,
    },
    {
      label: "Patients",
      description: "Manage patient records",
      path: "/patients",
      icon: <PeopleIcon />,
    },
  ],

  doctor: [
    {
      label: "AI Assistant",
      description: "Start a clinical workflow",
      path: "/ai",
      icon: <SmartToyIcon />,
    },
    {
      label: "Patients",
      description: "View patient records",
      path: "/patients",
      icon: <PeopleIcon />,
    },
    {
      label: "Laboratory",
      description: "Order and review tests",
      path: "/laboratory",
      icon: <ScienceIcon />,
    },
    {
      label: "Beds",
      description: "Check bed availability",
      path: "/beds",
      icon: <BedIcon />,
    },
  ],

  nurse: [
    {
      label: "Patients",
      description: "View patient records",
      path: "/patients",
      icon: <PeopleIcon />,
    },
    {
      label: "Beds",
      description: "Monitor ward beds",
      path: "/beds",
      icon: <BedIcon />,
    },
    {
      label: "Encounters",
      description: "View patient encounters",
      path: "/encounters",
      icon: <LocalHospitalIcon />,
    },
    {
      label: "Medications",
      description: "Review medications",
      path: "/medications",
      icon: <MedicationIcon />,
    },
  ],

  receptionist: [
    {
      label: "Patients",
      description: "Register and manage patients",
      path: "/patients",
      icon: <PeopleIcon />,
    },
    {
      label: "Appointments",
      description: "Manage appointments",
      path: "/appointments",
      icon: <EventIcon />,
    },
    {
      label: "Encounters",
      description: "View encounters",
      path: "/encounters",
      icon: <LocalHospitalIcon />,
    },
  ],

  lab_technician: [
    {
      label: "Pending Orders",
      description: "Process laboratory orders",
      path: "/laboratory",
      icon: <PendingActionsIcon />,
    },
    {
      label: "Laboratory",
      description: "Manage lab workflow",
      path: "/laboratory",
      icon: <ScienceIcon />,
    },
    {
      label: "Templates",
      description: "Manage test templates",
      path: "/laboratory/templates",
      icon: <DescriptionIcon />,
    },
    {
      label: "Patients",
      description: "View patient records",
      path: "/patients",
      icon: <PeopleIcon />,
    },
  ],

  pharmacist: [
    {
      label: "Medications",
      description: "Manage prescriptions",
      path: "/medications",
      icon: <LocalPharmacyIcon />,
    },
    {
      label: "Patients",
      description: "View patient records",
      path: "/patients",
      icon: <PeopleIcon />,
    },
    {
      label: "Reports",
      description: "View medication reports",
      path: "/reports",
      icon: <DescriptionIcon />,
    },
  ],
};

// ==========================================================
// STAT CARD
// ==========================================================

function StatCard({
  title,
  value,
  description,
  icon,
  iconBg = "#E3F2FD",
  iconColor = "#1976D2",
}) {
  return (
    <Card
      sx={{
        height: "100%",
        borderRadius: 4,
        border: "1px solid #e5e7eb",
        transition: "all 0.25s ease",
        "&:hover": {
          transform: "translateY(-4px)",
          boxShadow: "0 12px 30px rgba(0,0,0,0.08)",
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box
          sx={{
            width: 52,
            height: 52,
            borderRadius: 3,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            bgcolor: iconBg,
            color: iconColor,
            mb: 2,
          }}
        >
          {icon}
        </Box>

        <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
          {title}
        </Typography>

        <Typography
          variant="h3"
          fontWeight={800}
          sx={{ letterSpacing: "-1px" }}
        >
          {value}
        </Typography>

        <Typography variant="caption" color="text.secondary">
          {description}
        </Typography>
      </CardContent>
    </Card>
  );
}

// ==========================================================
// DASHBOARD
// ==========================================================

export default function Dashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);

  const [stats, setStats] = useState({
    patients: 0,
    service_requests: 0,
    diagnostic_reports: 0,
    observations: 0,
    medication_requests: 0,
  });

  const [bedStats, setBedStats] = useState({
    total: 0,
    available: 0,
    occupied: 0,
  });

  const [loading, setLoading] = useState(true);
  const [bedLoading, setBedLoading] = useState(true);
  const [error, setError] = useState("");

  // ========================================================
  // LOAD USER
  // ========================================================

  useEffect(() => {
    const storedUser = localStorage.getItem("user");

    if (!storedUser) {
      return;
    }

    try {
      const parsedUser = JSON.parse(storedUser);
      setUser(parsedUser);

      console.log("Dashboard user:", parsedUser);
      console.log("Dashboard role:", parsedUser?.role);
      console.log("Dashboard practitioner ID:", parsedUser?.practitioner_id);
    } catch (err) {
      console.error("Unable to parse user:", err);
    }
  }, []);

  // ========================================================
  // FETCH ORIGINAL DASHBOARD STATS
  // ========================================================

  useEffect(() => {
    const fetchDashboardStats = async () => {
      try {
        setLoading(true);
        setError("");

        // Keep the original endpoint exactly as before.
        const response = await api.get("/admin/dashboard-stats");

        console.log("Dashboard stats response:", response.data);

        setStats({
          patients: response.data?.patients ?? 0,

          service_requests: response.data?.service_requests ?? 0,

          diagnostic_reports: response.data?.diagnostic_reports ?? 0,

          observations: response.data?.observations ?? 0,

          medication_requests: response.data?.medication_requests ?? 0,
        });
      } catch (err) {
        console.error("Failed to fetch dashboard stats:", err);

        console.error("Dashboard API response:", err.response?.data);

        setError(
          err.response?.data?.detail || "Unable to load dashboard statistics.",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardStats();
  }, []);

  // ========================================================
  // FETCH BED DATA
  // ========================================================

  useEffect(() => {
    const fetchBedStats = async () => {
      try {
        setBedLoading(true);

        const [availableResponse, occupiedResponse] = await Promise.all([
          api.get("/beds/dashboard/available"),
          api.get("/beds/dashboard/occupied"),
        ]);

        const availableData = availableResponse.data;

        const occupiedData = occupiedResponse.data;

        const available = Array.isArray(availableData)
          ? availableData.length
          : (availableData?.count ?? 0);

        const occupied = Array.isArray(occupiedData)
          ? occupiedData.length
          : (occupiedData?.count ?? 0);

        setBedStats({
          total: available + occupied,
          available,
          occupied,
        });
      } catch (err) {
        console.error("Failed to fetch bed statistics:", err);
      } finally {
        setBedLoading(false);
      }
    };

    fetchBedStats();
  }, []);

  // ========================================================
  // ROLE
  // ========================================================

  const role = user?.role?.toLowerCase() || "admin";

  const roleData = roleInfo[role] || {
    title: "Hospital Dashboard",
    subtitle: "Hospital workflow management",
    greeting: "Welcome back",
  };

  const actions = roleActions[role] || roleActions.admin;

  // ========================================================
  // BED UTILIZATION
  // ========================================================

  const bedUtilization = useMemo(() => {
    if (!bedStats.total) {
      return 0;
    }

    return Math.round((bedStats.occupied / bedStats.total) * 100);
  }, [bedStats]);

  // ========================================================
  // CURRENT DATE
  // ========================================================

  const currentDate = new Intl.DateTimeFormat("en-IN", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(new Date());

  // ========================================================
  // DISPLAY NAME
  // ========================================================

  const displayName =
    [user?.first_name, user?.last_name].filter(Boolean).join(" ") ||
    user?.username ||
    "User";

  // ========================================================
  // STAT CARDS
  // ========================================================

  const cards = [
    {
      title: "Total Patients",
      value: stats.patients,
      description: "FHIR patient records",
      icon: <PeopleIcon fontSize="large" />,
      iconBg: "#E3F2FD",
      iconColor: "#1976D2",
    },

    {
      title: "Service Requests",
      value: stats.service_requests,
      description: "Active clinical requests",
      icon: <AssignmentIcon fontSize="large" />,
      iconBg: "#FFF3E0",
      iconColor: "#EF6C00",
    },

    {
      title: "Diagnostic Reports",
      value: stats.diagnostic_reports,
      description: "Generated diagnostic reports",
      icon: <DescriptionIcon fontSize="large" />,
      iconBg: "#E8F5E9",
      iconColor: "#2E7D32",
    },

    {
      title: "Observations",
      value: stats.observations,
      description: "Clinical observations",
      icon: <VisibilityIcon fontSize="large" />,
      iconBg: "#F3E5F5",
      iconColor: "#7B1FA2",
    },

    {
      title: "Medication Requests",
      value: stats.medication_requests,
      description: "Medication workflows",
      icon: <MedicationIcon fontSize="large" />,
      iconBg: "#FFEBEE",
      iconColor: "#C62828",
    },
  ];

  // ========================================================
  // UI
  // ========================================================

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

        <Box
          component="main"
          sx={{
            p: {
              xs: 2,
              sm: 3,
              lg: 4,
            },
          }}
        >
          {/* ==================================================
              HERO
          ================================================== */}

          <Card
            sx={{
              mb: 4,
              borderRadius: 5,
              overflow: "hidden",
              color: "#fff",
              background: "linear-gradient(135deg, #1565C0 0%, #102A43 100%)",
              boxShadow: "0 15px 40px rgba(21,101,192,0.20)",
            }}
          >
            <CardContent
              sx={{
                p: {
                  xs: 3,
                  md: 4,
                },
              }}
            >
              <Grid container spacing={3} alignItems="center">
                <Grid
                  size={{
                    xs: 12,
                    md: 8,
                  }}
                >
                  <Typography
                    variant="body2"
                    sx={{
                      opacity: 0.8,
                      mb: 1,
                    }}
                  >
                    {currentDate}
                  </Typography>

                  <Typography
                    variant="h4"
                    fontWeight={800}
                    sx={{
                      mb: 1,
                      letterSpacing: "-0.5px",
                    }}
                  >
                    {roleData.greeting}, {displayName}
                  </Typography>

                  <Typography variant="h6" fontWeight={600} sx={{ mb: 1 }}>
                    {roleData.title}
                  </Typography>

                  <Typography
                    variant="body2"
                    sx={{
                      opacity: 0.85,
                      maxWidth: 650,
                    }}
                  >
                    {roleData.subtitle}
                  </Typography>

                  {role === "doctor" && user?.practitioner_id && (
                    <Chip
                      label={`FHIR Practitioner: ${user.practitioner_id}`}
                      sx={{
                        mt: 2,
                        color: "#fff",
                        borderColor: "rgba(255,255,255,0.5)",
                        background: "rgba(255,255,255,0.10)",
                      }}
                      variant="outlined"
                    />
                  )}
                </Grid>

                <Grid
                  size={{
                    xs: 12,
                    md: 4,
                  }}
                  sx={{
                    display: "flex",
                    justifyContent: {
                      xs: "flex-start",
                      md: "flex-end",
                    },
                  }}
                >
                  <Avatar
                    sx={{
                      width: 96,
                      height: 96,
                      fontSize: 38,
                      fontWeight: 700,
                      background: "rgba(255,255,255,0.15)",
                      border: "2px solid rgba(255,255,255,0.35)",
                    }}
                  >
                    {(
                      user?.first_name?.charAt(0) ||
                      user?.username?.charAt(0) ||
                      "U"
                    ).toUpperCase()}
                  </Avatar>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          {/* ==================================================
              ERROR
          ================================================== */}

          {error && (
            <Card
              sx={{
                mb: 3,
                borderRadius: 3,
                border: "1px solid #FECACA",
                bgcolor: "#FEF2F2",
              }}
            >
              <CardContent>
                <Typography color="error" variant="body2">
                  {error}
                </Typography>
              </CardContent>
            </Card>
          )}

          {/* ==================================================
              HOSPITAL OVERVIEW
          ================================================== */}

          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" fontWeight={700} sx={{ mb: 0.5 }}>
              Hospital Overview
            </Typography>

            <Typography variant="body2" color="text.secondary" sx={{ mb: 2.5 }}>
              Key healthcare resources at a glance
            </Typography>

            {loading ? (
              <Card
                sx={{
                  borderRadius: 4,
                  p: 5,
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <CircularProgress />
              </Card>
            ) : (
              <Grid container spacing={3}>
                {cards.map((card) => (
                  <Grid
                    key={card.title}
                    size={{
                      xs: 12,
                      sm: 6,
                      md: 4,
                      lg: 4,
                      xl: 2.4,
                    }}
                  >
                    <StatCard {...card} />
                  </Grid>
                ))}
              </Grid>
            )}
          </Box>

          {/* ==================================================
              LOWER SECTION
          ================================================== */}

          <Grid container spacing={3}>
            {/* ==================================================
                QUICK ACTIONS
            ================================================== */}

            <Grid
              size={{
                xs: 12,
                lg: 8,
              }}
            >
              <Card
                sx={{
                  height: "100%",
                  borderRadius: 4,
                  border: "1px solid #e5e7eb",
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      mb: 2,
                    }}
                  >
                    <Box>
                      <Typography variant="h6" fontWeight={700}>
                        Quick Actions
                      </Typography>

                      <Typography variant="body2" color="text.secondary">
                        Common tasks for your role
                      </Typography>
                    </Box>

                    <Chip
                      label={roleData.title}
                      size="small"
                      variant="outlined"
                    />
                  </Box>

                  <Divider sx={{ mb: 2 }} />

                  <Grid container spacing={2}>
                    {actions.map((action) => (
                      <Grid
                        key={action.label}
                        size={{
                          xs: 12,
                          sm: 6,
                        }}
                      >
                        <Button
                          fullWidth
                          variant="outlined"
                          onClick={() => navigate(action.path)}
                          sx={{
                            minHeight: 92,
                            borderRadius: 3,
                            justifyContent: "flex-start",
                            textTransform: "none",
                            px: 2,
                            gap: 1,
                            transition: "all 0.2s ease",
                            "&:hover": {
                              backgroundColor: "#F8FAFC",
                              transform: "translateY(-2px)",
                            },
                          }}
                          startIcon={
                            <Box
                              sx={{
                                width: 38,
                                height: 38,
                                borderRadius: 2,
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                                bgcolor: "#E3F2FD",
                                color: "#1976D2",
                              }}
                            >
                              {action.icon}
                            </Box>
                          }
                          endIcon={<ArrowForwardIcon />}
                        >
                          <Box
                            sx={{
                              textAlign: "left",
                              flex: 1,
                            }}
                          >
                            <Typography fontWeight={700}>
                              {action.label}
                            </Typography>

                            <Typography
                              variant="caption"
                              color="text.secondary"
                            >
                              {action.description}
                            </Typography>
                          </Box>
                        </Button>
                      </Grid>
                    ))}
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* ==================================================
                BED OVERVIEW
            ================================================== */}

            <Grid
              size={{
                xs: 12,
                lg: 4,
              }}
            >
              <Card
                sx={{
                  height: "100%",
                  borderRadius: 4,
                  border: "1px solid #e5e7eb",
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Box
                    sx={{
                      display: "flex",
                      alignItems: "center",
                      gap: 2,
                      mb: 3,
                    }}
                  >
                    <Box
                      sx={{
                        width: 48,
                        height: 48,
                        borderRadius: 3,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        bgcolor: "#E8F5E9",
                        color: "#2E7D32",
                      }}
                    >
                      <BedIcon />
                    </Box>

                    <Box>
                      <Typography variant="h6" fontWeight={700}>
                        Bed Overview
                      </Typography>

                      <Typography variant="caption" color="text.secondary">
                        Current availability
                      </Typography>
                    </Box>
                  </Box>

                  {bedLoading ? (
                    <Box
                      sx={{
                        py: 5,
                        display: "flex",
                        justifyContent: "center",
                      }}
                    >
                      <CircularProgress size={28} />
                    </Box>
                  ) : (
                    <>
                      <Box sx={{ mb: 2.5 }}>
                        <Box
                          sx={{
                            display: "flex",
                            justifyContent: "space-between",
                            mb: 1,
                          }}
                        >
                          <Typography variant="body2">Occupancy</Typography>

                          <Typography variant="body2" fontWeight={700}>
                            {bedUtilization}%
                          </Typography>
                        </Box>

                        <LinearProgress
                          variant="determinate"
                          value={bedUtilization}
                          sx={{
                            height: 10,
                            borderRadius: 5,
                          }}
                        />
                      </Box>

                      <Grid container spacing={2}>
                        <Grid size={{ xs: 6 }}>
                          <Box
                            sx={{
                              p: 2,
                              borderRadius: 3,
                              bgcolor: "#F0FDF4",
                            }}
                          >
                            <Typography
                              variant="caption"
                              color="text.secondary"
                            >
                              Available
                            </Typography>

                            <Typography
                              variant="h5"
                              fontWeight={800}
                              color="success.main"
                            >
                              {bedStats.available}
                            </Typography>
                          </Box>
                        </Grid>

                        <Grid size={{ xs: 6 }}>
                          <Box
                            sx={{
                              p: 2,
                              borderRadius: 3,
                              bgcolor: "#FFF7ED",
                            }}
                          >
                            <Typography
                              variant="caption"
                              color="text.secondary"
                            >
                              Occupied
                            </Typography>

                            <Typography
                              variant="h5"
                              fontWeight={800}
                              color="warning.main"
                            >
                              {bedStats.occupied}
                            </Typography>
                          </Box>
                        </Grid>
                      </Grid>

                      <Button
                        fullWidth
                        sx={{
                          mt: 3,
                          borderRadius: 2,
                          textTransform: "none",
                        }}
                        variant="text"
                        endIcon={<ArrowForwardIcon />}
                        onClick={() => navigate("/beds")}
                      >
                        View Bed Management
                      </Button>
                    </>
                  )}
                </CardContent>
              </Card>
            </Grid>

            {/* ==================================================
                WORKFLOW CENTER
            ================================================== */}

            <Grid
              size={{
                xs: 12,
              }}
            >
              <Card
                sx={{
                  borderRadius: 4,
                  border: "1px solid #e5e7eb",
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" fontWeight={700} sx={{ mb: 0.5 }}>
                    Workflow Center
                  </Typography>

                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ mb: 3 }}
                  >
                    Access the core hospital workflow modules quickly.
                  </Typography>

                  <Grid container spacing={2}>
                    {[
                      {
                        label: "Admission",
                        description: "Patient admission and bed allocation",
                        path: "/ai",
                        icon: <LocalHospitalIcon />,
                      },
                      {
                        label: "Laboratory",
                        description: "Orders, results and reports",
                        path: "/laboratory",
                        icon: <ScienceIcon />,
                      },
                      {
                        label: "Medication",
                        description: "Medication and prescription workflows",
                        path: "/medications",
                        icon: <MedicationIcon />,
                      },
                      {
                        label: "Patients",
                        description: "Patient records and clinical data",
                        path: "/patients",
                        icon: <PeopleIcon />,
                      },
                      {
                        label: "Settings",
                        description: "Account and system settings",
                        path: "/settings",
                        icon: <SettingsIcon />,
                      },
                    ].map((item) => (
                      <Grid
                        key={item.label}
                        size={{
                          xs: 12,
                          sm: 6,
                          md: 4,
                          lg: 2.4,
                        }}
                      >
                        <Button
                          fullWidth
                          onClick={() => navigate(item.path)}
                          sx={{
                            p: 2,
                            minHeight: 125,
                            borderRadius: 3,
                            border: "1px solid #E5E7EB",
                            justifyContent: "flex-start",
                            alignItems: "flex-start",
                            textTransform: "none",
                            flexDirection: "column",
                            gap: 1,
                            "&:hover": {
                              borderColor: "#90CAF9",
                              background: "#F8FBFF",
                            },
                          }}
                        >
                          <Box
                            sx={{
                              width: 42,
                              height: 42,
                              borderRadius: 2,
                              display: "flex",
                              alignItems: "center",
                              justifyContent: "center",
                              bgcolor: "#E3F2FD",
                              color: "#1976D2",
                            }}
                          >
                            {item.icon}
                          </Box>

                          <Typography fontWeight={700} color="text.primary">
                            {item.label}
                          </Typography>

                          <Typography
                            variant="caption"
                            color="text.secondary"
                            sx={{
                              textAlign: "left",
                            }}
                          >
                            {item.description}
                          </Typography>
                        </Button>
                      </Grid>
                    ))}
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Box>
  );
}
