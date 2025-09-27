import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { CssBaseline, ThemeProvider, createTheme, Box } from "@mui/material";
import Landing from "./pages/Landing";
import CasePage from "./pages/CasePage";
import PolicePortal from "./pages/PolicePortal";
import SubmitEvidence from "./pages/SubmitEvidence";
import InvestigatorAI from "./pages/InvestigatorAI";
import Navbar from "./components/Navbar";
import {WalletProvider} from "./context/WalletContext.tsx"

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
      <WalletProvider>
      <Router>
        <Box
          sx={{
            minHeight: "100vh",
            bgcolor: "background.default", 
            color: "text.primary",
            backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url(${backgroundPattern})`,
            backgroundSize: "cover", 
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat", 
            backgroundAttachment: "fixed", 
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
      </WalletProvider>
    </ThemeProvider>
  );
}

export default App;