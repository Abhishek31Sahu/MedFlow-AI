import { Button, Typography, Box } from "@mui/material";

import DataTable from "./DataTable";

export default function PatientSelectionList({ patients, onSelect }) {
  const columns = [
    {
      field: "name",
      headerName: "Patient Name",
    },
    {
      field: "gender",
      headerName: "Gender",
    },
    {
      field: "birth_date",
      headerName: "Birth Date",
    },
    {
      field: "action",
      headerName: "Action",
      sortable: false,

      render: (row) => (
        <Button
          variant="contained"
          size="small"
          onClick={() => onSelect(row.id)}
        >
          Select
        </Button>
      ),
    },
  ];

  return (
    <Box mt={2}>
      <Typography variant="subtitle1" fontWeight="bold" mb={2}>
        Multiple patients found. Select one.
      </Typography>

      <DataTable
        columns={columns}
        rows={patients}
        rowKey="id"
        loading={false}
        selectable={false}
      />
    </Box>
  );
}
