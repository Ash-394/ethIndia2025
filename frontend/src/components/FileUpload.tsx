import { useState } from "react";
import { Box, Button, Typography } from "@mui/material";
import { uploadFileEncrypted } from "../utils/lighthouseUpload";


const FileUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [cid, setCid] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file || !signer || !account) return;  // need wallet signer and account
    setUploading(true);
    try {
      const apiKey = process.env.REACT_APP_LIGHTHOUSE_API_KEY!;
      const uploadedCid = await uploadFileEncrypted(file, apiKey, signer, account, (progress) => {
        console.log(`Upload progress: ${progress}%`);
      });
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
          {uploading ? "Uploading..." : "Upload to Lighthouse"}
        </Button>
      </Box>
      {cid && (
        <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
          Uploaded CID: <a href={`https://gateway.lighthouse.storage/ipfs/${cid}`} target="_blank" rel="noreferrer">{cid}</a>
        </Typography>
      )}
    </Box>
  );
};

export default FileUpload;
