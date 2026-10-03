import { Grid, Card, CardContent, Typography, Box } from "@mui/material";

import HotelIcon from "@mui/icons-material/Hotel";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import PersonIcon from "@mui/icons-material/Person";
import BookmarkIcon from "@mui/icons-material/Bookmark";
import CleaningServicesIcon from "@mui/icons-material/CleaningServices";
import LocalHospitalIcon from "@mui/icons-material/LocalHospital";
import AirIcon from "@mui/icons-material/Air";
import MonitorHeartIcon from "@mui/icons-material/MonitorHeart";

const cardData = [
  {
    title: "Total Beds",
    key: "total_beds",
    color: "#1976d2",
    icon: <HotelIcon fontSize="large" />,
  },
  {
    title: "Available",
    key: "available",
    color: "#2e7d32",
    icon: <CheckCircleIcon fontSize="large" />,
  },
  {
    title: "Occupied",
    key: "occupied",
    color: "#d32f2f",
    icon: <PersonIcon fontSize="large" />,
  },
  {
    title: "Reserved",
    key: "reserved",
    color: "#ed6c02",
    icon: <BookmarkIcon fontSize="large" />,
  },
  {
    title: "Cleaning",
    key: "cleaning",
    color: "#0288d1",
    icon: <CleaningServicesIcon fontSize="large" />,
  },
  {
    title: "ICU Beds",
    key: "icu",
    color: "#8e24aa",
    icon: <LocalHospitalIcon fontSize="large" />,
  },
  {
    title: "Oxygen Beds",
    key: "oxygen",
    color: "#00897b",
    icon: <AirIcon fontSize="large" />,
  },
  {
    title: "Ventilator",
    key: "ventilator",
    color: "#5d4037",
    icon: <MonitorHeartIcon fontSize="large" />,
  },
];

export default function BedStatsCards({ stats }) {
  return (
    <Grid container spacing={3} mb={3}>
      {cardData.map((card) => (
        <Grid item xs={12} sm={6} md={3} key={card.key}>
          <Card
            elevation={3}
            sx={{
              borderRadius: 3,
              borderLeft: `6px solid ${card.color}`,
              height: "100%",
            }}
          >
            <CardContent>
              <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
              >
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    {card.title}
                  </Typography>

                  <Typography variant="h4" fontWeight={700} mt={1}>
                    {stats?.[card.key] ?? 0}
                  </Typography>
                </Box>

                <Box sx={{ color: card.color }}>{card.icon}</Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}
