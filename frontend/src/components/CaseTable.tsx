import React from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

const CaseTable = ({ cases }) => {
  if (!cases || cases.length === 0) {
    return <Typography sx={{ mt: 2 }}>No cases found.</Typography>;
  }

  return (
    <TableContainer component={Paper} elevation={2} sx={{ mt: 3, bgcolor: "background.paper" }}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold' }}>Case ID</TableCell>
            <TableCell sx={{ fontWeight: 'bold' }}>Metadata Hash</TableCell>
            <TableCell sx={{ fontWeight: 'bold' }}>Creator</TableCell>
            <TableCell sx={{ fontWeight: 'bold' }}>Created At</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {cases.map((c, index) => (
            <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">
                {c.caseId.toString()}
              </TableCell>
              <TableCell>{c.metadataHash}</TableCell>
              <TableCell>{c.creator}</TableCell>
              <TableCell>{new Date(c.createdAt.toNumber() * 1000).toLocaleString()}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default CaseTable;