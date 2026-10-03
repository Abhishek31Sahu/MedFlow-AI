import React, { useMemo, useState } from "react";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  FormControl,
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import { submitMedicationReview } from "../../services/dischargeService";

export default function MedicationReview({ interrupt, threadId, onComplete }) {
  const patient = interrupt?.patient;
  const medications = interrupt?.medications || [];
  const aiReview = interrupt?.ai_review;

  const [decisions, setDecisions] = useState(() =>
    medications.map((medication) => ({
      medication_id: medication.id,
      medicine_name: medication.medicine,
      final_action: "continue",
      accepted_ai_recommendation: true,
      dosage: null,
      frequency: null,
      override_reason: null,
    })),
  );

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const getPatientName = () => {
    const name = patient?.name?.[0];

    if (!name) return "-";

    const given = Array.isArray(name.given)
      ? name.given.join(" ")
      : name.given || "";

    const family = name.family || "";

    return `${given} ${family}`.trim() || "-";
  };

  const getRecommendation = (medicineName) => {
    return (
      aiReview?.recommendations?.find(
        (item) =>
          item.medicine_name?.toLowerCase() === medicineName?.toLowerCase(),
      ) || null
    );
  };

  const updateDecision = (index, field, value) => {
    setDecisions((prev) =>
      prev.map((item, i) => {
        if (i !== index) return item;

        return {
          ...item,
          [field]: value,
        };
      }),
    );
  };

  const handleActionChange = (index, action) => {
    const medication = medications[index];
    const aiRecommendation = getRecommendation(medication.medicine);

    let accepted = false;

    if (aiRecommendation) {
      if (
        aiRecommendation.recommendation === "continue" &&
        action === "continue"
      ) {
        accepted = true;
      }

      if (
        aiRecommendation.recommendation === "consider_stop" &&
        action === "stop"
      ) {
        accepted = true;
      }

      if (
        aiRecommendation.recommendation === "consider_modify" &&
        action === "modify"
      ) {
        accepted = true;
      }
    }

    setDecisions((prev) =>
      prev.map((item, i) => {
        if (i !== index) return item;

        return {
          ...item,
          final_action: action,
          accepted_ai_recommendation: accepted,

          dosage: action === "modify" ? item.dosage || "" : null,

          frequency: action === "modify" ? item.frequency || "" : null,

          override_reason: accepted ? null : item.override_reason || "",
        };
      }),
    );
  };

  const validate = () => {
    for (const decision of decisions) {
      if (decision.final_action === "modify") {
        if (!decision.dosage?.trim()) {
          return `Enter dosage for ${decision.medicine_name}.`;
        }

        if (!decision.frequency?.trim()) {
          return `Enter frequency for ${decision.medicine_name}.`;
        }
      }

      if (!decision.accepted_ai_recommendation) {
        if (!decision.override_reason?.trim()) {
          return `Enter override reason for ${decision.medicine_name}.`;
        }
      }
    }

    return null;
  };

  const handleSubmit = async () => {
    setError("");

    const validationError = validate();

    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      setSubmitting(true);

      const payload = {
        thread_id: threadId,

        doctor_decision: decisions.map((item) => ({
          medication_id: item.medication_id,
          medicine_name: item.medicine_name,
          final_action: item.final_action,
          accepted_ai_recommendation: item.accepted_ai_recommendation,

          dosage: item.final_action === "modify" ? item.dosage : null,

          frequency: item.final_action === "modify" ? item.frequency : null,

          override_reason: item.accepted_ai_recommendation
            ? null
            : item.override_reason,
        })),
      };

      console.log("Submitting medication review:", payload);

      const response = await submitMedicationReview(payload);

      onComplete?.(response);
    } catch (err) {
      console.error("Medication review submit error:", err);

      setError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to submit medication review.",
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card
      sx={{
        mt: 2,
        borderRadius: 3,
        border: "1px solid",
        borderColor: "divider",
      }}
    >
      <CardContent>
        <Stack spacing={2.5}>
          <Box>
            <Typography variant="h6" fontWeight={700}>
              Doctor Medication Review
            </Typography>

            <Typography variant="body2" color="text.secondary">
              Patient: {getPatientName()} ({patient?.id})
            </Typography>
          </Box>

          {aiReview?.summary && (
            <Alert severity="info">
              <Typography variant="body2" fontWeight={600}>
                AI Summary
              </Typography>

              <Typography variant="body2">{aiReview.summary}</Typography>
            </Alert>
          )}

          {aiReview?.requires_doctor_approval && (
            <Alert severity="warning">
              Doctor approval is required before continuing discharge.
            </Alert>
          )}

          {medications.map((medication, index) => {
            const decision = decisions[index];

            const recommendation = getRecommendation(medication.medicine);

            return (
              <Card
                key={medication.id}
                variant="outlined"
                sx={{
                  borderRadius: 2,
                }}
              >
                <CardContent>
                  <Stack spacing={2}>
                    <Box>
                      <Typography variant="subtitle1" fontWeight={700}>
                        {medication.medicine}
                      </Typography>

                      <Typography variant="body2" color="text.secondary">
                        Current dosage: {medication.dosage || "-"}
                      </Typography>
                    </Box>

                    {recommendation && (
                      <Box>
                        <Stack direction="row" spacing={1} alignItems="center">
                          <Typography variant="body2" fontWeight={600}>
                            AI Recommendation:
                          </Typography>

                          <Chip
                            size="small"
                            label={recommendation.recommendation.replace(
                              "_",
                              " ",
                            )}
                          />
                        </Stack>

                        <Typography
                          variant="body2"
                          color="text.secondary"
                          sx={{ mt: 1 }}
                        >
                          {recommendation.reason}
                        </Typography>
                      </Box>
                    )}

                    <Divider />

                    <FormControl>
                      <FormLabel>Doctor's Final Decision</FormLabel>

                      <RadioGroup
                        value={decision.final_action}
                        onChange={(event) =>
                          handleActionChange(index, event.target.value)
                        }
                      >
                        <FormControlLabel
                          value="continue"
                          control={<Radio />}
                          label="Continue"
                        />

                        <FormControlLabel
                          value="stop"
                          control={<Radio />}
                          label="Stop"
                        />

                        <FormControlLabel
                          value="modify"
                          control={<Radio />}
                          label="Modify"
                        />
                      </RadioGroup>
                    </FormControl>

                    {decision.final_action === "modify" && (
                      <Stack spacing={2}>
                        <TextField
                          fullWidth
                          label="New Dosage"
                          value={decision.dosage || ""}
                          onChange={(event) =>
                            updateDecision(index, "dosage", event.target.value)
                          }
                        />

                        <TextField
                          fullWidth
                          label="New Frequency"
                          value={decision.frequency || ""}
                          onChange={(event) =>
                            updateDecision(
                              index,
                              "frequency",
                              event.target.value,
                            )
                          }
                        />
                      </Stack>
                    )}

                    {!decision.accepted_ai_recommendation && (
                      <TextField
                        fullWidth
                        multiline
                        minRows={2}
                        label="Reason for overriding AI recommendation"
                        value={decision.override_reason || ""}
                        onChange={(event) =>
                          updateDecision(
                            index,
                            "override_reason",
                            event.target.value,
                          )
                        }
                      />
                    )}
                  </Stack>
                </CardContent>
              </Card>
            );
          })}

          {error && <Alert severity="error">{error}</Alert>}

          <Button
            variant="contained"
            size="large"
            onClick={handleSubmit}
            disabled={submitting || decisions.length === 0}
          >
            {submitting ? "Submitting..." : "Submit Medication Review"}
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
}
