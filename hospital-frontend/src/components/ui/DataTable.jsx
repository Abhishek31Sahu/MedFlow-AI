import React, { useMemo, useState } from "react";

import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  TablePagination,
  Checkbox,
  CircularProgress,
  Typography,
  Box,
} from "@mui/material";

export default function DataTable({
  columns = [],
  rows = [],
  loading = false,
  selectable = false,
  striped = true,
  stickyHeader = true,
  dense = false,
  rowKey = "id",
  onRowClick,
}) {
  const [order, setOrder] = useState("asc");

  const [orderBy, setOrderBy] = useState("");

  const [page, setPage] = useState(0);

  const [rowsPerPage, setRowsPerPage] = useState(10);

  const [selected, setSelected] = useState([]);

  const handleSort = (field) => {
    const isAsc = orderBy === field && order === "asc";

    setOrder(isAsc ? "desc" : "asc");

    setOrderBy(field);
  };

  const sortedRows = useMemo(() => {
    const copied = [...rows];

    if (!orderBy) return copied;

    copied.sort((a, b) => {
      if (a[orderBy] < b[orderBy]) return order === "asc" ? -1 : 1;

      if (a[orderBy] > b[orderBy]) return order === "asc" ? 1 : -1;

      return 0;
    });

    return copied;
  }, [rows, order, orderBy]);

  const visibleRows = sortedRows.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage,
  );

  const handleSelectAll = (event) => {
    if (event.target.checked) {
      setSelected(rows.map((r) => r[rowKey]));
    } else {
      setSelected([]);
    }
  };

  const handleSelectRow = (id) => {
    setSelected((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id],
    );
  };
  return (
    <Paper elevation={3} sx={{ borderRadius: 3, overflow: "hidden" }}>
      <TableContainer sx={{ maxHeight: 650 }}>
        <Table stickyHeader={stickyHeader} size={dense ? "small" : "medium"}>
          {/* ================= HEADER ================= */}

          <TableHead>
            <TableRow>
              {selectable && (
                <TableCell padding="checkbox">
                  <Checkbox
                    checked={rows.length > 0 && selected.length === rows.length}
                    indeterminate={
                      selected.length > 0 && selected.length < rows.length
                    }
                    onChange={handleSelectAll}
                  />
                </TableCell>
              )}

              {columns.map((column) => (
                <TableCell
                  key={column.field}
                  align={column.align || "left"}
                  sx={{
                    fontWeight: "bold",
                    backgroundColor: "#1976d2",
                    color: "#fff",
                    minWidth: column.minWidth || 120,
                  }}
                >
                  {column.sortable === false ? (
                    column.headerName
                  ) : (
                    <TableSortLabel
                      active={orderBy === column.field}
                      direction={orderBy === column.field ? order : "asc"}
                      onClick={() => handleSort(column.field)}
                      sx={{
                        color: "#fff",
                        "&.Mui-active": {
                          color: "#fff",
                        },
                        "& .MuiTableSortLabel-icon": {
                          color: "#fff !important",
                        },
                      }}
                    >
                      {column.headerName}
                    </TableSortLabel>
                  )}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>

          {/* ================= BODY ================= */}

          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length + (selectable ? 1 : 0)}
                  align="center"
                >
                  <Box py={5}>
                    <CircularProgress />
                  </Box>
                </TableCell>
              </TableRow>
            ) : visibleRows.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length + (selectable ? 1 : 0)}
                  align="center"
                >
                  <Typography py={4}>No Records Found</Typography>
                </TableCell>
              </TableRow>
            ) : (
              visibleRows.map((row, index) => {
                const isSelected = selected.includes(row[rowKey]);

                return (
                  <TableRow
                    key={row[rowKey]}
                    hover
                    selected={isSelected}
                    onClick={() => onRowClick && onRowClick(row)}
                    sx={{
                      cursor: onRowClick ? "pointer" : "default",

                      backgroundColor:
                        striped && index % 2 === 0 ? "#fafafa" : "#fff",

                      "&:hover": {
                        backgroundColor: "#E3F2FD",
                      },
                    }}
                  >
                    {selectable && (
                      <TableCell padding="checkbox">
                        <Checkbox
                          checked={isSelected}
                          onClick={(e) => e.stopPropagation()}
                          onChange={() => handleSelectRow(row[rowKey])}
                        />
                      </TableCell>
                    )}

                    {columns.map((column) => (
                      <TableCell
                        key={column.field}
                        align={column.align || "left"}
                      >
                        {column.render ? column.render(row) : row[column.field]}
                      </TableCell>
                    ))}
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}
