import { Chip } from "@mui/material";

export default function LabStatusChip({ status }) {
  const value = status?.toString().toUpperCase();

  const color =
    value === "COMPLETED"
      ? "success"
      : value === "PENDING"
        ? "warning"
        : value === "CANCELLED"
          ? "error"
          : "info";

  return <Chip label={status || "UNKNOWN"} color={color} size="small" />;
}
