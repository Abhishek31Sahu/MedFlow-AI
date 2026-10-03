import { Avatar, Box, Paper, Typography } from "@mui/material";

import SmartToyIcon from "@mui/icons-material/SmartToy";
import PersonIcon from "@mui/icons-material/Person";
import MedicationIcon from "@mui/icons-material/Medication";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { Chip, Stack } from "@mui/material";

import AppointmentList from "./AppointmentList";
import ResponseCard from "./ResponseCard";

/**
 * MessageBubble
 * -------------
 * Every AI message that carries `message.response` (the
 * standardized ResponseOutput from response_agent — see
 * graph/models/response.py) renders through <ResponseCard />, so a
 * doctor sees the identical card layout whichever agent or workflow
 * answered.
 *
 * The block below `message.response` is the LEGACY path, kept only
 * so older messages already sitting in a chat's history (saved
 * before this change) still render instead of going blank. Once
 * useChat.js attaches `response` on every AI message, new messages
 * never touch this path.
 */
export default function MessageBubble({ message, onSuggestedReply }) {
  if (!message) return null;

  const isUser = message.role === "user";
  const structured = message.response;

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        mb: 2,
        width: "100%",
      }}
    >
      {!isUser && (
        <Avatar sx={{ bgcolor: "#1976d2", mr: 1, flexShrink: 0 }}>
          <SmartToyIcon />
        </Avatar>
      )}

      {!isUser && structured ? (
        // ============================================================
        // STANDARDIZED PATH — every agent / workflow renders the same
        // ============================================================
        <Box sx={{ maxWidth: "80%", minWidth: 0 }}>
          <ResponseCard response={structured} onReply={onSuggestedReply} />

          {message.timestamp && (
            <Typography
              variant="caption"
              sx={{ display: "block", mt: 0.5, ml: 0.5, opacity: 0.6 }}
            >
              {message.timestamp}
            </Typography>
          )}
        </Box>
      ) : (
        // ============================================================
        // LEGACY PATH — old messages without a `response` payload
        // ============================================================
        <LegacyBubble message={message} isUser={isUser} />
      )}

      {isUser && (
        <Avatar sx={{ bgcolor: "#2e7d32", ml: 1, flexShrink: 0 }}>
          <PersonIcon />
        </Avatar>
      )}
    </Box>
  );
}

/* ============================================================
   LEGACY BUBBLE (pre-standardization message shape)
============================================================ */

function LegacyBubble({ message, isUser }) {
  const data = message.data || {};

  const hasResults = Array.isArray(data.results) && data.results.length > 0;
  const hasPatient = !!data.patient;
  const hasMedications =
    Array.isArray(data.medications) && data.medications.length > 0;
  const hasRecommendations =
    Array.isArray(data.recommendations) && data.recommendations.length > 0;

  return (
    <Paper
      elevation={2}
      sx={{
        maxWidth: "80%",
        minWidth: 0,
        px: 2,
        py: 1.5,
        borderRadius: 3,
        bgcolor: isUser ? "#1976d2" : "#fff",
        color: isUser ? "#fff" : "#000",
      }}
    >
      {message.title && (
        <Typography variant="subtitle1" fontWeight={700} sx={{ mb: 1 }}>
          {message.title}
        </Typography>
      )}

      {message.content && (
        <Typography
          variant="body1"
          sx={{ whiteSpace: "pre-wrap", lineHeight: 1.7 }}
        >
          {message.content}
        </Typography>
      )}

      {message.data?.appointments && (
        <AppointmentList appointments={message.data.appointments} />
      )}

      {!isUser && hasPatient && (
        <Box sx={{ mt: 2, p: 2, bgcolor: "#F5F7FA", borderRadius: 2 }}>
          <Typography fontWeight={700} sx={{ mb: 1.5 }}>
            Patient Information
          </Typography>

          <Stack spacing={1}>
            <InfoRow label="Patient ID" value={data.patient?.id} />
            <InfoRow label="Name" value={getPatientName(data.patient)} />
            <InfoRow label="Gender" value={data.patient?.gender} />
            <InfoRow label="Birth Date" value={data.patient?.birthDate} />
            {data.patient?.active !== undefined && (
              <InfoRow
                label="Status"
                value={data.patient.active ? "Active" : "Inactive"}
              />
            )}
          </Stack>
        </Box>
      )}

      {!isUser && hasMedications && (
        <Box sx={{ mt: 2, p: 2, bgcolor: "#F5F7FA", borderRadius: 2 }}>
          <Stack
            direction="row"
            spacing={1}
            alignItems="center"
            sx={{ mb: 1.5 }}
          >
            <MedicationIcon color="primary" fontSize="small" />
            <Typography variant="subtitle2" fontWeight={700}>
              Medications
            </Typography>
          </Stack>

          <Stack spacing={1}>
            {data.medications.map((medication, index) => (
              <Box
                key={
                  medication?.id ||
                  `${medication?.medicine || "medicine"}-${index}`
                }
                sx={{
                  p: 1.5,
                  bgcolor: "#fff",
                  borderRadius: 2,
                  border: "1px solid #e5e7eb",
                }}
              >
                <Stack
                  direction={{ xs: "column", sm: "row" }}
                  justifyContent="space-between"
                  alignItems={{ xs: "flex-start", sm: "center" }}
                  spacing={1}
                >
                  <Box>
                    <Typography fontWeight={600}>
                      {medication?.medicine || "-"}
                    </Typography>
                    {medication?.id && (
                      <Typography variant="caption" color="text.secondary">
                        Medication ID: {medication.id}
                      </Typography>
                    )}
                  </Box>

                  <Chip
                    label={medication?.dosage || "Dosage not specified"}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                </Stack>
              </Box>
            ))}
          </Stack>
        </Box>
      )}

      {!isUser && hasRecommendations && (
        <Box sx={{ mt: 2, p: 2, bgcolor: "#F5F7FA", borderRadius: 2 }}>
          <Stack
            direction="row"
            spacing={1}
            alignItems="center"
            sx={{ mb: 1.5 }}
          >
            <MedicationIcon color="primary" />
            <Typography variant="subtitle2" fontWeight={700}>
              AI Medication Review
            </Typography>
          </Stack>

          <Stack spacing={1.5}>
            {data.recommendations.map((recommendation, index) => (
              <MedicationRecommendation
                key={recommendation?.medicine_name || index}
                recommendation={recommendation}
              />
            ))}
          </Stack>

          {data.summary && (
            <Box
              sx={{
                mt: 2,
                p: 1.5,
                bgcolor: "#fff",
                borderRadius: 2,
                border: "1px solid #e5e7eb",
              }}
            >
              <Typography variant="subtitle2" fontWeight={700} sx={{ mb: 0.5 }}>
                Summary
              </Typography>
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ lineHeight: 1.6 }}
              >
                {data.summary}
              </Typography>
            </Box>
          )}

          {data.requires_doctor_approval && (
            <Box
              sx={{
                mt: 2,
                p: 1.5,
                bgcolor: "#FFF8E1",
                borderRadius: 2,
                border: "1px solid #FFE082",
              }}
            >
              <Stack direction="row" spacing={1} alignItems="center">
                <WarningAmberIcon sx={{ color: "#F57C00" }} />
                <Typography
                  variant="body2"
                  fontWeight={700}
                  sx={{ color: "#8A4B00" }}
                >
                  Doctor approval required
                </Typography>
              </Stack>
            </Box>
          )}
        </Box>
      )}

      {!isUser && hasResults && (
        <Box sx={{ mt: 2, p: 2, bgcolor: "#F5F7FA", borderRadius: 2 }}>
          <Typography variant="subtitle2" fontWeight={700} sx={{ mb: 1.5 }}>
            Observation Results
          </Typography>

          <Stack spacing={1}>
            {data.results.map((result, index) => (
              <Box
                key={`${result?.test || "result"}-${result?.date || index}-${index}`}
                sx={{
                  p: 1.5,
                  bgcolor: "#fff",
                  borderRadius: 2,
                  border: "1px solid #e5e7eb",
                }}
              >
                <Stack
                  direction={{ xs: "column", sm: "row" }}
                  justifyContent="space-between"
                  alignItems={{ xs: "flex-start", sm: "center" }}
                  spacing={1}
                >
                  <Box>
                    <Typography fontWeight={600}>
                      {result?.test || "-"}
                    </Typography>
                    {result?.date && (
                      <Typography variant="caption" color="text.secondary">
                        {formatDate(result.date)}
                      </Typography>
                    )}
                  </Box>

                  <Stack direction="row" spacing={1} alignItems="center">
                    <Typography fontWeight={700}>
                      {result?.value ?? "-"} {result?.unit || ""}
                    </Typography>
                    {result?.status && (
                      <Chip
                        label={result.status}
                        size="small"
                        color={
                          result.status?.toString().toLowerCase() === "final"
                            ? "success"
                            : "default"
                        }
                      />
                    )}
                  </Stack>
                </Stack>
              </Box>
            ))}
          </Stack>
        </Box>
      )}

      {!isUser &&
        data &&
        !hasResults &&
        !hasPatient &&
        !hasMedications &&
        !hasRecommendations &&
        renderOtherData(data)}

      {message.timestamp && (
        <Typography
          variant="caption"
          sx={{ display: "block", mt: 1, textAlign: "right", opacity: 0.7 }}
        >
          {message.timestamp}
        </Typography>
      )}
    </Paper>
  );
}

function MedicationRecommendation({ recommendation }) {
  const type = recommendation?.recommendation?.toString().toLowerCase();
  const isContinue = type === "continue";
  const isConsiderStop = type === "consider_stop";

  return (
    <Box
      sx={{
        p: 1.5,
        bgcolor: "#fff",
        borderRadius: 2,
        border: "1px solid #e5e7eb",
      }}
    >
      <Stack spacing={1}>
        <Stack
          direction={{ xs: "column", sm: "row" }}
          justifyContent="space-between"
          alignItems={{ xs: "flex-start", sm: "center" }}
          spacing={1}
        >
          <Typography fontWeight={700}>
            {recommendation?.medicine_name || "-"}
          </Typography>
          <Chip
            icon={
              isContinue ? (
                <CheckCircleIcon />
              ) : isConsiderStop ? (
                <WarningAmberIcon />
              ) : undefined
            }
            label={formatRecommendation(recommendation?.recommendation)}
            size="small"
            color={
              isContinue ? "success" : isConsiderStop ? "warning" : "default"
            }
          />
        </Stack>

        {recommendation?.reason && (
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ lineHeight: 1.6 }}
          >
            {recommendation.reason}
          </Typography>
        )}
      </Stack>
    </Box>
  );
}

function renderOtherData(data) {
  const entries = Object.entries(data);
  if (entries.length === 0) return null;

  return (
    <Box sx={{ mt: 2, p: 2, bgcolor: "#F5F7FA", borderRadius: 2 }}>
      {entries.map(([key, value]) => {
        if (value !== null && typeof value === "object") return null;
        return (
          <Typography key={key} variant="body2" sx={{ mb: 0.5 }}>
            <strong>{formatLabel(key)}:</strong> {String(value)}
          </Typography>
        );
      })}
    </Box>
  );
}

function InfoRow({ label, value }) {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        gap: 2,
      }}
    >
      <Typography color="text.secondary" fontSize={14}>
        {label}
      </Typography>
      <Typography
        fontWeight={600}
        fontSize={14}
        sx={{ textAlign: "right", wordBreak: "break-word" }}
      >
        {formatValue(value)}
      </Typography>
    </Box>
  );
}

/**
 * Fixed: `name` may already be a flattened plain string ("Harsh
 * Kumar") — the earlier bug came from assuming it was always a raw
 * FHIR HumanName array and indexing a string by [0], which grabs a
 * single character instead of the name.
 */
function getPatientName(patient) {
  const raw = patient?.name;

  if (!raw) return "-";

  if (typeof raw === "string") {
    return raw.trim() || "-";
  }

  const name = Array.isArray(raw) ? raw[0] : raw;
  if (!name || typeof name !== "object") return "-";

  const given = Array.isArray(name.given)
    ? name.given.join(" ")
    : name.given || "";
  const family = name.family || "";

  return `${given} ${family}`.trim() || "-";
}

function formatValue(value) {
  if (value === null || value === undefined || value === "") return "-";
  if (Array.isArray(value))
    return value.map((item) => formatValue(item)).join(", ");

  if (typeof value === "object") {
    if (value.given || value.family) {
      const given = Array.isArray(value.given)
        ? value.given.join(" ")
        : value.given || "";
      const family = value.family || "";
      return `${given} ${family}`.trim() || "-";
    }
    return JSON.stringify(value);
  }

  return String(value);
}

function formatDate(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}

function formatLabel(value) {
  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatRecommendation(value) {
  if (!value) return "Unknown";
  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}
