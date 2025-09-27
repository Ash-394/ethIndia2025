# models.py - Create this file first
from typing import Dict, List
from uagents import Model

class EvidenceMetadata(Model):
    evidence: Dict[str, dict]

class InvestigationReport(Model):
    case_id: str
    hypotheses: List[Dict]

# ----------------------------

# FIXED detective_agent.py
import os
from dotenv import load_dotenv
from typing import Dict, List
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from models import EvidenceMetadata, InvestigationReport

load_dotenv()

# Keys
ASI_KEY = os.getenv("ASI_API_KEY")
AGENTVERSE_KEY = os.getenv("AGENTVERSE_API_KEY")

# Local Metta copy
METTA_GRAPH = {"cases": {}}

# Harry agent
harry = Agent(
    name="Harry",
    seed="harry-secure-seed-67890",
    port=8001,
    mailbox=True,
)

fund_agent_if_low(harry.wallet.address())

@harry.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("🕵️ Harry (Detective) READY")
    ctx.logger.info(f"📍 Address: {ctx.agent.address}")
    ctx.logger.info(f"🔑 Using ASI key: {bool(ASI_KEY)}, Agentverse key: {bool(AGENTVERSE_KEY)}")

@harry.on_message(model=EvidenceMetadata)
async def analyze(ctx: Context, sender: str, msg: EvidenceMetadata):
    ctx.logger.info(f"🔥 Evidence received from {sender}")
    ctx.logger.info(f"📄 Evidence data: {msg.evidence}")

    case_id = "case_001"
    if case_id not in METTA_GRAPH["cases"]:
        METTA_GRAPH["cases"][case_id] = {"nodes": [], "edges": []}

    METTA_GRAPH["cases"][case_id]["nodes"].append(msg.evidence)

    # Extract persons of interest
    persons_of_interest = []
    for evidence_item in msg.evidence.values():
        if "shows_person" in evidence_item or evidence_item.get("claims", {}).get("suspect"):  
            persons_of_interest.append(evidence_item)

    report = InvestigationReport(
        case_id=case_id,
        hypotheses=[{
            "summary": "Evidence analysis complete",
            "persons_of_interest": persons_of_interest,
            "evidence_used": list(msg.evidence.keys()),
            "confidence": 0.9
        }]
    )
    
    ctx.logger.info(f"📊 Report ready: {report}")
    await ctx.send(sender, report)
    ctx.logger.info("✅ Report sent!")

# REMOVED the problematic catch_all handler with model=object

if __name__ == "__main__":
    harry.run()
