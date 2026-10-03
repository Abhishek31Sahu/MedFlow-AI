import { Button, Typography, Box } from "@mui/material";

import DataTable from "./DataTable";

export default function BedRecommendationList({
  message,
  recommendations,
  onSelect,
}) {
  const columns = [
    {
      field: "bed_number",
      headerName: "Bed Number",
    },
    {
      field: "ward",
      headerName: "Ward",
    },
    {
      field: "room_number",
      headerName: "Room",
    },
    {
      field: "department",
      headerName: "Department",
    },
    {
      field: "score",
      headerName: "Score",
    },
    {
      field: "reasons",
      headerName: "Reasons",

      render: (row) => row.reasons.join(", "),
    },
    {
      field: "action",
      headerName: "Action",
      sortable: false,

      render: (row) => (
        <Button
          variant="contained"
          size="small"
          onClick={() =>
            onSelect({
              action: "select",

              bed_id: row.bed_id,

              selected_bed: row,
            })
          }
        >
          Select
        </Button>
      ),
    },
  ];

  return (
    <Box mt={2}>
      <Typography variant="subtitle1" fontWeight="bold" mb={2}>
        {message}
      </Typography>

      <DataTable
        columns={columns}
        rows={recommendations}
        loading={false}
        rowKey="bed_id"
        selectable={false}
        striped
        stickyHeader
      />
    </Box>
  );
}
