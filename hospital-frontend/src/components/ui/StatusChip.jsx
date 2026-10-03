import { Chip } from "@mui/material";
import {
  FaCheckCircle,
  FaTimesCircle,
  FaClock,
  FaBed,
  FaUserMd,
} from "react-icons/fa";

export default function StatusChip({ status, size = "small" }) {
  const config = {
    ACTIVE: {
      label: "Active",
      color: "success",
      icon: <FaCheckCircle />,
    },

    INACTIVE: {
      label: "Inactive",
      color: "default",
      icon: <FaTimesCircle />,
    },

    PENDING: {
      label: "Pending",
      color: "warning",
      icon: <FaClock />,
    },

    OCCUPIED: {
      label: "Occupied",
      color: "error",
      icon: <FaBed />,
    },

    AVAILABLE: {
      label: "Available",
      color: "success",
      icon: <FaBed />,
    },

    ON_DUTY: {
      label: "On Duty",
      color: "primary",
      icon: <FaUserMd />,
    },

    OFF_DUTY: {
      label: "Off Duty",
      color: "secondary",
      icon: <FaUserMd />,
    },
  };

  const item = config[status] || {
    label: status || "Unknown",
    color: "default",
    icon: <FaClock />,
  };

  return (
    <Chip
      size={size}
      label={item.label}
      color={item.color}
      icon={item.icon}
      variant="filled"
      sx={{
        fontWeight: 600,
        borderRadius: "10px",
        px: 1,
      }}
    />
  );
}
