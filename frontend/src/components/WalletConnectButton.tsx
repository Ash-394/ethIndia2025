import { Button } from "@mui/material";
import { useWallet } from "../context/WalletContext";
import WalletIcon from '@mui/icons-material/AccountBalanceWallet';
import DisconnectIcon from '@mui/icons-material/Logout';

const WalletConnectButton = () => {
  const { account, isConnected, connectWallet, disconnectWallet } = useWallet();

  const handleButtonClick = () => {
    if (isConnected) {
      disconnectWallet();
    } else {
      connectWallet();
    }
  };

  return (
    <Button
      variant="contained"
      color={isConnected ? "success" : "secondary"}
      onClick={handleButtonClick}
      sx={{ textTransform: "none" }}
      startIcon={isConnected ? <DisconnectIcon /> : <WalletIcon />}
    >
      {isConnected ? `Disconnect` : "Connect Wallet"}
    </Button>
  );
};

export default WalletConnectButton;