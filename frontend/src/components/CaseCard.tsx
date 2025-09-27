import { Card, CardContent, Typography } from "@mui/material";

interface Props {
  id: string;
  type: string;
  location: string;
  evidences: number;
}

const CaseCard = ({ id, type, location, evidences }: Props) => {
  return (
    <Card sx={{ bgcolor: "background.paper", boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h6">{type}</Typography>
        <Typography variant="body2" color="text.secondary">
          Location: {location}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Evidence Count: {evidences}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default CaseCard;