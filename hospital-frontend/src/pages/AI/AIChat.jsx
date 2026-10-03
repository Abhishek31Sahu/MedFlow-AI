import { Box, Grid, Paper } from "@mui/material";

import InterruptRenderer from "../../components/ui/InterruptRenderer";
import Sidebar from "../../components/layout/Sidebar";
import Header from "../../components/layout/Header";

import ChatHeader from "../../components/common/ChatHeader";
import EmptyChat from "../../components/common/EmptyChat";
import MedicationReview from "../../components/ui/MedicationReview";
import MessageList from "../../components/ui/MessageList";
import TypingIndicator from "../../components/ui/TypingIndicator";
import AppointmentConfirmation from "../../components/ui/AppointmentConfirmation";
import ChatInput from "../../components/forms/ChatInput";

import { useChat } from "../../hook/useChat";

const SIDEBAR_WIDTH = 260;
const HEADER_HEIGHT = 64;

export default function AIChat() {
  const practitionerId = "1053";

  const {
    messages,
    loading,
    interrupt,
    threadId,
    sendMessage,
    selectBed,
    resolvePatient,
    newChat,
    clearInterrupt,
    onAppointmentConfirmation,
  } = useChat(practitionerId);

  const handleAppointmentConfirmation = async (confirmed) => {
    try {
      const response = await onAppointmentConfirmation({
        confirmed,
      });

      console.log("Appointment workflow resumed:", response);

      clearInterrupt();
    } catch (error) {
      console.error("Appointment confirmation error:", error);
    }
  };

  // Tapping a suggested reply chip on a ResponseCard (e.g. "Yes,
  // confirm" / "No, cancel" / a value for a missing workflow field)
  // just sends it through the normal chat pipe, same as if the
  // doctor had typed it.
  const handleSuggestedReply = (reply) => {
    sendMessage(reply);
  };

  return (
    <Box
      sx={{
        display: "grid",
        gridTemplateColumns: `${SIDEBAR_WIDTH}px 1fr`,
        gridTemplateRows: `${HEADER_HEIGHT}px 1fr`,
        gridTemplateAreas: `
          "sidebar header"
          "sidebar main"
        `,
        minHeight: "100vh",
      }}
    >
      {/* Sidebar */}

      <Box
        sx={{
          gridArea: "sidebar",
          width: SIDEBAR_WIDTH,
          height: "100vh",
          position: "sticky",
          top: 0,
          overflow: "hidden",
        }}
      >
        <Sidebar />
      </Box>

      {/* Header */}

      <Box
        sx={{
          gridArea: "header",
          height: HEADER_HEIGHT,
          position: "sticky",
          top: 0,
          zIndex: 10,
        }}
      >
        <Header />
      </Box>

      {/* Main */}

      <Box
        sx={{
          gridArea: "main",
          bgcolor: "#F5F7FB",
          p: 3,
          margin: 2,
          minWidth: 0,
        }}
      >
        <ChatHeader onNewChat={newChat} />

        <Grid container spacing={3}>
          {/* ================= CHAT ================= */}

          <Grid size={{ xs: 12, lg: 8 }}>
            <Paper
              elevation={3}
              sx={{
                borderRadius: 3,
                display: "flex",
                flexDirection: "column",
                height: "78vh",
                overflow: "hidden",
              }}
            >
              {/* Messages */}

              <Box
                sx={{
                  flex: 1,
                  overflowY: "auto",
                  bgcolor: "#FAFAFA",
                  p: 2,
                }}
              >
                {messages.length === 0 ? (
                  <EmptyChat onSuggestionClick={sendMessage} />
                ) : (
                  <>
                    {/*
                      MessageList renders the running transcript. Any
                      assistant message that carries a `response`
                      field (the standardized ResponseOutput coming
                      back from response_agent — patient/medication/
                      observation/appointment/summary lookups, and
                      completed or failed workflow steps) should be
                      rendered as a ResponseCard instead of a plain
                      text bubble, so every agent/workflow answer
                      looks the same to the doctor. Plain assistant
                      text (no `response` payload) still renders as
                      a normal bubble.
                    */}
                    <MessageList
                      messages={messages}
                      onSuggestedReply={handleSuggestedReply}
                    />

                    {/* Medication Review */}

                    {interrupt?.type === "MEDICATION_REVIEW" && (
                      <MedicationReview
                        interrupt={interrupt}
                        threadId={threadId}
                        onComplete={(response) => {
                          console.log("Discharge workflow resumed:", response);

                          clearInterrupt();
                        }}
                      />
                    )}

                    {/* Appointment Confirmation */}

                    {interrupt?.type === "appointment_confirmation" && (
                      <AppointmentConfirmation
                        data={interrupt}
                        onConfirm={handleAppointmentConfirmation}
                      />
                    )}

                    {/* Other interrupts */}

                    {interrupt &&
                      interrupt.type !== "MEDICATION_REVIEW" &&
                      interrupt.type !== "appointment_confirmation" && (
                        <InterruptRenderer
                          interrupt={interrupt}
                          onSelectBed={selectBed}
                          onSelectPatient={resolvePatient}
                        />
                      )}

                    {loading && <TypingIndicator />}
                  </>
                )}
              </Box>

              {/* Input */}

              <Box
                sx={{
                  borderTop: "1px solid #E0E0E0",
                  p: 2,
                  bgcolor: "#fff",
                }}
              >
                <ChatInput loading={loading} onSend={sendMessage} />
              </Box>
            </Paper>
          </Grid>

          {/* ================= RIGHT PANEL ================= */}

          <Grid size={{ xs: 12, lg: 4 }}>
            <Paper
              elevation={3}
              sx={{
                borderRadius: 3,
                p: 3,
                height: "78vh",
              }}
            >
              <Box
                sx={{
                  color: "text.secondary",
                  textAlign: "center",
                  mt: 5,
                }}
              >
                Patient Context
                <br />
                <br />
                (Coming Soon)
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
}
