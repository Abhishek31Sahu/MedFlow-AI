import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import {
  Alert,
  Avatar,
  Box,
  Button,
  Chip,
  CircularProgress,
  IconButton,
  Paper,
  Stack,
  Typography,
} from "@mui/material";

import {
  Add,
  ArrowBack,
  Delete,
  Edit,
  AccessTime,
  CalendarMonth,
} from "@mui/icons-material";

import StaffScheduleForm from "../components/forms/StaffScheduleForm";

import {
  getPractitionerSchedules,
  createPractitionerSchedule,
  updatePractitionerSchedule,
  deletePractitionerSchedule,
} from "../services/staffSchedule";

import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";

const DAYS = [
  "MONDAY",
  "TUESDAY",
  "WEDNESDAY",
  "THURSDAY",
  "FRIDAY",
  "SATURDAY",
  "SUNDAY",
];

export default function StaffScheduleManagement() {
  const navigate = useNavigate();
  const location = useLocation();

  // =====================================================
  // GET STAFF FROM NAVIGATION STATE
  // =====================================================

  const staff = location.state?.staff;

  const [schedules, setSchedules] = useState([]);

  const [loading, setLoading] = useState(false);

  const [openForm, setOpenForm] = useState(false);

  const [selectedSchedule, setSelectedSchedule] = useState(null);

  const [error, setError] = useState("");

  // =====================================================
  // DEBUG
  // =====================================================

  console.log("Schedule page staff:", staff);

  // =====================================================
  // FETCH SCHEDULES
  // =====================================================

  const fetchSchedules = async () => {
    if (!staff?.practitioner_id) {
      console.log("No practitioner ID found:", staff);

      return;
    }

    try {
      setLoading(true);
      setError("");

      const data = await getPractitionerSchedules(staff.practitioner_id);

      console.log("Practitioner schedule API response:", data);

      /*
       * Expected backend response:
       *
       * {
       *   practitioner_id: "...",
       *   day_of_week: "monday",
       *   schedules: [
       *     {
       *       id: "...",
       *       practitioner_id: "...",
       *       day_of_week: "monday",
       *       start_time: "10:00:00",
       *       end_time: "16:00:00",
       *       is_active: true
       *     }
       *   ]
       * }
       */

      const list = Array.isArray(data?.schedules)
        ? data.schedules
        : Array.isArray(data)
          ? data
          : [];

      console.log("Normalized schedules:", list);

      setSchedules(list);
    } catch (error) {
      console.error("Failed to fetch schedules:", error);

      setError(error?.response?.data?.detail || "Failed to load schedules.");

      setSchedules([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSchedules();
  }, [staff?.practitioner_id]);

  // =====================================================
  // ADD
  // =====================================================

  const handleAdd = () => {
    setSelectedSchedule(null);
    setOpenForm(true);
  };

  // =====================================================
  // EDIT
  // =====================================================

  const handleEdit = (schedule) => {
    setSelectedSchedule(schedule);
    setOpenForm(true);
  };

  // =====================================================
  // SAVE
  // =====================================================

  const handleSave = async (data) => {
    try {
      setLoading(true);

      if (selectedSchedule) {
        await updatePractitionerSchedule(selectedSchedule.id, data);
      } else {
        await createPractitionerSchedule(data);
      }

      setOpenForm(false);
      setSelectedSchedule(null);

      await fetchSchedules();
    } catch (error) {
      console.error("Failed to save schedule:", error);

      setError(error?.response?.data?.detail || "Failed to save schedule.");
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // DELETE
  // =====================================================

  const handleDelete = async (scheduleId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this schedule?",
    );

    if (!confirmed) {
      return;
    }

    try {
      setLoading(true);

      await deletePractitionerSchedule(scheduleId);

      await fetchSchedules();
    } catch (error) {
      console.error("Failed to delete schedule:", error);

      setError(error?.response?.data?.detail || "Failed to delete schedule.");
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // GET SCHEDULES FOR DAY
  // =====================================================

  const getDaySchedules = (day) => {
    return schedules.filter(
      (schedule) => String(schedule.day_of_week).toUpperCase() === day,
    );
  };

  // =====================================================
  // STAFF NOT FOUND
  // =====================================================

  if (!staff) {
    return (
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: "280px 1fr",
          minHeight: "100vh",
          backgroundColor: "#f6f8fb",
        }}
      >
        <Box
          component="aside"
          sx={{
            position: "sticky",
            top: 0,
            height: "100vh",
          }}
        >
          <Sidebar />
        </Box>

        <Box>
          <Header />

          <Box sx={{ p: 4 }}>
            <Alert severity="error">
              Staff information was not passed to the schedule page.
            </Alert>

            <Button
              sx={{ mt: 2 }}
              startIcon={<ArrowBack />}
              onClick={() => navigate("/staff")}
            >
              Back to Staff Management
            </Button>
          </Box>
        </Box>
      </Box>
    );
  }

  // =====================================================
  // STAFF NAME
  // =====================================================

  const fullName =
    [staff.first_name, staff.last_name].filter(Boolean).join(" ") ||
    staff.username ||
    "Staff";

  // =====================================================
  // UI
  // =====================================================

  return (
    <Box
      sx={{
        display: "grid",
        gridTemplateColumns: "280px 1fr",
        minHeight: "100vh",
        backgroundColor: "#f6f8fb",
      }}
    >
      {/* =================================================
          SIDEBAR
      ================================================= */}

      <Box
        component="aside"
        sx={{
          position: "sticky",
          top: 0,
          height: "100vh",
          overflowY: "auto",
          zIndex: 10,
        }}
      >
        <Sidebar />
      </Box>

      {/* =================================================
          MAIN
      ================================================= */}

      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          minWidth: 0,
        }}
      >
        <Header />

        <Box
          component="main"
          sx={{
            flex: 1,
            p: {
              xs: 2,
              md: 3,
            },
          }}
        >
          {/* =================================================
              PAGE HEADER
          ================================================= */}

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
            spacing={2}
            sx={{ mb: 3 }}
          >
            <Box>
              <Button
                startIcon={<ArrowBack />}
                onClick={() => navigate("/staff")}
                sx={{
                  mb: 1,
                  px: 0,
                  textTransform: "none",
                }}
              >
                Back to Staff Management
              </Button>

              <Stack direction="row" spacing={1} alignItems="center">
                <CalendarMonth color="primary" />

                <Typography variant="h5" fontWeight={700}>
                  Practitioner Schedule
                </Typography>
              </Stack>

              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ mt: 0.5 }}
              >
                Manage weekly working hours for {fullName}
              </Typography>
            </Box>

            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={handleAdd}
              disabled={!staff.practitioner_id}
              sx={{
                borderRadius: 2,
                px: 2.5,
                py: 1.2,
                fontWeight: 600,
              }}
            >
              Add Schedule
            </Button>
          </Stack>

          {/* =================================================
              STAFF INFORMATION
          ================================================= */}

          <Paper
            elevation={0}
            sx={{
              p: 2.5,
              mb: 3,
              borderRadius: 3,
              border: "1px solid #e5e7eb",
              backgroundColor: "#ffffff",
            }}
          >
            <Stack
              direction={{
                xs: "column",
                md: "row",
              }}
              spacing={3}
              alignItems={{
                xs: "flex-start",
                md: "center",
              }}
            >
              {/* AVATAR */}

              <Avatar
                sx={{
                  width: 58,
                  height: 58,
                  bgcolor: "primary.main",
                  fontSize: 22,
                  fontWeight: 600,
                }}
              >
                {(
                  staff.first_name?.charAt(0) ||
                  staff.username?.charAt(0) ||
                  "S"
                ).toUpperCase()}
              </Avatar>

              {/* NAME */}

              <Box
                sx={{
                  minWidth: {
                    md: 200,
                  },
                }}
              >
                <Typography variant="h6" fontWeight={700}>
                  {fullName}
                </Typography>

                <Typography variant="body2" color="text.secondary">
                  {staff.designation || "Staff"}
                </Typography>
              </Box>

              {/* DEPARTMENT */}

              <Box>
                <Typography variant="caption" color="text.secondary">
                  Department
                </Typography>

                <Typography fontWeight={500}>
                  {staff.department || "-"}
                </Typography>
              </Box>

              {/* ROLE */}

              <Box>
                <Typography variant="caption" color="text.secondary">
                  Role
                </Typography>

                <Box sx={{ mt: 0.5 }}>
                  <Chip
                    label={staff.role || "STAFF"}
                    color="primary"
                    size="small"
                  />
                </Box>
              </Box>

              {/* PRACTITIONER ID */}

              <Box
                sx={{
                  ml: {
                    md: "auto",
                  },
                }}
              >
                <Typography variant="caption" color="text.secondary">
                  Practitioner ID
                </Typography>

                <Typography
                  variant="body2"
                  sx={{
                    fontFamily: "monospace",
                    mt: 0.3,
                  }}
                >
                  {staff.practitioner_id}
                </Typography>
              </Box>
            </Stack>
          </Paper>

          {/* =================================================
              ERROR
          ================================================= */}

          {error && (
            <Alert
              severity="error"
              sx={{
                mb: 2,
                borderRadius: 2,
              }}
            >
              {error}
            </Alert>
          )}

          {/* =================================================
              WEEKLY SCHEDULE HEADER
          ================================================= */}

          <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 2 }}>
            <Typography variant="h6" fontWeight={600}>
              Weekly Schedule
            </Typography>

            <Chip
              label={`${schedules.length} ${
                schedules.length === 1 ? "schedule" : "schedules"
              }`}
              size="small"
              variant="outlined"
            />
          </Stack>

          {/* =================================================
              LOADING
          ================================================= */}

          {loading && schedules.length === 0 ? (
            <Paper
              elevation={0}
              sx={{
                p: 6,
                textAlign: "center",
                borderRadius: 3,
                border: "1px solid #e5e7eb",
              }}
            >
              <CircularProgress />

              <Typography color="text.secondary" sx={{ mt: 2 }}>
                Loading schedule...
              </Typography>
            </Paper>
          ) : (
            <Stack spacing={1.5}>
              {DAYS.map((day) => {
                const daySchedules = getDaySchedules(day);

                const isWorking = daySchedules.length > 0;

                return (
                  <Paper
                    key={day}
                    elevation={0}
                    sx={{
                      p: 2.2,
                      borderRadius: 3,

                      border: isWorking
                        ? "1px solid #c8e6c9"
                        : "1px solid #e5e7eb",

                      backgroundColor: isWorking ? "#fbfffc" : "#ffffff",

                      transition: "all 0.2s ease",

                      "&:hover": {
                        boxShadow: "0 4px 14px rgba(0,0,0,0.07)",
                      },
                    }}
                  >
                    <Stack
                      direction={{
                        xs: "column",
                        sm: "row",
                      }}
                      spacing={2}
                      alignItems={{
                        xs: "flex-start",
                        sm: "center",
                      }}
                    >
                      {/* DAY */}

                      <Box
                        sx={{
                          width: {
                            xs: "100%",
                            sm: 150,
                          },
                        }}
                      >
                        <Typography fontWeight={700} fontSize={16}>
                          {formatDay(day)}
                        </Typography>

                        <Typography variant="caption" color="text.secondary">
                          Weekly availability
                        </Typography>
                      </Box>

                      {/* SCHEDULE */}

                      <Box sx={{ flex: 1 }}>
                        {!isWorking ? (
                          <Chip
                            label="Not working"
                            size="small"
                            variant="outlined"
                            sx={{
                              color: "text.secondary",
                            }}
                          />
                        ) : (
                          <Stack spacing={1}>
                            {daySchedules.map((schedule) => (
                              <Stack
                                key={schedule.id}
                                direction="row"
                                spacing={1.2}
                                alignItems="center"
                                flexWrap="wrap"
                              >
                                <Box
                                  sx={{
                                    width: 34,
                                    height: 34,
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    borderRadius: 2,
                                    bgcolor: "#e8f5e9",
                                  }}
                                >
                                  <AccessTime
                                    fontSize="small"
                                    sx={{
                                      color: "#2e7d32",
                                    }}
                                  />
                                </Box>

                                <Typography fontWeight={600}>
                                  {formatTime(schedule.start_time)}
                                  {" - "}
                                  {formatTime(schedule.end_time)}
                                </Typography>

                                <Chip
                                  label={
                                    schedule.is_active === false
                                      ? "Inactive"
                                      : "Working"
                                  }
                                  color={
                                    schedule.is_active === false
                                      ? "default"
                                      : "success"
                                  }
                                  size="small"
                                />
                              </Stack>
                            ))}
                          </Stack>
                        )}
                      </Box>

                      {/* ACTIONS */}

                      {isWorking && (
                        <Stack direction="row" spacing={0.5}>
                          {daySchedules.map((schedule) => (
                            <Box key={schedule.id}>
                              <IconButton
                                size="small"
                                color="primary"
                                title="Edit schedule"
                                onClick={() => handleEdit(schedule)}
                              >
                                <Edit />
                              </IconButton>

                              <IconButton
                                size="small"
                                color="error"
                                title="Delete schedule"
                                onClick={() => handleDelete(schedule.id)}
                              >
                                <Delete />
                              </IconButton>
                            </Box>
                          ))}
                        </Stack>
                      )}
                    </Stack>
                  </Paper>
                );
              })}
            </Stack>
          )}

          {/* =================================================
              ADD / EDIT FORM
          ================================================= */}

          <StaffScheduleForm
            open={openForm}
            staff={staff}
            initialData={selectedSchedule}
            onClose={() => {
              setOpenForm(false);
              setSelectedSchedule(null);
            }}
            onSubmit={handleSave}
            loading={loading}
          />
        </Box>
      </Box>
    </Box>
  );
}

// =====================================================
// FORMAT DAY
// =====================================================

function formatDay(day) {
  return day.charAt(0) + day.slice(1).toLowerCase();
}

// =====================================================
// FORMAT TIME
// =====================================================

function formatTime(value) {
  if (!value) {
    return "--";
  }

  const [hours, minutes] = String(value).split(":");

  const date = new Date();

  date.setHours(Number(hours), Number(minutes), 0);

  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}
