import { useState } from "react";
import { Button } from "@mui/material";

const WalletConnectButton = () => {
  const [connected, setConnected] = useState(false);

  return (
    <Button
      variant="contained"
      color="secondary"
      onClick={() => setConnected(!connected)}
      sx={{ textTransform: "none" }}
    >
      {connected ? "Connected" : "Connect Wallet"}
    </Button>
  );
};

export default WalletConnectButton;