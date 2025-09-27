import { Box, Typography, Button, Paper } from "@mui/material";
import FileUpload from "../components/FileUpload";

const SubmitEvidence = () => {
  return (
    <Box sx={{ p: 4 }}>
      <Paper elevation={3} sx={{ p: 4, bgcolor: "background.paper" }}>
        <Typography variant="h4" gutterBottom>
          Submit Evidence
        </Typography>
        <FileUpload />
        <Button
          variant="contained"
          color="primary"
          sx={{ mt: 2 }}
        >
          Submit
        </Button>
      </Paper>
    </Box>
  );
};

export default SubmitEvidence;