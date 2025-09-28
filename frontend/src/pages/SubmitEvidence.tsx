import { useState } from "react";
import { Box, Button, Typography, TextField, Paper, CircularProgress, Alert, FormControl, InputLabel, Select, MenuItem, Divider, Snackbar } from "@mui/material";
import { useContract } from "../hooks/useContract";
import { calculateSha256, calculateSha256OfText } from "../utils/crypto";
import { uploadFileEncrypted, uploadTextEncrypted } from "../utils/lighthouseUpload";

const SubmitEvidence = () => {
  const { account, signer, contract, loading: web3Loading, error: web3Error, connectWallet } = useContract();

  const [caseId, setCaseId] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [textEvidence, setTextEvidence] = useState("");
  const [submitterType, setSubmitterType] = useState(0);
  const [encryptedKeyRef, setEncryptedKeyRef] = useState("");

  const [uploading, setUploading] = useState(false);
  const [submittingContract, setSubmittingContract] = useState(false);
  const [statusMessage, setStatusMessage] = useState({ message: "", type: "" });
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setTextEvidence("");
    } else {
      setFile(null);
    }
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTextEvidence(e.target.value);
    setFile(null);
  };

  const handleSubmitEvidence = async () => {
    if (!account || !signer || !contract) return;

    const apiKey = import.meta.env.VITE_LIGHTHOUSE_API_KEY!;
    let cid: string = "";
    let sha256Hash: string = "";

    try {
      setUploading(true);

      if (file) {
        cid = await uploadFileEncrypted(file, apiKey, signer, account, (progress) => console.log(`Upload: ${progress}%`));
        sha256Hash = await calculateSha256(file);
      } else if (textEvidence) {
        cid = await uploadTextEncrypted(textEvidence, apiKey, signer, account, "evidence.txt");
        sha256Hash = await calculateSha256OfText(textEvidence);
      }

      setUploading(false);
      setSubmittingContract(true);

      const safeSha256Hash = sha256Hash || "";
      const safeCid = cid || "";
      const safeEncryptedKeyRef = encryptedKeyRef?.trim() || "";
      
      const tx = await contract.connect(signer).submitEvidenceToCase(
        parseInt(caseId),
        safeSha256Hash,
        safeCid,
        submitterType,
        safeEncryptedKeyRef
      );
      

      setSubmittingContract(false);
      setStatusMessage({ message: `Evidence submitted successfully! CID: ${cid}`, type: "success" });
      setSnackbarOpen(true); // Show toast notification
      setFile(null);
      setTextEvidence("");
      setEncryptedKeyRef("");
    } catch (err: any) {
      console.error(err);
      setUploading(false);
      setSubmittingContract(false);
      setStatusMessage({ message: `Submission failed: ${err.message || err}`, type: "error" });
      setSnackbarOpen(true); // Show toast even on error
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  // --- Render ---

  if (web3Loading) {
    return (
      <Box sx={{ p: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography sx={{ mt: 2 }}>Loading Web3 connection...</Typography>
      </Box>
    );
  }

  if (web3Error) {
    return (
      <Box sx={{ p: 4 }}>
        <Alert severity="error">
          <Typography variant="h6">Web3 Connection Error</Typography>
          <Typography>{web3Error}</Typography>
          <Button onClick={connectWallet} variant="contained" sx={{ mt: 2 }}>Reconnect Wallet</Button>
        </Alert>
      </Box>
    );
  }

  if (!account) {
    return (
      <Box sx={{ p: 4 }}>
        <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>Connect Wallet</Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Please connect your wallet to submit evidence.
          </Typography>
          <Button onClick={connectWallet} variant="contained" color="primary">Connect Wallet</Button>
        </Paper>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>Submit Evidence</Typography>

        <TextField
          fullWidth label="Case ID" variant="outlined" type="number"
          value={caseId} onChange={(e) => setCaseId(e.target.value)} sx={{ mb: 3 }} required
        />

        <FormControl fullWidth sx={{ mb: 3 }}>
          <InputLabel id="submitter-type-label">Submitter Type</InputLabel>
          <Select
            labelId="submitter-type-label"
            id="submitter-type-select"
            value={submitterType}
            label="Submitter Type"
            onChange={(e) => setSubmitterType(e.target.value as number)}
          >
            <MenuItem value={0}>Anonymous (address(0) on-chain)</MenuItem>
            <MenuItem value={1}>Authenticated (your connected address)</MenuItem>
          </Select>
        </FormControl>

        <Divider sx={{ my: 3 }}>Evidence Content</Divider>

        {/* File Upload */}
        <Box sx={{
          border: "2px dashed", borderColor: "primary.main", borderRadius: 2, p: 4,
          textAlign: "center", mb: 3, backgroundColor: file ? 'rgba(0, 229, 255, 0.1)' : 'transparent',
        }}>
          <Button variant="contained" component="label" sx={{ mb: 2 }}>
            Select File
            <input type="file" hidden onChange={handleFileChange} />
          </Button>
          {file && <Typography>{file.name} ({file.size} bytes)</Typography>}
          {!file && !textEvidence && <Typography variant="body2" color="text.secondary">No file selected</Typography>}
        </Box>

        <Divider sx={{ my: 3 }}>OR</Divider>

        {/* Text Input */}
        <TextField
          fullWidth label="Enter Text Evidence" variant="outlined" multiline rows={6}
          value={textEvidence} onChange={handleTextChange} sx={{ mb: 3 }}
          placeholder="Type or paste your text evidence here. Selecting a file will clear this."
          disabled={!!file}
        />

        <TextField
          fullWidth label="Encrypted Key Reference (Optional)" variant="outlined"
          value={encryptedKeyRef} onChange={(e) => setEncryptedKeyRef(e.target.value)}
          sx={{ mb: 3 }}
          helperText="If your evidence is encrypted, store a reference to the decryption key here."
        />

        {/* Submit Button */}
        <Button
          fullWidth variant="contained" color="primary"
          onClick={handleSubmitEvidence}
          disabled={!caseId || (!file && !textEvidence) || uploading || submittingContract || !contract || !signer}
          startIcon={(uploading || submittingContract) && <CircularProgress size={20} color="inherit" />}
        >
          {uploading ? "Uploading to Lighthouse..." : submittingContract ? "Submitting to Blockchain..." : "Submit Evidence"}
        </Button>

        {/* Snackbar for success/error */}
        <Snackbar
          open={snackbarOpen}
          autoHideDuration={5000}
          onClose={handleCloseSnackbar}
          message={statusMessage.message}
        />
      </Paper>
    </Box>
  );
};

export default SubmitEvidence;