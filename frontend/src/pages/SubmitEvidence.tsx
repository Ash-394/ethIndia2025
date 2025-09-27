import { useState } from "react";
import { Box, Button, Typography, TextField, Paper, CircularProgress, Alert, FormControl, InputLabel, Select, MenuItem, Divider } from "@mui/material";
import { uploadFile, uploadText } from "../utils/storage";
import { calculateSha256, calculateSha256OfText } from "../utils/crypto";
import { useContract } from "../hooks/useContract"; // Import YOUR hook

const SubmitEvidence = () => {
  // Use your useContract hook
  const { account, signer, contract, loading: web3Loading, error: web3Error, connectWallet } = useContract();

  const [caseId, setCaseId] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [textEvidence, setTextEvidence] = useState("");
  const [submitterType, setSubmitterType] = useState(0); // 0 for anonymous, 1 for authenticated
  const [encryptedKeyRef, setEncryptedKeyRef] = useState(""); // Placeholder for encryption reference

  const [uploading, setUploading] = useState(false);
  const [submittingContract, setSubmittingContract] = useState(false);
  const [statusMessage, setStatusMessage] = useState({ message: "", type: "" }); // 'info', 'success', 'error'

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setTextEvidence(""); // Clear text if file is selected
    } else {
      setFile(null);
    }
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTextEvidence(e.target.value);
    setFile(null); // Clear file if text is entered
  };

  const handleSubmitEvidence = async () => {
    if (!account || !signer || !contract) {
      setStatusMessage({ message: "Please connect your wallet.", type: "error" });
      return;
    }
    if (!caseId) {
      setStatusMessage({ message: "Please enter a Case ID.", type: "error" });
      return;
    }
    if (!file && !textEvidence) {
      setStatusMessage({ message: "Please select a file or enter text evidence.", type: "error" });
      return;
    }

    setUploading(true);
    setSubmittingContract(false);
    setStatusMessage({ message: "Uploading evidence to IPFS...", type: "info" });

    let cid: string | null = null;
    let sha256Hash: string = "";

    try {
      if (file) {
        cid = await uploadFile(file);
        sha256Hash = await calculateSha256(file);
      } else if (textEvidence) {
        cid = await uploadText(textEvidence); // Use new uploadText helper
        sha256Hash = await calculateSha256OfText(textEvidence);
      } else {
        throw new Error("No evidence selected.");
      }

      if (!cid) throw new Error("Failed to get CID after upload.");

      setUploading(false);
      setSubmittingContract(true);
      setStatusMessage({ message: "Evidence uploaded. Submitting to blockchain...", type: "info" });

      // Call smart contract function
      const tx = await contract.connect(signer).submitEvidenceToCase(
        parseInt(caseId),
        sha256Hash,
        cid, // cidPreview
        submitterType,
        encryptedKeyRef // This would be the reference to encrypted key, if any
      );

      setStatusMessage({ message: `Transaction sent: ${tx.hash}`, type: "info" });
      await tx.wait();

      setStatusMessage({ message: `Evidence submitted successfully! CID: ${cid}`, type: "success" });
      // Reset form
      setFile(null);
      setTextEvidence("");
      setCaseId("");
      setEncryptedKeyRef("");

    } catch (err: any) {
      console.error("Submission failed:", err);
      setStatusMessage({ message: `Submission failed: ${err.reason || err.message || String(err)}`, type: "error" });
    } finally {
      setUploading(false);
      setSubmittingContract(false);
    }
  };

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
        <Paper elevation={3} sx={{ p: 4, bgcolor: "background.paper", textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            Connect Wallet
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Please connect your wallet to submit evidence.
          </Typography>
          <Button onClick={connectWallet} variant="contained" color="primary">
            Connect Wallet
          </Button>
        </Paper>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 4 }}>
      <Paper elevation={3} sx={{ p: 4, bgcolor: "background.paper" }}>
        <Typography variant="h4" gutterBottom>
          Submit Evidence
        </Typography>

        {statusMessage.message && (
          <Alert severity={statusMessage.type} sx={{ mb: 3 }}>
            {statusMessage.message}
          </Alert>
        )}

        <TextField
          fullWidth
          label="Case ID"
          variant="outlined"
          type="number"
          value={caseId}
          onChange={(e) => setCaseId(e.target.value)}
          sx={{ mb: 3 }}
          required
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

        {/* File Upload Section */}
        <Box
          sx={{
            border: "2px dashed",
            borderColor: "primary.main",
            borderRadius: 2,
            p: 4,
            textAlign: "center",
            mb: 3,
            backgroundColor: file ? 'rgba(0, 229, 255, 0.1)' : 'transparent', // Highlight if file is chosen
          }}
        >
          <Button variant="contained" component="label" sx={{ mb: 2 }}>
            Select File
            <input type="file" hidden onChange={handleFileChange} />
          </Button>
          {file && <Typography>{file.name} ({file.size} bytes)</Typography>}
          {!file && !textEvidence && <Typography variant="body2" color="text.secondary">No file selected</Typography>}
        </Box>

        <Divider sx={{ my: 3 }}>OR</Divider>

        {/* Text Box Input */}
        <TextField
          fullWidth
          label="Enter Text Evidence"
          variant="outlined"
          multiline
          rows={6}
          value={textEvidence}
          onChange={handleTextChange}
          sx={{ mb: 3 }}
          placeholder="Type or paste your text evidence here. Selecting a file will clear this."
          disabled={!!file} // Disable if a file is selected
        />

        {/* Placeholder for Encrypted Key Reference */}
        <TextField
          fullWidth
          label="Encrypted Key Reference (Optional)"
          variant="outlined"
          value={encryptedKeyRef}
          onChange={(e) => setEncryptedKeyRef(e.target.value)}
          sx={{ mb: 3 }}
          helperText="If your evidence is encrypted, store a reference to the decryption key here."
        />

        <Button
          fullWidth
          variant="contained"
          color="primary"
          onClick={handleSubmitEvidence}
          disabled={!caseId || (!file && !textEvidence) || uploading || submittingContract || !contract || !signer}
          startIcon={(uploading || submittingContract) && <CircularProgress size={20} color="inherit" />}
        >
          {uploading ? "Uploading to IPFS..." : submittingContract ? "Submitting to Blockchain..." : "Submit Evidence"}
        </Button>
      </Paper>
    </Box>
  );
};

export default SubmitEvidence;