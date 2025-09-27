import { Grid, Typography, Button, Box, Container, Card, CardContent } from "@mui/material";
import { styled, keyframes } from "@mui/system";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Science, Security, Gavel, VerifiedUser } from "@mui/icons-material";
import landingImg from "../assets/images/landing.png";

const fadeInSlideRight = keyframes`
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
`;

const darkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#00e5ff" },
    secondary: { main: "#ff6e40" },
    background: { default: "#0a0a0f", paper: "#1a1a2e" },
    text: { primary: "#e0e0e0", secondary: "#a0a0a0" },
  },
  typography: {
    fontFamily: ['"Orbitron"', "Arial", "sans-serif"].join(","),
    h2: { fontWeight: 700, fontSize: "3.5rem" },
    h5: { fontWeight: 600, fontSize: "1.5rem" },
  },
});

const NeonButton = (props: any) => <Button variant="outlined" {...props} />;

const FeatureCard = ({ title, description, icon: Icon, delay }: any) => (
  <Card
    sx={{
      bgcolor: "background.paper",
      border: `1px solid ${darkTheme.palette.primary.main}40`,
      boxShadow: `0 0 10px ${darkTheme.palette.primary.main}20`,
      backdropFilter: "blur(5px)",
      textAlign: "left",
      p: 2,
      mb: 2,
      display: "flex",
      alignItems: "center",
      gap: 2,
      animation: `${fadeInSlideRight} 0.6s ease-out ${delay}s forwards`,
      opacity: 0,
    }}
  >
    <Icon sx={{ fontSize: 32, color: "primary.main" }} />
    <Box>
      <Typography variant="body1" sx={{ color: "primary.main", fontWeight: "bold" }}>
        {title}
      </Typography>
      <Typography variant="caption" color="text.secondary">
        {description}
      </Typography>
    </Box>
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
      <Box sx={{ pt: 8, pb: 12, minHeight: "100vh", display: "flex", alignItems: "center" }}>
        <Container maxWidth="lg">
          <Grid container spacing={6} alignItems="center">
            {/* Left: Text + Buttons */}
            <Grid item xs={12} lg={4}>
              <Typography
                variant="h2"
                gutterBottom
                sx={{ color: "primary.main", textShadow: "0 0 15px #00e5ff90" }}
              >
                AI Detective Ledger
              </Typography>
              <Typography variant="h6" color="text.primary" sx={{ mb: 4 }}>
                Submit evidence anonymously, let AI uncover hidden links, and ensure tamper-proof
                justice on a decentralized ledger.
              </Typography>
              <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap" }}>
                <NeonButton>Submit Evidence</NeonButton>
                <NeonButton>Login as Police</NeonButton>
              </Box>
            </Grid>

            {/* Middle: Image */}
            <Grid item xs={12} lg={4}>
              <Box
                sx={{
                  width: "100%",
                  height: { xs: 250, md: 400, lg: 450 },
                  borderRadius: 3,
                  border: `2px solid ${darkTheme.palette.primary.main}80`,
                  boxShadow: `0 0 25px ${darkTheme.palette.primary.main}60`,
                  overflow: "hidden",
                }}
              >
                <img
                  src={landingImg}
                  alt="AI Connections"
                  style={{ width: "100%", height: "100%", objectFit: "cover" }}
                />
              </Box>
            </Grid>

            {/* Right: Features */}
            <Grid item xs={12} lg={4}>
              <Typography
                variant="h5"
                gutterBottom
                sx={{ color: "primary.main", mb: 3, textAlign: { xs: "center", lg: "left" } }}
              >
                Core Features
              </Typography>
              {features.map((f, idx) => (
                <FeatureCard {...f} key={idx} delay={0.2 * (idx + 1)} />
              ))}
            </Grid>
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  );
};

export default Landing;
