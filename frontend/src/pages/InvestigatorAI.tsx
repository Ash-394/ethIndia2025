import { Box, Typography, Paper } from "@mui/material";

const InvestigatorAI = () => {
  return (
    <Box sx={{ p: 4 }}>
      <Paper elevation={3} sx={{ p: 4, bgcolor: "background.paper" }}>
        <Typography variant="h4" gutterBottom>
          AI Investigator
        </Typography>
        <Typography variant="body1" color="text.secondary">
          This page will show AI analysis and evidence linking.
        </Typography>
      </Paper>
    </Box>
  );
};

export default InvestigatorAI;