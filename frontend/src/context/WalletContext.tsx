import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { ethers } from 'ethers';

const WalletContext = createContext();

export const useWallet = () => useContext(WalletContext);

export const WalletProvider = ({ children }) => {
  const [account, setAccount] = useState(null);
  const [provider, setProvider] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  // Function to connect the wallet
  const connectWallet = useCallback(async () => {
    try {
      if (!window.ethereum) {
        alert("Please install MetaMask!");
        return;
      }
      const newProvider = new ethers.providers.Web3Provider(window.ethereum);
      const accounts = await newProvider.send("eth_requestAccounts", []);
      const newAccount = accounts[0];
      setAccount(newAccount);
      setProvider(newProvider);
      setIsConnected(true);
      // Optional: Store connection status in localStorage to maintain state on refresh
      localStorage.setItem('isWalletConnected', 'true');
    } catch (err) {
      console.error(err);
    }
  }, []);

  // Function to disconnect the wallet
  const disconnectWallet = useCallback(() => {
    setAccount(null);
    setProvider(null);
    setIsConnected(false);
    // Remove the connection status from localStorage
    localStorage.removeItem('isWalletConnected');
  }, []);

  // Watch for account changes in MetaMask
  useEffect(() => {
    if (window.ethereum) {
      const handleAccountsChanged = (accounts) => {
        if (accounts.length === 0) {
          disconnectWallet();
        } else {
          setAccount(accounts[0]);
          setIsConnected(true);
        }
      };
      window.ethereum.on('accountsChanged', handleAccountsChanged);
      
      // Initial check on page load
      const checkConnection = async () => {
        const storedConnection = localStorage.getItem('isWalletConnected');
        if (storedConnection === 'true' && window.ethereum) {
          const accounts = await window.ethereum.request({ method: 'eth_accounts' });
          if (accounts.length > 0) {
            connectWallet();
          } else {
            disconnectWallet();
          }
        }
      };
      checkConnection();

      return () => {
        if (window.ethereum) {
          window.ethereum.off('accountsChanged', handleAccountsChanged);
        }
      };
    }
  }, [connectWallet, disconnectWallet]);

  return (
    <WalletContext.Provider value={{ account, isConnected, provider, connectWallet, disconnectWallet }}>
      {children}
    </WalletContext.Provider>
  );
};