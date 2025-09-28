import { useState } from 'react';
import { AppBar, Toolbar, Typography, Button, Box, IconButton, Menu, MenuItem } from "@mui/material";
import MenuIcon from '@mui/icons-material/Menu';
import { Link } from "react-router-dom";
import WalletConnectButton from "./WalletConnectButton";

const Navbar = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const navLinks = [
    { title: 'Submit Evidence', path: '/submit' },
    { title: 'Police Portal', path: '/police' },
    { title: 'AI Investigator', path: '/ai' },
  ];

  return (
    <AppBar position="static" color="primary" elevation={4}>
      <Toolbar sx={{ justifyContent: { xs: 'space-between', md: 'flex-start' } }}>
        <Box sx={{ flexGrow: { xs: 1, md: 0 }, textAlign: { xs: 'center', md: 'left' } }}>
          <Typography
            variant="h6"
            component={Link}
            to="/"
            sx={{
              textDecoration: "none",
              color: "inherit",
              display: 'block', // Ensures the Box centering works
              px: { md: 2 } // Adds padding on desktop
            }}
          >
            EvidenceRegistry
          </Typography>
        </Box>

        {/* Desktop Links */}
        <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' }, justifyContent: 'flex-end', alignItems: 'center', gap: 2 }}>
          {navLinks.map((link) => (
            <Button
              key={link.title}
              component={Link}
              to={link.path}
              color="inherit"
              sx={{ '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.1)' } }}
            >
              {link.title}
            </Button>
          ))}
          <WalletConnectButton />
        </Box>

        {/* Mobile Menu */}
        <Box sx={{ display: { xs: 'flex', md: 'none' }, alignItems: 'center' }}>
          <WalletConnectButton />
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={handleMenu}
            sx={{ ml: 1 }}
          >
            <MenuIcon />
          </IconButton>
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={open}
            onClose={handleClose}
          >
            {navLinks.map((link) => (
              <MenuItem
                key={link.title}
                onClick={handleClose}
                component={Link}
                to={link.path}
              >
                {link.title}
              </MenuItem>
            ))}
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;