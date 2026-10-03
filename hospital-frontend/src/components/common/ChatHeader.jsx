import { Box, Button, Chip, Grid, Stack, Typography } from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import SmartToyIcon from "@mui/icons-material/SmartToy";

export default function ChatHeader({ onNewChat }) {
  return (
    <Box
      sx={{
        bgcolor: "#fff",
        borderRadius: 3,
        p: 2.5,
        mb: 2,
        boxShadow: 2,
      }}
    >
      <Grid container alignItems="flex-start" justifyContent="space-between">
        {/* Left Side */}

        <Grid size="grow">
          <Stack direction="row" spacing={1} alignItems="center">
            <SmartToyIcon color="primary" fontSize="large" />

            <Typography variant="h5" fontWeight="bold">
              AI Hospital Assistant
            </Typography>

            <Chip label="Online" color="success" size="small" />
          </Stack>

          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
            Ask about admissions, transfers, medications, discharge, bed
            recommendations and more.
          </Typography>
        </Grid>

        {/* Right Side */}

        <Grid size="auto">
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={onNewChat}
          >
            New Chat
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
}
