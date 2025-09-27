import { useState } from "react";
import { Box, Button, Typography } from "@mui/material";

const FileUpload = () => {
  const [file, setFile] = useState<File | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setFile(e.target.files[0]);
  };

  return (
    <Box
      sx={{
        border: "2px dashed",
        borderColor: "primary.main",
        borderRadius: 2,
        p: 4,
        textAlign: "center",
      }}
    >
      <Button
        variant="contained"
        component="label"
        sx={{ mb: 2 }}
      >
        Upload File
        <input
          type="file"
          hidden
          onChange={handleChange}
        />
      </Button>
      {file && (
        <Typography variant="body2" color="text.secondary">
          {file.name}
        </Typography>
      )}
    </Box>
  );
};

export default FileUpload;