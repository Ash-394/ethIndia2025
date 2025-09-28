import { useState, useEffect, useCallback } from "react";
import { Box, Typography, Paper, Button, TextField, CircularProgress, Alert, Grid } from "@mui/material";
import { useContract } from "../hooks/useContract";
import { ethers } from "ethers";

import CaseTable from '../components/CaseTable';

const PolicePortal = () => {
  const { contract, provider } = useContract();

  const [account, setAccount] = useState(null);
  const [signer, setSigner] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [isPoliceOfficer, setIsPoliceOfficer] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [checkingRole, setCheckingRole] = useState(true);
  const [statusMessage, setStatusMessage] = useState({ message: "", type: "" });

  const [cases, setCases] = useState([]); // State to hold fetched cases
  const [caseIdToFetch, setCaseIdToFetch] = useState("");
  const [fetchedCase, setFetchedCase] = useState(null);

  // Form states for various functions
  const [newOfficerAddress, setNewOfficerAddress] = useState("");
  const [createCaseId, setCreateCaseId] = useState("");
  const [createCaseMetadataHash, setCreateCaseMetadataHash] = useState("");
  const [createCasePublicKey, setCreateCasePublicKey] = useState("");
  const [approveEvidenceCaseId, setApproveEvidenceCaseId] = useState("");
  const [approveEvidenceId, setApproveEvidenceId] = useState("");
  const [linkTipTipId, setLinkTipTipId] = useState("");
  const [linkTipCaseId, setLinkTipCaseId] = useState("");

  const connectWallet = async () => {
    setLoading(true);
    setError(null);
    try {
      if (provider) {
        await provider.send("eth_requestAccounts", []);
        const _signer = provider.getSigner();
        const _account = await _signer.getAddress();
        setAccount(_account);
        setSigner(_signer);
        window.ethereum.on('accountsChanged', (accounts) => {
          if (accounts.length > 0) {
            setAccount(accounts[0]);
            provider.getSigner(accounts[0]).then(setSigner);
          } else {
            setAccount(null);
            setSigner(null);
          }
        });
        window.ethereum.on('chainChanged', () => window.location.reload());
      } else {
        setError("MetaMask not detected. Please install it.");
      }
    } catch (err) {
      console.error("Failed to connect wallet:", err);
      setError("Failed to connect wallet. " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const checkRoles = useCallback(async () => {
    if (contract && account) {
      try {
        setCheckingRole(true);
        const policeRoleStatus = await contract.isPolice(account);
        setIsPoliceOfficer(policeRoleStatus);
        const adminRoleStatus = await contract.hasRole(DEFAULT_ADMIN_ROLE, account);
        setIsAdmin(adminRoleStatus);
      } catch (err) {
        console.error("Error checking roles:", err);
        // setStatusMessage({ message: `Error checking roles: ${err.message}`, type: "error" });
      } finally {
        setCheckingRole(false);
      }
    } else if (!account) {
      setIsPoliceOfficer(false);
      setIsAdmin(false);
      setCheckingRole(false);
    }
  }, [account, contract]);

  useEffect(() => {
    if (provider && window.ethereum) {
      if (window.ethereum.selectedAddress) {
        connectWallet();
      } else {
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  }, [provider]);

  useEffect(() => {
    checkRoles();
  }, [account, contract, checkRoles]);

  // Fetch all cases to display a list
  const fetchAllCases = useCallback(async () => {
    if (!contract) return;
    try {
      // Assuming a public function to get all case IDs or a way to iterate.
      // The current contract doesn't have a direct way, so this is a placeholder.
      // In a real scenario, you'd listen for `CaseCreated` events from a block or use a backend indexer.
      // For this example, we'll assume we can query a few by ID.
      // This part needs to be updated based on how your contract provides data.
      // We will mock fetching case 1 and 2 for demonstration.
      const case1 = await contract.cases(1);
      const case2 = await contract.cases(2);
      setCases([case1, case2].filter(c => c.caseId.toNumber() !== 0));
    } catch (err) {
      console.error("Error fetching cases:", err);
    }
  }, [contract]);

  useEffect(() => {
    if (contract && isPoliceOfficer) {
      fetchAllCases();
    }
  }, [contract, isPoliceOfficer, fetchAllCases]);

  const handleFetchCaseById = async () => {
    if (!contract || !caseIdToFetch) return;
    try {
      const caseData = await contract.cases(caseIdToFetch);
      if (caseData.caseId.toNumber() === 0) {
        setFetchedCase(null);
        setStatusMessage({ message: "Case not found.", type: "warning" });
      } else {
        setFetchedCase(caseData);
        setStatusMessage({ message: `Case ${caseIdToFetch} fetched successfully.`, type: "success" });
      }
    } catch (err) {
      console.error("Error fetching case:", err);
      setStatusMessage({ message: `Error fetching case: ${err.message}`, type: "error" });
    }
  };

  const sendTransaction = async (txFunction, successMsg) => {
    setStatusMessage({ message: "Sending transaction...", type: "info" });
    try {
      const tx = await txFunction();
      setStatusMessage({ message: `Transaction sent: ${tx.hash}`, type: "info" });
      await tx.wait();
      setStatusMessage({ message: successMsg, type: "success" });
      // Refresh data after a successful transaction
      await fetchAllCases();
    } catch (err) {
      console.error("Transaction failed:", err);
      setStatusMessage({ message: `Transaction failed: ${err.reason || err.message}`, type: "error" });
    }
  };

  const handleAddPoliceOfficer = () => {
    if (!signer || !contract || !newOfficerAddress) return;
    // Using grantRole as per AccessControl, not the custom addPoliceOfficer
    sendTransaction(
      () => contract.connect(signer).grantRole(ethers.utils.keccak256(ethers.utils.toUtf8Bytes("POLICE_ROLE")), newOfficerAddress),
      `Officer ${newOfficerAddress} added successfully!`
    );
  };
  
  const handleCreateCase = async () => {
    if (!signer || !contract || !createCaseId || !createCaseMetadataHash || !createCasePublicKey) return;
    try {
      const publicKeyBytes = ethers.utils.arrayify(createCasePublicKey);
      sendTransaction(
        () => contract.connect(signer).createCaseWithId(
          parseInt(createCaseId),
          createCaseMetadataHash,
          publicKeyBytes
        ),
        `Case ${createCaseId} created successfully!`
      );
    } catch (err) {
      console.error("Error preparing case creation:", err);
      setStatusMessage({ message: `Error creating case: ${err.reason || err.message}`, type: "error" });
    }
  };

  const handleApproveEvidence = () => {
    if (!signer || !contract || !approveEvidenceCaseId || !approveEvidenceId) return;
    sendTransaction(
      () => contract.connect(signer).approveEvidence(
        parseInt(approveEvidenceCaseId),
        parseInt(approveEvidenceId)
      ),
      `Evidence ${approveEvidenceId} for case ${approveEvidenceCaseId} approved!`
    );
  };

  const handleLinkTipToCase = () => {
    if (!signer || !contract || !linkTipTipId || !linkTipCaseId) return;
    sendTransaction(
      () => contract.connect(signer).linkTipToCase(
        parseInt(linkTipTipId),
        parseInt(linkTipCaseId)
      ),
      `Tip ${linkTipTipId} linked to case ${linkTipCaseId}!`
    );
  };

  if (loading || checkingRole) {
    return (
      <Box sx={{ p: 4, textAlign: 'center' }}>
        <CircularProgress />
        <Typography sx={{ mt: 2 }}>Loading Web3 connection and checking roles...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 4 }}>
        <Alert severity="error">
          <Typography variant="h6">Web3 Connection Error</Typography>
          <Typography>{error}</Typography>
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
            Please connect your wallet to access the Police Portal.
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
          Police Portal
        </Typography>

        {statusMessage.message && (
          <Alert severity={statusMessage.type} sx={{ mb: 3 }}>
            {statusMessage.message}
          </Alert>
        )}

        {!isPoliceOfficer && (
          <Alert severity="warning" sx={{ mb: 3 }}>
            <Typography variant="h6">Access Denied</Typography>
            <Typography>
              You do not have the `POLICE_ROLE` for this contract. Only authorized police officers can manage cases.
              {isAdmin && " As an admin, you can assign roles."}
            </Typography>
          </Alert>
        )}

        {isAdmin && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom color="primary">
              Admin: Add Police Officer
            </Typography>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={8}>
                <TextField
                  fullWidth
                  label="New Officer Address"
                  variant="outlined"
                  value={newOfficerAddress}
                  onChange={(e) => setNewOfficerAddress(e.target.value)}
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <Button
                  fullWidth
                  variant="contained"
                  color="secondary"
                  onClick={handleAddPoliceOfficer}
                  disabled={!newOfficerAddress || !signer}
                >
                  Add Officer
                </Button>
              </Grid>
            </Grid>
          </Box>
        )}

        {isPoliceOfficer ? (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom>
              Your Police Functions
            </Typography>

            {/* View Cases Section */}
            <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: "background.default" }}>
              <Typography variant="h6" gutterBottom color="primary">
                View Cases
              </Typography>
              <Button onClick={fetchAllCases} variant="contained">
                Refresh All Cases
              </Button>
              <CaseTable cases={cases} />
              <Grid container spacing={2} alignItems="center" sx={{ mt: 2 }}>
                <Grid item xs={12} sm={8}>
                  <TextField
                    fullWidth
                    label="Enter Case ID to Fetch"
                    variant="outlined"
                    type="number"
                    value={caseIdToFetch}
                    onChange={(e) => setCaseIdToFetch(e.target.value)}
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Button
                    fullWidth
                    variant="contained"
                    onClick={handleFetchCaseById}
                  >
                    Fetch Case
                  </Button>
                </Grid>
              </Grid>
              {fetchedCase && (
  <Box sx={{ mt: 2 }}>
    <Typography variant="subtitle1">Fetched Case Details:</Typography>
    <Typography>ID: {fetchedCase.caseId.toString()}</Typography>
    <Typography>Metadata Hash: {fetchedCase.metadataHash}</Typography>
    <Typography>Creator: {fetchedCase.creator}</Typography>
    <Typography>Created At: {new Date(fetchedCase.createdAt.toNumber() * 1000).toLocaleString()}</Typography>
    <Typography>Is Open: {fetchedCase.isOpen ? "Yes" : "No"}</Typography>

    {/* Show evidence file from CID only if authorized */}
    <CaseEvidenceViewer
      cid={fetchedCase.metadataHash}
      authorized={isPoliceOfficer || account?.toLowerCase() === fetchedCase.creator.toLowerCase()}
    />
  </Box>
)}

            </Paper>

            {/* Create Case */}
            <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: "background.default" }}>
              <Typography variant="h6" gutterBottom color="primary">Create New Case</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Case ID (e.g., 101)"
                    variant="outlined"
                    type="number"
                    value={createCaseId}
                    onChange={(e) => setCreateCaseId(e.target.value)}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Metadata Hash (IPFS CID)"
                    variant="outlined"
                    value={createCaseMetadataHash}
                    onChange={(e) => setCreateCaseMetadataHash(e.target.value)}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Case Public Key (Hex String, e.g., 0x...)"
                    variant="outlined"
                    value={createCasePublicKey}
                    onChange={(e) => setCreateCasePublicKey(e.target.value)}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick={handleCreateCase}
                    disabled={!createCaseId || !createCaseMetadataHash || !createCasePublicKey || !signer}
                  >
                    Create Case
                  </Button>
                </Grid>
              </Grid>
            </Paper>

            {/* Approve Evidence */}
            <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: "background.default" }}>
              <Typography variant="h6" gutterBottom color="primary">Approve Evidence</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Case ID"
                    variant="outlined"
                    type="number"
                    value={approveEvidenceCaseId}
                    onChange={(e) => setApproveEvidenceCaseId(e.target.value)}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Evidence ID"
                    variant="outlined"
                    type="number"
                    value={approveEvidenceId}
                    onChange={(e) => setApproveEvidenceId(e.target.value)}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick={handleApproveEvidence}
                    disabled={!approveEvidenceCaseId || !approveEvidenceId || !signer}
                  >
                    Approve Evidence
                  </Button>
                </Grid>
              </Grid>
            </Paper>

            {/* Link Tip to Case */}
            <Paper elevation={2} sx={{ p: 3, bgcolor: "background.default" }}>
              <Typography variant="h6" gutterBottom color="primary">Link Tip to Case</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Tip ID"
                    variant="outlined"
                    type="number"
                    value={linkTipTipId}
                    onChange={(e) => setLinkTipTipId(e.target.value)}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Case ID"
                    variant="outlined"
                    type="number"
                    value={linkTipCaseId}
                    onChange={(e) => setLinkTipCaseId(e.target.value)}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    onClick={handleLinkTipToCase}
                    disabled={!linkTipTipId || !linkTipCaseId || !signer}
                  >
                    Link Tip
                  </Button>
                </Grid>
              </Grid>
            </Paper>
          </Box>
        ) : (
          !isAdmin && (
            <Typography variant="body2" color="text.secondary" sx={{ mt: 3 }}>
              Connect with an authorized police officer account to view case management functions.
            </Typography>
          )
        )}
      </Paper>
    </Box>
  );
};

export default PolicePortal;