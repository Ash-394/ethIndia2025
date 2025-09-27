import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { Link } from "react-router-dom";
import WalletConnectButton from "./WalletConnectButton";

const Navbar = () => {
  return (
    <AppBar position="static" color="primary" elevation={4}>
      <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
        <Typography variant="h6" component={Link} to="/" sx={{ textDecoration: "none", color: "inherit" }}>
          EvidenceRegistry
        </Typography>
        <Box sx={{ display: "flex", gap: 2 }}>
          <Button component={Link} to="/submit" color="inherit">
            Submit Evidence
          </Button>
          <Button component={Link} to="/police" color="inherit">
            Police Portal
          </Button>
          <Button component={Link} to="/ai" color="inherit">
            AI Investigator
          </Button>
          <WalletConnectButton />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;