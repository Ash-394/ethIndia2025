import { useState, useEffect } from "react";
import { Box, Typography, Button, CircularProgress, Alert } from "@mui/material";
import { fetchFileFromCID } from "../utils/lighthouseFetch";

interface Props {
  cid: string;
  authorized: boolean; // true if police role or submitter
}

const CaseEvidenceViewer: React.FC<Props> = ({ cid, authorized }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    if (!authorized) {
      setError("You are not authorized to view this evidence.");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const fileData = await fetchFileFromCID(cid);
      setData(fileData);
    } catch (err: any) {
      setError(err.message || "Failed to fetch evidence.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [cid, authorized]);

  if (loading) return <CircularProgress size={24} />;
  if (error) return <Alert severity="error">{error}</Alert>;

  if (!data) return null;

  return (
    <Box sx={{ mt: 2, p: 2, border: "1px solid", borderColor: "grey.300", borderRadius: 2 }}>
      <Typography variant="subtitle2">Evidence Content:</Typography>
      {typeof data === "string" && <Typography sx={{ mt: 1 }}>{data}</Typography>}
      {typeof data === "object" && !(data instanceof Blob) && (
        <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(data, null, 2)}</pre>
      )}
      {data instanceof Blob && (
        <Button
          variant="contained"
          href={URL.createObjectURL(data)}
          target="_blank"
          sx={{ mt: 1 }}
        >
          Download File
        </Button>
      )}
    </Box>
  );
};

export default CaseEvidenceViewer;
