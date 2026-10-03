import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Avatar,
  Box,
  Button,
  Chip,
  IconButton,
  Paper,
  Stack,
  Typography,
} from "@mui/material";

import { Add, Delete, Edit, CalendarMonth } from "@mui/icons-material";

import DataTable from "../components/ui/DataTable";
import SearchBar from "../components/ui/SearchBar";
import StatusChip from "../components/ui/StatusChip";
import StaffForm from "../components/forms/StaffForm";
import StaffScheduleManagement from "../pages/StaffScheduleManagement";
import {
  getUsers,
  createUser,
  updateUser,
  deleteUser,
} from "../services/userService";

import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";

export default function StaffManagement() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [openForm, setOpenForm] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [scheduleStaff, setScheduleStaff] = useState(null);
  const navigate = useNavigate();
  // ================= FETCH USERS =================
  const fetchUsers = async () => {
    try {
      setLoading(true);

      const data = await getUsers();

      console.log("Users API response:", data);

      const userList = Array.isArray(data)
        ? data
        : Array.isArray(data?.users)
          ? data.users
          : [];

      setUsers(userList);
    } catch (error) {
      console.error("Failed to fetch users:", error);
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  // ================= SEARCH =================
  const filteredUsers = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return users;
    }

    return users.filter((user) => {
      const searchableFields = [
        user.username,
        user.email,
        user.first_name,
        user.last_name,
        user.phone,
        user.department,
        user.designation,
        user.role,
        user.practitioner_id,
      ];

      return searchableFields.some((field) =>
        String(field ?? "")
          .toLowerCase()
          .includes(query),
      );
    });
  }, [users, search]);

  // ================= ADD =================
  const handleAdd = () => {
    setSelectedUser(null);
    setOpenForm(true);
  };

  //  ================= Schedule =================

  const handleSchedule = (user) => {
    if (!user.practitioner_id) {
      alert("This staff member does not have a practitioner ID.");
      return;
    }

    setScheduleStaff(user);
  };

  // ================= EDIT =================
  const handleEdit = (user) => {
    setSelectedUser(user);
    setOpenForm(true);
  };

  // ================= DELETE =================
  const handleDelete = async (id) => {
    if (!window.confirm("Delete this user?")) {
      return;
    }

    try {
      setLoading(true);

      await deleteUser(id);

      await fetchUsers();
    } catch (error) {
      console.error("Failed to delete user:", error);
    } finally {
      setLoading(false);
    }
  };

  // ================= SAVE =================
  const handleSave = async (data) => {
    try {
      setLoading(true);

      if (selectedUser) {
        await updateUser(selectedUser.id, data);
      } else {
        await createUser(data);
      }

      setOpenForm(false);
      setSelectedUser(null);

      await fetchUsers();
    } catch (error) {
      console.error("Failed to save user:", error);
    } finally {
      setLoading(false);
    }
  };
  // ================= SAVE Schedule =================
  const handleScheduleSave = async (data) => {
    try {
      setLoading(true);
    } catch (error) {
      console.error("Failed to save user:", error);
    } finally {
      setLoading(false);
    }
  };
  // ================= TABLE COLUMNS =================
  const columns = [
    {
      field: "avatar",
      headerName: "",
      sortable: false,
      minWidth: 70,

      render: (row) => (
        <Avatar
          sx={{
            bgcolor: "#1976d2",
          }}
        >
          {(
            row.first_name?.charAt(0) ||
            row.username?.charAt(0) ||
            "U"
          ).toUpperCase()}
        </Avatar>
      ),
    },

    {
      field: "name",
      headerName: "Name",
      minWidth: 180,

      render: (row) => {
        const fullName = [row.first_name, row.last_name]
          .filter(Boolean)
          .join(" ");

        return (
          <Typography fontWeight={500}>
            {fullName || row.username || "-"}
          </Typography>
        );
      },
    },

    {
      field: "username",
      headerName: "Username",
      minWidth: 150,
    },

    {
      field: "email",
      headerName: "Email",
      minWidth: 220,
    },

    {
      field: "role",
      headerName: "Role",
      minWidth: 150,

      render: (row) => (
        <Chip label={row.role || "staff"} color="primary" size="small" />
      ),
    },

    {
      field: "department",
      headerName: "Department",
      minWidth: 170,

      render: (row) => row.department || "-",
    },

    {
      field: "designation",
      headerName: "Designation",
      minWidth: 180,

      render: (row) => row.designation || "-",
    },

    {
      field: "phone",
      headerName: "Phone",
      minWidth: 140,

      render: (row) => row.phone || "-",
    },

    {
      field: "practitioner_id",
      headerName: "Practitioner ID",
      minWidth: 160,

      render: (row) =>
        row.practitioner_id ? (
          <Chip
            label={row.practitioner_id}
            color="success"
            size="small"
            variant="outlined"
          />
        ) : (
          <Typography color="text.secondary">Not created</Typography>
        ),
    },

    {
      field: "is_active",
      headerName: "Status",
      minWidth: 120,

      render: (row) => (
        <StatusChip status={row.is_active ? "ACTIVE" : "INACTIVE"} />
      ),
    },

    {
      field: "actions",
      headerName: "Actions",
      sortable: false,
      minWidth: 140,

      render: (row) => (
        <Stack direction="row" spacing={1}>
          <IconButton
            color="primary"
            onClick={(e) => {
              e.stopPropagation();
              handleEdit(row);
            }}
          >
            <Edit />
          </IconButton>

          <IconButton
            color="error"
            onClick={(e) => {
              e.stopPropagation();
              handleDelete(row.id);
            }}
          >
            <Delete />
          </IconButton>
          <Button
            size="small"
            variant="text"
            color="secondary"
            startIcon={<CalendarMonth />}
            disabled={!row.practitioner_id}
            onClick={(e) => {
              e.stopPropagation();

              console.log("Staff being sent to schedule:", row);

              navigate(`/staff/${row.id}/schedule`, {
                state: {
                  staff: row,
                },
              });
            }}
          >
            Schedule
          </Button>
        </Stack>
      ),
    },
  ];

  // ================= UI =================
  return (
    <Box
      sx={{
        display: "grid",
        gridTemplateColumns: "280px 1fr",
        minHeight: "100vh",
      }}
    >
      {/* ================= SIDEBAR ================= */}
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

      {/* ================= MAIN ================= */}
      <Box
        sx={{
          gridColumn: "2",
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
            p: 3,
          }}
        >
          {/* ================= PAGE TITLE ================= */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="h5" fontWeight={600}>
              Staff Management
            </Typography>

            <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
              Manage hospital staff accounts, roles and practitioner
              information.
            </Typography>
          </Box>

          {/* ================= SEARCH + ADD ================= */}
          <Paper
            sx={{
              p: 2,
              mb: 3,
              borderRadius: 3,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: 2,
            }}
          >
            <SearchBar
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search name, username, email, role or department..."
            />

            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={handleAdd}
              sx={{
                flexShrink: 0,
              }}
            >
              Add User
            </Button>
          </Paper>

          {/* ================= DATA TABLE ================= */}
          <Paper
            elevation={2}
            sx={{
              borderRadius: 3,
              overflow: "hidden",
              position: "relative",
            }}
          >
            <Box
              sx={{
                overflowX: "auto",
              }}
            >
              <DataTable
                columns={columns}
                rows={filteredUsers}
                loading={loading}
                selectable
                striped
                stickyHeader
                rowKey="id"
              />
            </Box>
          </Paper>

          {/* ================= STAFF FORM ================= */}
          <StaffForm
            open={openForm}
            onClose={() => {
              setOpenForm(false);
              setSelectedUser(null);
            }}
            onSubmit={handleSave}
            initialData={selectedUser}
            loading={loading}
          />
        </Box>
      </Box>
    </Box>
  );
}
