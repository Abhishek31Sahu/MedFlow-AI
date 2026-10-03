import { useState } from "react";

import { Box, IconButton, Paper, TextField, Tooltip } from "@mui/material";

import SendIcon from "@mui/icons-material/Send";
import AttachFileIcon from "@mui/icons-material/AttachFile";

export default function ChatInput({ onSend, loading = false }) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;

    onSend(input);

    setInput("");
  };

  const handleKeyDown = (event) => {
    // Enter = Send
    // Shift + Enter = New Line
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <Paper
      elevation={3}
      sx={{
        p: 2,
        borderRadius: 3,
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "flex-end",
          gap: 1,
        }}
      >
        {/* Attachment (Future Feature) */}

        <Tooltip title="Attach File">
          <IconButton disabled>
            <AttachFileIcon />
          </IconButton>
        </Tooltip>

        {/* Message Input */}

        <TextField
          fullWidth
          multiline
          maxRows={5}
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        {/* Send Button */}

        <Tooltip title="Send">
          <span>
            <IconButton
              color="primary"
              onClick={handleSend}
              disabled={loading || !input.trim()}
            >
              <SendIcon />
            </IconButton>
          </span>
        </Tooltip>
      </Box>
    </Paper>
  );
}
