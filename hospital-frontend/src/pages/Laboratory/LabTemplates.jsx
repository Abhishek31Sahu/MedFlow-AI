import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  Box,
  Button,
  Card,
  Chip,
  CircularProgress,
  Container,
  IconButton,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import EditOutlinedIcon from "@mui/icons-material/EditOutlined";
import DeleteIcon from "@mui/icons-material/Delete";
import SearchIcon from "@mui/icons-material/Search";
import Sidebar from "../../components/layout/Sidebar";
import Header from "../../components/layout/Header";

import { getTemplates, deleteTemplate } from "../../services/labTemplateApi";

export default function LabTemplates() {
  const navigate = useNavigate();

  const [templates, setTemplates] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  // ==========================================
  // Load Templates
  // ==========================================

  const loadTemplates = async () => {
    try {
      setLoading(true);

      const response = await getTemplates();

      setTemplates(Array.isArray(response) ? response : response?.data || []);
    } catch (error) {
      console.error("Load templates error:", error.response?.data || error);

      alert(error.response?.data?.detail || "Unable to load templates.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTemplates();
  }, []);

  // ==========================================
  // Delete Template
  // ==========================================

  const handleDelete = async (testCode) => {
    if (
      !window.confirm(`Are you sure you want to delete "${testCode}" template?`)
    ) {
      return;
    }

    try {
      await deleteTemplate(testCode);

      // Remove using test_code, not id
      setTemplates((prev) =>
        prev.filter((template) => template.test_code !== testCode),
      );
    } catch (error) {
      console.error("Delete template error:", error.response?.data || error);

      alert(error.response?.data?.detail || "Unable to delete template.");
    }
  };

  // ==========================================
  // Search
  // ==========================================

  const filteredTemplates = templates.filter((template) => {
    const text = `
        ${template.test_code || ""}
        ${template.test_name || ""}
        ${template.category || ""}
      `.toLowerCase();

    return text.includes(search.toLowerCase());
  });

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

        {/* Page Content */}
        <Container maxWidth={false} sx={{ py: 4 }}>
          {/* ======================================
              Page Header
          ======================================= */}
          <Stack
            direction={{
              xs: "column",
              md: "row",
            }}
            justifyContent="space-between"
            alignItems={{
              xs: "stretch",
              md: "center",
            }}
            gap={2}
            mb={3}
          >
            <Box>
              <Typography variant="h4" fontWeight={700}>
                Laboratory Templates
              </Typography>

              <Typography color="text.secondary">
                Manage laboratory tests and their parameters
              </Typography>
            </Box>

            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => navigate("/laboratory/templates/create")}
            >
              Create Template
            </Button>
          </Stack>

          {/* ======================================
              Search
          ======================================= */}

          <TextField
            fullWidth
            placeholder="Search templates by code, name or category..."
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

          {/* ======================================
              Loading
          ======================================= */}

          {loading ? (
            <Box display="flex" justifyContent="center" py={10}>
              <CircularProgress />
            </Box>
          ) : filteredTemplates.length === 0 ? (
            <Card
              sx={{
                p: 8,
                textAlign: "center",
              }}
            >
              <Typography variant="h6" fontWeight={600} mb={1}>
                No templates found
              </Typography>

              <Typography color="text.secondary" mb={3}>
                {search
                  ? "No templates match your search."
                  : "Create your first laboratory template."}
              </Typography>

              {!search && (
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() => navigate("/laboratory/templates/create")}
                >
                  Create Template
                </Button>
              )}
            </Card>
          ) : (
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: {
                  xs: "1fr",
                  lg: "repeat(2, 1fr)",
                },
                gap: 2,
              }}
            >
              {filteredTemplates.map((template) => (
                <Card
                  key={template.test_code}
                  sx={{
                    p: 2.5,
                    border: "1px solid #E2E8F0",
                    borderRadius: 3,
                  }}
                >
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
                    gap={2}
                  >
                    {/* ==================================
                          Template Information
                      =================================== */}

                    <Box sx={{ minWidth: 0 }}>
                      <Stack
                        direction="row"
                        gap={1}
                        alignItems="center"
                        mb={1}
                        flexWrap="wrap"
                      >
                        <Chip
                          label={template.test_code}
                          size="small"
                          sx={{
                            background: "#EAF2FF",
                            color: "#1565C0",
                            fontWeight: 700,
                          }}
                        />

                        <Chip
                          label={template.category || "Other"}
                          size="small"
                          variant="outlined"
                        />
                      </Stack>

                      <Typography variant="h6" fontWeight={700}>
                        {template.test_name}
                      </Typography>

                      <Typography color="text.secondary" noWrap>
                        {template.description || "No description"}
                      </Typography>

                      <Typography variant="body2" mt={1} fontWeight={600}>
                        {template.parameters?.length || 0} parameters
                      </Typography>
                    </Box>

                    {/* ==================================
                          Actions
                      =================================== */}

                    <Stack direction="row" spacing={1} flexShrink={0}>
                      {/* View */}

                      <IconButton
                        title="View Template"
                        onClick={() =>
                          navigate(
                            `/laboratory/templates/${encodeURIComponent(
                              template.test_code,
                            )}`,
                          )
                        }
                      >
                        <VisibilityOutlinedIcon />
                      </IconButton>

                      {/* Edit */}

                      <IconButton
                        title="Edit Template"
                        onClick={() =>
                          navigate(
                            `/laboratory/templates/${encodeURIComponent(
                              template.test_code,
                            )}/edit`,
                          )
                        }
                      >
                        <EditOutlinedIcon />
                      </IconButton>

                      {/* Delete */}

                      <IconButton
                        color="error"
                        title="Delete Template"
                        onClick={() => handleDelete(template.test_code)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Stack>
                  </Stack>
                </Card>
              ))}
            </Box>
          )}
        </Container>
      </Box>
    </Box>
  );
}
