import { useState } from "react";
import { Box, Button, Typography } from "@mui/material";
import { uploadFile } from "../utils/storage"; // import helper

const FileUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [cid, setCid] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    try {
      const uploadedCid = await uploadFile(file);
      setCid(uploadedCid);
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
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
      <Button variant="contained" component="label" sx={{ mb: 2 }}>
        Select File
        <input type="file" hidden onChange={handleChange} />
      </Button>
      {file && <Typography>{file.name}</Typography>}
      <Box sx={{ mt: 2 }}>
        <Button
          variant="contained"
          disabled={!file || uploading}
          onClick={handleUpload}
        >
          {uploading ? "Uploading..." : "Upload to IPFS"}
        </Button>
      </Box>
      {cid && (
        <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
          Uploaded CID: {cid}
        </Typography>
      )}
      <div> or text box (for mvp easier to parse for ai agent)

      </div>
    </Box>
  );
};

export default FileUpload;
