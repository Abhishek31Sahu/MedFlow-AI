import React, { useEffect, useState } from "react";

import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Grid,
  Stack,
  Typography,
} from "@mui/material";

import PersonIcon from "@mui/icons-material/Person";
import ScienceIcon from "@mui/icons-material/Science";
import MedicationIcon from "@mui/icons-material/Medication";
import EventIcon from "@mui/icons-material/Event";
import DescriptionIcon from "@mui/icons-material/Description";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import LocalHospitalIcon from "@mui/icons-material/LocalHospital";
import MonitorHeartOutlinedIcon from "@mui/icons-material/MonitorHeartOutlined";
import HealingOutlinedIcon from "@mui/icons-material/HealingOutlined";
import AssignmentOutlinedIcon from "@mui/icons-material/AssignmentOutlined";
import MedicalInformationOutlinedIcon from "@mui/icons-material/MedicalInformationOutlined";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";

import { useNavigate, useParams } from "react-router-dom";

import { getPatient } from "../../services/patientService";

export default function PatientDetails() {
  const { patientId } = useParams();
  const navigate = useNavigate();

  const [patient, setPatient] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadPatient();
  }, [patientId]);

  const loadPatient = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getPatient(patientId);

      console.log("Patient Details:", data);

      setPatient(data);
    } catch (err) {
      console.error(err);

      setError(err.response?.data?.detail || "Unable to load patient details.");
    } finally {
      setLoading(false);
    }
  };

  const getPatientName = () => {
    if (!patient) return "Patient";

    // FHIR style name
    if (Array.isArray(patient.name)) {
      const name = patient.name[0];

      return (
        [...(name?.given || []), name?.family].filter(Boolean).join(" ") ||
        "Patient"
      );
    }

    // Normal API style
    return patient.name || patient.full_name || "Patient";
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          mt: 8,
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!patient) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Patient not found.</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* =====================================================
          HEADER
      ===================================================== */}

      <Card
        sx={{
          borderRadius: 3,
          mb: 3,
        }}
      >
        <CardContent sx={{ p: 3 }}>
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
          >
            <Stack direction="row" spacing={2} alignItems="center">
              <Box
                sx={{
                  width: 64,
                  height: 64,
                  borderRadius: "50%",
                  bgcolor: "#eaf3ff",
                  color: "primary.main",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <PersonIcon sx={{ fontSize: 36 }} />
              </Box>

              <Box>
                <Typography variant="h4" fontWeight={800}>
                  {getPatientName()}
                </Typography>

                <Typography color="text.secondary" sx={{ mt: 0.5 }}>
                  Patient ID: {patient.id}
                </Typography>
              </Box>
            </Stack>

            <Chip
              label={patient.active ? "Active Patient" : "Inactive Patient"}
              color={patient.active ? "success" : "default"}
            />
          </Stack>
        </CardContent>
      </Card>

      {/* =====================================================
          BASIC INFORMATION
      ===================================================== */}

      <Card
        sx={{
          borderRadius: 3,
          mb: 3,
        }}
      >
        <CardContent sx={{ p: 3 }}>
          <Typography variant="h6" fontWeight={800} mb={2}>
            Patient Information
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={3}>
              <InfoItem label="Patient ID" value={patient.id} />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <InfoItem label="Name" value={getPatientName()} />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <InfoItem label="Gender" value={patient.gender} />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <InfoItem label="Date of Birth" value={patient.birthDate} />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* =====================================================
          CLINICAL INFORMATION CARDS
      ===================================================== */}

      <Typography variant="h6" fontWeight={800} mb={2}>
        Clinical Information
      </Typography>

      <Grid container spacing={2.5}>
        {/* Laboratory Reports */}

        <Grid item xs={12} sm={6} md={4}>
          <FeatureCard
            icon={<ScienceIcon />}
            title="Laboratory Reports"
            description="View completed diagnostic reports and laboratory results."
            buttonText="View Reports"
            onClick={() =>
              navigate(`/doctor/patients/${patientId}/lab-reports`)
            }
          />
        </Grid>

        {/* Laboratory Orders */}

        <Grid item xs={12} sm={6} md={4}>
          <FeatureCard
            icon={<AssignmentOutlinedIcon />}
            title="Laboratory Orders"
            description="View laboratory tests ordered for this patient."
            buttonText="View Orders"
            onClick={() => navigate(`/doctor/patients/${patientId}/lab-orders`)}
          />
        </Grid>

        {/* Medications */}

        <Grid item xs={12} sm={6} md={4}>
          <FeatureCard
            icon={<MedicationIcon />}
            title="Medications"
            description="View active and historical medications."
            buttonText="View Medications"
            onClick={() =>
              navigate(`/doctor/patients/${patientId}/medications`)
            }
          />
        </Grid>

        {/* Observations */}

        <Grid item xs={12} sm={6} md={4}>
          <FeatureCard
            icon={<VisibilityOutlinedIcon />}
            title="Observations"
            description="View laboratory and clinical observations."
            buttonText="View Observations"
            onClick={() =>
              navigate(`/doctor/patients/${patientId}/observations`)
            }
          />
        </Grid>

        {/* Appointments */}

        <Grid item xs={12} sm={6} md={4}>
          <FeatureCard
            icon={<EventIcon />}
            title="Appointments"
            description="View upcoming and previous patient appointments."
            buttonText="View Appointments"
            onClick={() =>
              navigate(`/doctor/patients/${patientId}/appointments`)
            }
          />
        </Grid>

        {/* Encounters */}

        <Grid item xs={12} sm={6} md={4}>
          <FeatureCard
            icon={<LocalHospitalIcon />}
            title="Encounters & Visits"
            description="View hospital visits, consultations and encounter history."
            buttonText="View Encounters"
            onClick={() => navigate(`/doctor/patients/${patientId}/encounters`)}
          />
        </Grid>

        {/* Medical Records */}

        <Grid item xs={12} sm={6} md={4}>
          <FeatureCard
            icon={<MedicalInformationOutlinedIcon />}
            title="Medical Records"
            description="View the patient's clinical records and documents."
            buttonText="View Records"
            onClick={() =>
              navigate(`/doctor/patients/${patientId}/medical-records`)
            }
          />
        </Grid>

        {/* Vital Signs */}

        <Grid item xs={12} sm={6} md={4}>
          <FeatureCard
            icon={<MonitorHeartOutlinedIcon />}
            title="Vital Signs"
            description="View blood pressure, heart rate, temperature and other vitals."
            buttonText="View Vitals"
            onClick={() => navigate(`/doctor/patients/${patientId}/vitals`)}
          />
        </Grid>

        {/* Conditions */}

        <Grid item xs={12} sm={6} md={4}>
          <FeatureCard
            icon={<HealingOutlinedIcon />}
            title="Conditions & Diagnoses"
            description="View known medical conditions and diagnoses."
            buttonText="View Conditions"
            onClick={() => navigate(`/doctor/patients/${patientId}/conditions`)}
          />
        </Grid>

        {/* Care Plan */}

        <Grid item xs={12} sm={6} md={4}>
          <FeatureCard
            icon={<DescriptionIcon />}
            title="Care Plan"
            description="View treatment plans and ongoing clinical care."
            buttonText="View Care Plan"
            onClick={() => navigate(`/doctor/patients/${patientId}/care-plan`)}
          />
        </Grid>
      </Grid>
    </Box>
  );
}

/* ============================================================
   INFO ITEM
============================================================ */

function InfoItem({ label, value }) {
  return (
    <Box>
      <Typography fontSize={13} color="text.secondary">
        {label}
      </Typography>

      <Typography fontWeight={600} sx={{ mt: 0.5 }}>
        {value || "-"}
      </Typography>
    </Box>
  );
}

/* ============================================================
   FEATURE CARD
============================================================ */

function FeatureCard({ icon, title, description, buttonText, onClick }) {
  return (
    <Card
      sx={{
        height: "100%",
        borderRadius: 3,
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
          p: 3,
          height: "100%",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Box
          sx={{
            width: 52,
            height: 52,
            borderRadius: 2,
            bgcolor: "#eef5ff",
            color: "primary.main",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            mb: 2,
          }}
        >
          {icon}
        </Box>

        <Typography variant="h6" fontWeight={700}>
          {title}
        </Typography>

        <Typography
          color="text.secondary"
          fontSize={14}
          sx={{
            mt: 1,
            lineHeight: 1.6,
            flex: 1,
          }}
        >
          {description}
        </Typography>

        <Button
          variant="outlined"
          endIcon={<ArrowForwardIcon />}
          sx={{
            mt: 2,
            alignSelf: "flex-start",
          }}
          onClick={onClick}
        >
          {buttonText}
        </Button>
      </CardContent>
    </Card>
  );
}
