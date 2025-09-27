import { Grid, Typography, Button, Box, Container, Card, CardContent, IconButton } from "@mui/material";
import { styled } from "@mui/system";
import { createTheme, ThemeProvider } from "@mui/material/styles"; // IMPORTANT: createTheme and ThemeProvider from @mui/material/styles
import { Science, Security, Gavel, VerifiedUser } from '@mui/icons-material'; // Icons for features
import landingImg from "../assets/images/landing.png"
// 1. Create a custom theme for a futuristic, dark aesthetic
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00e5ff', // Brighter cyan for neon effect
    },
    secondary: {
      main: '#ff6e40', // A contrasting accent color
    },
    background: {
      default: '#0a0a0f', // Very dark background
      paper: '#1a1a2e', // Slightly lighter for cards/sections
    },
    text: {
      primary: '#e0e0e0', // Light grey for general text
      secondary: '#a0a0a0', // Muted grey for descriptions
    },
  },
  typography: {
    fontFamily: ['"Orbitron"', 'Arial', 'sans-serif'].join(','), // Futuristic font
    h2: {
      fontWeight: 700,
      fontSize: '3.5rem',
      '@media (max-width:600px)': {
        fontSize: '2.5rem',
      },
    },
    h4: {
      fontWeight: 600,
      fontSize: '2.5rem',
      '@media (max-width:600px)': {
        fontSize: '2rem',
      },
    },
    h6: {
      fontWeight: 500,
      fontSize: '1.2rem',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12, // Slightly rounded corners
          transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
          '&:hover': {
            transform: 'translateY(-5px)',
            boxShadow: `0 8px 30px #00e5ff40`, // Use literal color or reference after theme is ready
          },
        },
      },
    },
    // Adding button styles to the theme for consistency
    MuiButton: {
      styleOverrides: {
        root: {
          fontWeight: 600,
          padding: "0.8rem 2rem",
          borderRadius: 8,
          position: 'relative',
          overflow: 'hidden',
          zIndex: 1,
          transition: "0.4s ease-in-out",
          // The background gradient and hover effects
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: '-100%',
            width: '100%',
            height: '100%',
            background: `linear-gradient(90deg, transparent, #00e5ff50, transparent)`, // Use literal color here too
            transition: '0.4s ease-in-out',
            zIndex: -1,
          },
          "&:hover": {
            backgroundColor: '#00e5ff', // Use literal color here
            color: '#0a0a0f', // Use literal color here
            boxShadow: `0 0 20px #00e5ff`, // Use literal color here
            '&::before': {
              left: '100%',
            },
          },
        },
        outlined: { // Specific styles for outlined variant
            border: `2px solid #00e5ff`, // Use literal color here
            color: '#00e5ff', // Use literal color here
            '&:hover': {
                border: `2px solid #00e5ff`, // Keep border on hover
            }
        }
      }
    }
  },
});

// Keyframe animation for subtle glow effect
const neonGlowKeyframes = `
  @keyframes neonGlow {
    0% { text-shadow: 0 0 5px ${darkTheme.palette.primary.main}; }
    50% { text-shadow: 0 0 15px ${darkTheme.palette.primary.main}, 0 0 20px ${darkTheme.palette.primary.main}; }
    100% { text-shadow: 0 0 5px ${darkTheme.palette.primary.main}; }
  }
`;

// NOW define styled components AFTER darkTheme is initialized

// NeonButton can be a simple alias now, as its styles are in the theme components
const NeonButton = (props: any) => <Button variant="outlined" {...props} />;


// Feature Card Component
const FeatureCard = ({ title, description, icon: Icon }: { title: string; description: string; icon: React.ElementType }) => (
  <Card sx={{
    bgcolor: "background.paper",
    // Use literal color for border here or refactor to avoid direct darkTheme reference
    border: `1px solid ${darkTheme.palette.primary.main}40`,
    boxShadow: `0 0 10px ${darkTheme.palette.primary.main}20`,
    backdropFilter: "blur(5px)",
    textAlign: 'center',
    p: 2,
  }}>
    <CardContent>
      <Icon sx={{ fontSize: 60, color: "primary.main", mb: 2 }} />
      <Typography variant="h6" sx={{ mb: 1, color: "primary.main" }}>
        {title}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        {description}
      </Typography>
    </CardContent>
  </Card>
);

const Landing = () => {
  const features = [
    {
      title: "Anonymous Evidence Submission",
      description: "Drag & drop files, AI hashes and stores them securely on-chain.",
      icon: Science,
    },
    {
      title: "AI-Powered Investigation",
      description: "Detect connections and suspects with smart AI agents.",
      icon: Security,
    },
    {
      title: "Tamper-Proof Ledger",
      description: "Immutable blockchain storage for all evidence.",
      icon: Gavel,
    },
    {
      title: "Authority Verification",
      description: "ENS & Worldcoin verified police and investigator portals.",
      icon: VerifiedUser,
    },
  ];

  return (
    <ThemeProvider theme={darkTheme}>
      {/* Inject global styles for keyframes */}
      <style>{neonGlowKeyframes}</style>
      <Box sx={{ pt: 8, pb: 12, background: "linear-gradient(160deg, #0a0a0f, #1a1a2e)", minHeight: '100vh' }}>
        <Container maxWidth="lg">
          {/* Hero Section */}
          <Grid container spacing={6} alignItems="center">
            {/* Grid v2: removed 'item' prop, use sx for responsive width */}
            <Grid sx={{ xs: 12, md: 6 }}>
              <Typography variant="h2" gutterBottom sx={{ color: "primary.main", animation: 'neonGlow 1.5s infinite alternate ease-in-out' }}>
                AI Detective Ledger
              </Typography>
              <Typography variant="h6" gutterBottom color="text.primary" sx={{ mb: 4 }}>
                Submit evidence anonymously, let AI uncover hidden links, and ensure tamper-proof justice on a decentralized ledger.
              </Typography>
              <Box sx={{ mt: 4, display: 'flex', gap: 2 }}>
                <NeonButton>
                  Submit Evidence
                </NeonButton>
                <NeonButton>
                  Login as Police
                </NeonButton>
              </Box>
            </Grid>

            {/* Grid v2: removed 'item' prop, use sx for responsive width */}
            <Grid sx={{ xs: 12, md: 6 }}>
              {/* Hero Graphic / AI Mind Map Placeholder - This will be replaced by the image */}
              <Box
                sx={{
                  width: "100%",
                  height: { xs: 250, md: 400 },
                  bgcolor: "transparent", // Let the image handle the background
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  borderRadius: 3,
                  border: `2px solid ${darkTheme.palette.primary.main}80`,
                  boxShadow: `0 0 25px ${darkTheme.palette.primary.main}60`,
                  overflow: 'hidden', // Ensure image stays within bounds
                }}
              >
                {/* The generated image will go here */}
                <img
                src={landingImg}
                  alt="AI Mind Map illustrating connections and data flow"
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              </Box>
            </Grid>
          </Grid>

          {/* Features Section */}
          <Box sx={{ mt: 16 }}>
            <Typography variant="h4" gutterBottom sx={{ mb: 6, color: "primary.main", textAlign: 'center' }}>
              Core Features
            </Typography>
            <Grid container spacing={4}>
              {features.map((f, idx) => (
                // Grid v2: removed 'item' prop, use sx for responsive width
                <Grid sx={{ xs: 12, sm: 6, md: 3 }} key={idx}>
                  <FeatureCard {...f} />
                </Grid>
              ))}
            </Grid>
          </Box>
        </Container>
      </Box>
    </ThemeProvider>
  );
};

export default Landing;