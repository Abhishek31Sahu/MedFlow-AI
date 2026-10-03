import { useEffect, useState } from "react";
import {
  Button,
  Chip,
  Stack,
  Typography,
  Box,
  Container,
  Paper,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

import BedStatsCards from "./BedStatsCards";
import DataTable from "../../components/ui/DataTable";
import bedService from "../../services/bedService";
import SearchBar from "../../components/ui/SearchBar";
import Sidebar from "../../components/layout/Sidebar";
import Header from "../../components/layout/Header";

const BedDashboard = () => {
  const navigate = useNavigate();
  const [statistics, setStatistics] = useState({});
  const [beds, setBeds] = useState([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const loadBeds = async () => {
    try {
      setLoading(true);

      const response = await bedService.getBeds();

      setBeds(response);
    } catch (error) {
      console.error("Failed to load beds:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async () => {
    const data = await bedService.getStatistics();
    setStatistics(data);
  };

  useEffect(() => {
    loadBeds();
    loadStatistics();
  }, []);
  const filteredBeds = beds.filter((bed) => {
    const keyword = search.trim().toLowerCase();

    return (
      bed.bed_number?.toLowerCase().includes(keyword) ||
      bed.ward?.toLowerCase().includes(keyword) ||
      bed.room_number?.toLowerCase().includes(keyword) ||
      bed.department?.toLowerCase().includes(keyword) ||
      bed.status?.toLowerCase().includes(keyword) ||
      bed.bed_type?.toLowerCase().includes(keyword)
    );
  });

  const statusColor = (status) => {
    switch (status?.toUpperCase()) {
      case "AVAILABLE":
        return "success";
      case "OCCUPIED":
        return "error";
      case "RESERVED":
        return "warning";
      case "CLEANING":
        return "info";
      case "MAINTENANCE":
        return "default";
      default:
        return "default";
    }
  };

  const columns = [
    {
      field: "bed_number",
      headerName: "Bed No",
    },
    {
      field: "ward",
      headerName: "Ward",
    },
    {
      field: "room_number",
      headerName: "Room",
    },
    {
      field: "department",
      headerName: "Department",
    },
    {
      field: "floor",
      headerName: "Floor",
      render: (row) => row.floor || "-",
    },
    {
      field: "bed_type",
      headerName: "Bed Type",
    },
    {
      field: "gender_policy",
      headerName: "Gender",
      render: (row) => row.gender_policy || "Any",
    },
    {
      field: "oxygen",
      headerName: "O₂",
      align: "center",
      render: (row) => (row.oxygen ? "✓" : "—"),
    },
    {
      field: "ventilator",
      headerName: "Ventilator",
      align: "center",
      render: (row) => (row.ventilator ? "✓" : "—"),
    },
    {
      field: "isolation",
      headerName: "Isolation",
      align: "center",
      render: (row) => (row.isolation ? "✓" : "—"),
    },
    {
      field: "status",
      headerName: "Status",
      render: (row) => (
        <Chip label={row.status} color={statusColor(row.status)} size="small" />
      ),
    },
    {
      field: "occupied_by",
      headerName: "Patient",
      render: (row) => row.occupied_by || "-",
    },
    {
      field: "actions",
      headerName: "Actions",
      sortable: false,
      render: (row) => (
        <Stack direction="row" spacing={1}>
          <Button
            size="small"
            variant="outlined"
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/beds/${row.id}/edit`);
            }}
          >
            Edit
          </Button>

          <Button
            size="small"
            color="success"
            variant="contained"
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/beds/${row.id}`);
            }}
          >
            View
          </Button>
        </Stack>
      ),
    },
  ];

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
        <BedStatsCards stats={statistics} />
        {/* Page Content */}
        <Container maxWidth={false} sx={{ py: 4 }}>
          {/* Page Title */}
          <Typography variant="h4" fontWeight={700} mb={3}>
            Bed Management
          </Typography>

          {/* Search + Add Button */}
          <Paper
            elevation={1}
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
              placeholder="Search Beds..."
              width={350}
            />

            <Button
              variant="contained"
              size="large"
              onClick={() => navigate("/beds/add")}
            >
              Add Bed
            </Button>
          </Paper>

          {/* Data Table */}
          <Paper
            elevation={2}
            sx={{
              borderRadius: 3,
              overflow: "hidden",
              position: "relative", // anchors sticky header to THIS container, not the viewport
            }}
          >
            <Box sx={{ overflowX: "auto" }}>
              <DataTable
                columns={columns}
                rows={filteredBeds}
                loading={loading}
                selectable
                striped
                stickyHeader
                rowKey="id"
              />
            </Box>
          </Paper>
        </Container>
      </Box>
    </Box>
  );
};

export default BedDashboard;
