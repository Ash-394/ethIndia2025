import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { CssBaseline, ThemeProvider, createTheme, Box } from "@mui/material";
import Landing from "./pages/Landing";
import CasePage from "./pages/CasePage";
import PolicePortal from "./pages/PolicePortal";
import SubmitEvidence from "./pages/SubmitEvidence";
import InvestigatorAI from "./pages/InvestigatorAI";
import Navbar from "./components/Navbar";

// 1. Import the background image
// Adjust the path as needed, assuming App.tsx is in `src` and image is in `src/assets/images`
import backgroundPattern from './assets/images/landing.png'; 

const theme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#00bcd4", // Futuristic cyan
    },
    background: {
      default: "#121212", // Dark background (this will be beneath the image)
      paper: "#1e1e1e", // Slightly lighter for cards
    },
    text: {
      primary: "#ffffff",
      secondary: "#b0bec5",
    },
  },
  typography: {
    fontFamily: "'Roboto', 'Arial', sans-serif",
    h1: { fontWeight: 700 },
    h2: { fontWeight: 600 },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        {/* 2. Apply background styles to the main Box */}
        <Box
          sx={{
            minHeight: "100vh",
            // Fallback background color if image fails to load or for browsers that don't support image
            bgcolor: "background.default", 
            color: "text.primary",
            backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url(${backgroundPattern})`, // Add a dark overlay with linear-gradient
            backgroundSize: "cover", // Cover the entire Box
            backgroundPosition: "center", // Center the image
            backgroundRepeat: "no-repeat", // Don't repeat the image
            backgroundAttachment: "fixed", // Keeps the background fixed when scrolling
          }}
        >
          <Navbar />
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/case/:id" element={<CasePage />} />
            <Route path="/police" element={<PolicePortal />} />
            <Route path="/submit" element={<SubmitEvidence />} />
            <Route path="/ai" element={<InvestigatorAI />} />
          </Routes>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;