import { useParams } from "react-router-dom";
import EvidenceTimeline from "../components/Evidences";

const CasePage = () => {
  const { id } = useParams();
  const evidences = [
    { id: "1", submitter: "Victim", timestamp: "2025-09-20", status: "Pending" },
    { id: "2", submitter: "Police", timestamp: "2025-09-21", status: "Approved" },
  ];

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold">Case ID: {id}</h1>
      <EvidenceTimeline evidences={evidences} />
    </div>
  );
};

export default CasePage;