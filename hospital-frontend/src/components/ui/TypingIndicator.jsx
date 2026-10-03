import { Avatar, Box, Paper, Typography } from "@mui/material";

import SmartToyIcon from "@mui/icons-material/SmartToy";

export default function TypingIndicator() {
  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "flex-start",
        gap: 1.5,
        mb: 2,
      }}
    >
      {/* AI Avatar */}
      <Avatar
        sx={{
          bgcolor: "primary.main",
        }}
      >
        <SmartToyIcon />
      </Avatar>

      {/* Bubble */}
      <Paper
        elevation={2}
        sx={{
          px: 2,
          py: 1.5,
          borderRadius: 3,
          bgcolor: "#fff",
          minWidth: 180,
        }}
      >
        <Typography variant="body2" color="text.secondary" gutterBottom>
          AI Hospital Assistant is thinking...
        </Typography>

        <Box
          sx={{
            display: "flex",
            gap: 0.8,
            mt: 1,
          }}
        >
          <Box
            sx={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              bgcolor: "primary.main",
              animation: "typing 1s infinite ease-in-out",
            }}
          />

          <Box
            sx={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              bgcolor: "primary.main",
              animation: "typing 1s 0.2s infinite ease-in-out",
            }}
          />

          <Box
            sx={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              bgcolor: "primary.main",
              animation: "typing 1s 0.4s infinite ease-in-out",
            }}
          />
        </Box>

        <style>
          {`
            @keyframes typing {
              0% {
                transform: translateY(0);
                opacity: 0.3;
              }
              50% {
                transform: translateY(-6px);
                opacity: 1;
              }
              100% {
                transform: translateY(0);
                opacity: 0.3;
              }
            }
          `}
        </style>
      </Paper>
    </Box>
  );
}
