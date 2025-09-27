import { useState, useEffect, useCallback } from "react";
import { ethers } from "ethers";
import EvidenceRegistryAbi from "../utils/EvidenceRegistryAbi.json"; // Assuming this is correct

// Use a prefix for React environment variables
const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS;

export const useContract = () => {
  const [contract, setContract] = useState<ethers.Contract | null>(null);
  const [provider, setProvider] = useState<ethers.providers.Web3Provider | null>(null);
  const [signer, setSigner] = useState<ethers.Signer | null>(null); // Expose signer
  const [account, setAccount] = useState<string | null>(null); // Expose account
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const connectWallet = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      if (!window.ethereum) {
        throw new Error("MetaMask or compatible wallet not detected.");
      }

      const prov = new ethers.providers.Web3Provider(window.ethereum);
      setProvider(prov);

      // Request accounts and get signer
      await prov.send("eth_requestAccounts", []);
      const _signer = prov.getSigner();
      const _account = await _signer.getAddress();
      setSigner(_signer);
      setAccount(_account);

      // Initialize contract with the signer
      if (!CONTRACT_ADDRESS) {
        throw new Error("CONTRACT_ADDRESS is not defined in environment variables.");
      }
      const cont = new ethers.Contract(CONTRACT_ADDRESS, EvidenceRegistryAbi, _signer);
      setContract(cont);

      // Set up event listeners for accounts and chain changes
      window.ethereum.on('accountsChanged', (accounts: string[]) => {
        if (accounts.length > 0) {
          setAccount(accounts[0]);
          prov.getSigner(accounts[0]).then((newSigner) => {
            setSigner(newSigner);
            // Update contract with new signer if necessary
            setContract(new ethers.Contract(CONTRACT_ADDRESS!, EvidenceRegistryAbi, newSigner));
          });
        } else {
          setAccount(null);
          setSigner(null);
          setContract(null);
        }
      });
      window.ethereum.on('chainChanged', () => window.location.reload()); // Reload for chain changes

    } catch (err: any) {
      console.error("Failed to connect wallet or initialize contract:", err);
      setError(err.message || "Failed to connect wallet.");
      setAccount(null);
      setSigner(null);
      setContract(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // Auto-connect if wallet is already connected and approved
    if (window.ethereum && window.ethereum.selectedAddress && !account) {
      connectWallet();
    } else if (!window.ethereum) {
      setLoading(false); // No wallet, so not loading
    }
  }, [account, connectWallet]); // Depend on account to avoid re-running if already connected

  // Expose POLICE_ROLE constant for convenience
  const POLICE_ROLE = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("POLICE_ROLE"));
  const DEFAULT_ADMIN_ROLE = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("0x0000000000000000000000000000000000000000000000000000000000000000"));

  return { contract, provider, signer, account, loading, error, connectWallet, POLICE_ROLE, DEFAULT_ADMIN_ROLE };
};