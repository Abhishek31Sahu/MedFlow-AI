import { useEffect, useState } from "react";
import {
  Avatar,
  Box,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Divider,
} from "@mui/material";

import {
  FaUser,
  FaSignOutAlt,
  FaUserMd,
  FaUserNurse,
  FaFlask,
  FaUserTie,
  FaPills,
  FaShieldAlt,
} from "react-icons/fa";

import { useNavigate } from "react-router-dom";
import { logout } from "../../services/authService";

// ==========================================================
// ROLE DISPLAY
// ==========================================================

const roleInfo = {
  admin: {
    label: "Administrator",
    icon: <FaShieldAlt />,
  },

  doctor: {
    label: "Doctor",
    icon: <FaUserMd />,
  },

  nurse: {
    label: "Nurse",
    icon: <FaUserNurse />,
  },

  receptionist: {
    label: "Receptionist",
    icon: <FaUserTie />,
  },

  lab_technician: {
    label: "Lab Technician",
    icon: <FaFlask />,
  },

  pharmacist: {
    label: "Pharmacist",
    icon: <FaPills />,
  },
};

// ==========================================================
// HEADER
// ==========================================================

export default function Header() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [anchorEl, setAnchorEl] = useState(null);

  const menuOpen = Boolean(anchorEl);

  // ========================================================
  // LOAD USER
  // ========================================================

  useEffect(() => {
    const loadUser = () => {
      const storedUser = localStorage.getItem("user");

      if (!storedUser) {
        setUser(null);
        return;
      }

      try {
        const parsedUser = JSON.parse(storedUser);
        setUser(parsedUser);
      } catch (error) {
        console.error("Failed to read logged-in user:", error);

        localStorage.removeItem("user");
        setUser(null);
      }
    };

    loadUser();

    // Update when another component changes auth state
    window.addEventListener("storage", loadUser);

    return () => {
      window.removeEventListener("storage", loadUser);
    };
  }, []);

  // ========================================================
  // USER DATA
  // ========================================================

  const role = user?.role?.toLowerCase();

  const currentRole = roleInfo[role] || {
    label: "User",
    icon: <FaUser />,
  };

  const fullName =
    [user?.first_name, user?.last_name].filter(Boolean).join(" ") ||
    user?.username ||
    "User";

  const initials = (
    user?.first_name?.charAt(0) ||
    user?.username?.charAt(0) ||
    "U"
  ).toUpperCase();

  // ========================================================
  // MENU
  // ========================================================

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  // ========================================================
  // LOGOUT
  // ========================================================

  const handleLogout = async () => {
    handleMenuClose();

    try {
      await logout();
    } catch (error) {
      console.error("Logout failed:", error);
    } finally {
      localStorage.removeItem("user");

      navigate("/login", {
        replace: true,
      });
    }
  };

  // ========================================================
  // ROLE-BASED CONTEXT
  // ========================================================

  const getRoleMessage = () => {
    switch (role) {
      case "admin":
        return "Hospital Administration";

      case "doctor":
        return user?.department
          ? `${user.department} • Clinical`
          : "Clinical Operations";

      case "nurse":
        return user?.department
          ? `${user.department} • Nursing`
          : "Nursing Operations";

      case "lab_technician":
        return "Laboratory Operations";

      case "receptionist":
        return "Front Desk Operations";

      case "pharmacist":
        return "Pharmacy Operations";

      default:
        return "Hospital Workflow System";
    }
  };

  // ========================================================
  // UI
  // ========================================================

  return (
    <Box
      sx={{
        height: 72,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        px: 3,
        borderBottom: "1px solid #e5e7eb",
        backgroundColor: "#ffffff",
        position: "sticky",
        top: 0,
        zIndex: 20,
      }}
    >
      {/* ==================================================
          LEFT
      ================================================== */}

      <Box>
        <Typography variant="h6" fontWeight={600} color="text.primary">
          Hospital Workflow
        </Typography>

        <Typography variant="body2" color="text.secondary">
          {getRoleMessage()}
        </Typography>
      </Box>

      {/* ==================================================
          RIGHT
      ================================================== */}

      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 2,
        }}
      >
        {/* Role */}
        <Chip
          icon={currentRole.icon}
          label={currentRole.label}
          size="small"
          variant="outlined"
        />

        {/* Doctor Practitioner ID */}
        {role === "doctor" && user?.practitioner_id && (
          <Chip
            label={`Practitioner: ${user.practitioner_id}`}
            size="small"
            color="success"
            variant="outlined"
          />
        )}

        {/* User */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1,
          }}
        >
          <Box sx={{ textAlign: "right" }}>
            <Typography variant="body2" fontWeight={600}>
              {fullName}
            </Typography>

            <Typography variant="caption" color="text.secondary">
              {user?.email || ""}
            </Typography>
          </Box>

          <IconButton onClick={handleMenuOpen} size="small">
            <Avatar
              sx={{
                width: 40,
                height: 40,
                bgcolor: "primary.main",
              }}
            >
              {initials}
            </Avatar>
          </IconButton>
        </Box>
      </Box>

      {/* ==================================================
          USER MENU
      ================================================== */}

      <Menu
        anchorEl={anchorEl}
        open={menuOpen}
        onClose={handleMenuClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "right",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "right",
        }}
      >
        <Box sx={{ px: 2, py: 1 }}>
          <Typography fontWeight={600}>{fullName}</Typography>

          <Typography variant="caption" color="text.secondary">
            {currentRole.label}
          </Typography>
        </Box>

        <Divider />

        <MenuItem
          onClick={() => {
            handleMenuClose();
            navigate("/settings");
          }}
        >
          <FaUser style={{ marginRight: 10 }} />
          Profile
        </MenuItem>

        <MenuItem onClick={handleLogout}>
          <FaSignOutAlt style={{ marginRight: 10 }} />
          Logout
        </MenuItem>
      </Menu>
    </Box>
  );
}
