import {
  Box,
  Card,
  CardActionArea,
  CardContent,
  Grid,
  Stack,
  Typography,
} from "@mui/material";

import LocalHospitalIcon from "@mui/icons-material/LocalHospital";
import HotelIcon from "@mui/icons-material/Hotel";
import SwapHorizIcon from "@mui/icons-material/SwapHoriz";
import MedicationIcon from "@mui/icons-material/Medication";
import ScienceIcon from "@mui/icons-material/Science";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";

const suggestions = [
  {
    title: "Admit Patient",
    prompt: "Admit Rahul Sharma with chest pain.",
    icon: <LocalHospitalIcon color="primary" />,
  },
  {
    title: "Recommend Bed",
    prompt: "Recommend an ICU bed for Rahul Sharma.",
    icon: <HotelIcon color="primary" />,
  },
  {
    title: "Transfer Patient",
    prompt: "Transfer Rahul Sharma to ICU.",
    icon: <SwapHorizIcon color="primary" />,
  },
  {
    title: "Order Medication",
    prompt: "Prescribe Paracetamol 500mg twice daily.",
    icon: <MedicationIcon color="primary" />,
  },
  {
    title: "Lab Investigation",
    prompt: "Order CBC and Blood Sugar test.",
    icon: <ScienceIcon color="primary" />,
  },
  {
    title: "Discharge Patient",
    prompt: "Discharge Rahul Sharma.",
    icon: <ExitToAppIcon color="primary" />,
  },
];

export default function EmptyChat({ onSuggestionClick }) {
  return (
    <Box
      sx={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        px: 3,
      }}
    >
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        👋 Welcome Doctor
      </Typography>

      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Ask me anything about admissions, transfers, medications, beds,
        observations, or discharge.
      </Typography>

      <Grid container spacing={2} maxWidth={900}>
        {suggestions.map((item) => (
          <Grid item xs={12} sm={6} md={4} key={item.title}>
            <Card
              sx={{
                borderRadius: 3,
                height: "100%",
                transition: "0.2s",
                "&:hover": {
                  transform: "translateY(-4px)",
                  boxShadow: 6,
                },
              }}
            >
              <CardActionArea onClick={() => onSuggestionClick(item.prompt)}>
                <CardContent>
                  <Stack spacing={2}>
                    {item.icon}

                    <Typography variant="subtitle1" fontWeight="bold">
                      {item.title}
                    </Typography>

                    <Typography variant="body2" color="text.secondary">
                      {item.prompt}
                    </Typography>
                  </Stack>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
