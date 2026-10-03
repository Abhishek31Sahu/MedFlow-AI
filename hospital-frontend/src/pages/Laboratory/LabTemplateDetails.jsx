import { useEffect, useState } from "react";

import {
  Box,
  Button,
  Card,
  Chip,
  CircularProgress,
  Divider,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import EditOutlinedIcon from "@mui/icons-material/EditOutlined";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

import { useNavigate, useParams } from "react-router-dom";

import { getTemplate } from "../../services/labTemplateApi";

export default function LabTemplateDetails() {
  const { id } = useParams();

  const navigate = useNavigate();

  const [template, setTemplate] = useState(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadTemplate = async () => {
      try {
        const response = await getTemplate(id);

        setTemplate(response?.data || response);
      } catch (error) {
        console.error(error);

        alert("Unable to load template.");

        navigate("/laboratory/templates");
      } finally {
        setLoading(false);
      }
    };

    loadTemplate();
  }, [id, navigate]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" py={10}>
        <CircularProgress />
      </Box>
    );
  }

  if (!template) {
    return null;
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}

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
            {template.test_name}
          </Typography>

          <Typography color="text.secondary" mt={0.5}>
            Laboratory Test Template
          </Typography>
        </Box>

        <Stack direction="row" spacing={1}>
          <Button
            variant="outlined"
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate("/laboratory/templates")}
          >
            Back to List
          </Button>

          <Button
            variant="contained"
            startIcon={<EditOutlinedIcon />}
            onClick={() =>
              navigate(`/laboratory/templates/${template.test_code}`)
            }
          >
            Edit Template
          </Button>
        </Stack>
      </Stack>

      {/* Information */}

      <Card
        elevation={0}
        sx={{
          border: "1px solid #E2E8F0",
          borderRadius: 3,
          mb: 3,
        }}
      >
        <Box sx={{ p: 3 }}>
          <Typography variant="h6" fontWeight={700} mb={3}>
            Test Information
          </Typography>

          <Stack
            direction={{
              xs: "column",
              md: "row",
            }}
            divider={<Divider flexItem />}
            spacing={3}
          >
            <Box sx={{ flex: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Test Code
              </Typography>

              <Typography fontWeight={600}>{template.test_code}</Typography>
            </Box>

            <Box sx={{ flex: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Test Name
              </Typography>

              <Typography fontWeight={600}>{template.test_name}</Typography>
            </Box>

            <Box sx={{ flex: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Category
              </Typography>

              <Box mt={0.5}>
                <Chip
                  label={template.category}
                  color="primary"
                  variant="outlined"
                  size="small"
                />
              </Box>
            </Box>
          </Stack>

          <Box mt={3}>
            <Typography variant="caption" color="text.secondary">
              Description
            </Typography>

            <Typography mt={0.5}>
              {template.description || "No description available."}
            </Typography>
          </Box>
        </Box>
      </Card>

      {/* Parameters */}

      <Card
        elevation={0}
        sx={{
          border: "1px solid #E2E8F0",
          borderRadius: 3,
        }}
      >
        <Box sx={{ p: 3 }}>
          <Stack direction="row" justifyContent="space-between" mb={2}>
            <Typography variant="h6" fontWeight={700}>
              Parameters
            </Typography>

            <Chip
              label={`${template.parameters?.length || 0} Parameters`}
              size="small"
            />
          </Stack>

          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>
                    <strong>Code</strong>
                  </TableCell>

                  <TableCell>
                    <strong>Name</strong>
                  </TableCell>

                  <TableCell>
                    <strong>Unit</strong>
                  </TableCell>

                  <TableCell>
                    <strong>Value Type</strong>
                  </TableCell>

                  <TableCell>
                    <strong>Reference Range</strong>
                  </TableCell>

                  <TableCell>
                    <strong>Required</strong>
                  </TableCell>
                </TableRow>
              </TableHead>

              <TableBody>
                {template.parameters?.map((parameter) => (
                  <TableRow key={parameter.id}>
                    <TableCell>{parameter.code}</TableCell>

                    <TableCell>{parameter.name}</TableCell>

                    <TableCell>{parameter.unit || "-"}</TableCell>

                    <TableCell>{parameter.value_type}</TableCell>

                    <TableCell>
                      {parameter.reference_low ?? "-"} -{" "}
                      {parameter.reference_high ?? "-"}
                    </TableCell>

                    <TableCell>
                      {parameter.required ? (
                        <Chip label="Yes" size="small" color="success" />
                      ) : (
                        <Chip label="No" size="small" />
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      </Card>
    </Box>
  );
}
