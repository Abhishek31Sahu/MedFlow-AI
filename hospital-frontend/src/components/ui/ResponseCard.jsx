import {
  Box,
  Paper,
  Stack,
  Chip,
  Typography,
  Button,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  CircularProgress,
} from "@mui/material";

import CheckCircleRoundedIcon from "@mui/icons-material/CheckCircleRounded";
import CancelRoundedIcon from "@mui/icons-material/CancelRounded";
import WarningAmberRoundedIcon from "@mui/icons-material/WarningAmberRounded";

/**
 * ResponseCard
 * ------------
 * Renders the backend's standardized `ResponseOutput` shape
 * (graph/models/response.py). This is the ONE render path for
 * every agent (patient, encounter, medication, observation,
 * appointment, summary) and every clinical workflow (admission,
 * discharge, transfer, lab order, appointment booking/reschedule).
 *
 * Layout is fixed by `status` — success / error / action_required /
 * in_progress — never by `category`, so a doctor sees the same card
 * shape every time, whichever agent or workflow answered.
 *
 * This is separate from `InterruptRenderer` / `MedicationReview` /
 * `AppointmentConfirmation` — those handle LangGraph interrupts that
 * need a specific interactive form. ResponseCard is for the plain
 * "here's what happened" answer that comes back from response_agent.
 *
 * Usage:
 *   <ResponseCard response={message.response} onReply={sendMessage} />
 */

const STATUS_META = {
  success: {
    icon: CheckCircleRoundedIcon,
    color: "success",
    border: "success.main",
    label: "Done",
  },
  error: {
    icon: CancelRoundedIcon,
    color: "error",
    border: "error.main",
    label: "Failed",
  },
  action_required: {
    icon: WarningAmberRoundedIcon,
    color: "warning",
    border: "warning.main",
    label: "Needs input",
  },
  in_progress: {
    icon: null,
    color: "info",
    border: "info.main",
    label: "In progress",
  },
};

const EMPHASIS_COLOR = {
  normal: { bg: "grey.50", border: "grey.300", text: "text.primary" },
  warning: { bg: "warning.50", border: "warning.light", text: "warning.dark" },
  critical: { bg: "error.50", border: "error.light", text: "error.dark" },
};

function formatLabel(value) {
  return String(value)
    .split("_")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

const ISO_DATETIME = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/;

function formatCell(value) {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "string" && ISO_DATETIME.test(value)) {
    const d = new Date(value);
    if (!Number.isNaN(d.getTime())) return d.toLocaleString();
  }
  return String(value);
}

export default function ResponseCard({ response, onReply }) {
  if (!response) return null;

  // `tables` is the current shape; `table` is accepted for older payloads.
  const tables = response.tables ?? (response.table ? [response.table] : []);

  const meta = STATUS_META[response.status] || STATUS_META.success;
  const StatusIcon = meta.icon;

  return (
    <Paper
      variant="outlined"
      sx={{
        borderRadius: 2,
        borderLeft: 4,
        borderLeftColor: meta.border,
        maxWidth: 560,
        overflow: "hidden",
      }}
    >
      {/* Header */}
      <Stack
        direction="row"
        alignItems="flex-start"
        justifyContent="space-between"
        spacing={1.5}
        sx={{ px: 2, pt: 2 }}
      >
        <Stack direction="row" spacing={1.25} alignItems="flex-start">
          {StatusIcon ? (
            <StatusIcon color={meta.color} sx={{ mt: "1px", fontSize: 20 }} />
          ) : (
            <CircularProgress size={18} thickness={5} sx={{ mt: "3px" }} />
          )}
          <Box>
            <Typography
              variant="subtitle2"
              sx={{ fontWeight: 600, lineHeight: 1.3 }}
            >
              {response.title}
            </Typography>
            <Typography variant="caption" color="text.disabled">
              {formatLabel(response.category)}
            </Typography>
          </Box>
        </Stack>

        <Chip
          label={meta.label}
          color={meta.color}
          size="small"
          variant="outlined"
          sx={{ fontWeight: 500 }}
        />
      </Stack>

      {/* Message */}
      <Typography variant="body2" color="text.secondary" sx={{ px: 2, pt: 1 }}>
        {response.message}
      </Typography>

      {/* Highlights — the "read in 2 seconds" facts */}
      {response.highlights?.length > 0 && (
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: { xs: "1fr 1fr", sm: "1fr 1fr 1fr" },
            gap: 1,
            px: 2,
            pt: 1.5,
          }}
        >
          {response.highlights.map((h, i) => {
            const c = EMPHASIS_COLOR[h.emphasis || "normal"];
            return (
              <Box
                key={i}
                sx={{
                  border: "1px solid",
                  borderColor: c.border,
                  bgcolor: c.bg,
                  borderRadius: 1,
                  px: 1.25,
                  py: 0.75,
                }}
              >
                <Typography
                  variant="caption"
                  sx={{
                    textTransform: "uppercase",
                    opacity: 0.6,
                    display: "block",
                  }}
                >
                  {h.label}
                </Typography>
                <Typography
                  variant="body2"
                  sx={{ fontWeight: 600, color: c.text }}
                >
                  {h.value}
                </Typography>
              </Box>
            );
          })}
        </Box>
      )}

      {/* Tables — built from the raw backend data, one per list
          (e.g. patient summary: medications, observations, ...) */}
      {tables.map((table, t) => (
        <Box key={t} sx={{ px: 2, pt: 1.5 }}>
          {table.title && (
            <Typography
              variant="caption"
              sx={{ fontWeight: 600, display: "block", mb: 0.5 }}
            >
              {table.title}
            </Typography>
          )}
          <Box
            sx={{
              overflow: "auto",
              maxHeight: 320,
              border: "1px solid",
              borderColor: "grey.200",
              borderRadius: 1,
            }}
          >
            <Table size="small" stickyHeader>
              <TableHead>
                <TableRow>
                  {table.columns.map((col) => (
                    <TableCell
                      key={col}
                      sx={{
                        color: "text.secondary",
                        fontSize: 11,
                        fontWeight: 600,
                        bgcolor: "grey.50",
                      }}
                    >
                      {col}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {table.rows.map((row, i) => (
                  <TableRow key={i}>
                    {table.columns.map((col) => (
                      <TableCell key={col} sx={{ fontSize: 13 }}>
                        {formatCell(row[col])}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Box>
        </Box>
      ))}

      {/* Workflow progress — only present mid multi-step workflow */}
      {response.workflow && (
        <Box
          sx={{
            mx: 2,
            mt: 1.5,
            px: 1.5,
            py: 0.75,
            bgcolor: "grey.50",
            borderRadius: 1,
          }}
        >
          <Typography variant="caption" color="text.secondary">
            <Box
              component="span"
              sx={{ fontWeight: 600, color: "text.primary" }}
            >
              {formatLabel(response.workflow.name)}
            </Box>
            {" · "}
            {response.workflow.status.replaceAll("_", " ").toLowerCase()}
            {response.workflow.step && ` · ${response.workflow.step}`}
          </Typography>
        </Box>
      )}

      {/* Suggested replies — only rendered when status is action_required */}
      {response.suggested_replies?.length > 0 && (
        <Stack
          direction="row"
          flexWrap="wrap"
          gap={1}
          sx={{ px: 2, pt: 1.5, pb: 2 }}
        >
          {response.suggested_replies.map((reply, i) => (
            <Button
              key={i}
              size="small"
              variant="outlined"
              onClick={() => onReply?.(reply)}
              sx={{ borderRadius: 5, textTransform: "none" }}
            >
              {reply}
            </Button>
          ))}
        </Stack>
      )}

      {!response.suggested_replies?.length && <Box sx={{ pb: 2 }} />}
    </Paper>
  );
}
