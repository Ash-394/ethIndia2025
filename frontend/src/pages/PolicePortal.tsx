import { Box, Typography, Paper } from "@mui/material";

const PolicePortal = () => {
  return (
    <Box sx={{ p: 4 }}>
      <Paper elevation={3} sx={{ p: 4, bgcolor: "background.paper" }}>
        <Typography variant="h4" gutterBottom>
          Police Portal
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Register and manage cases here.
        </Typography>
      </Paper>
    </Box>
  );
};

export default PolicePortal;