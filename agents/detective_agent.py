from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from typing import Dict, List

class EvidenceMetadata(Model):
    evidence: Dict[str, dict]

class InvestigationReport(Model):
    case_id: str
    hypotheses: List[Dict]

# Detective Agent setup
detective_agent = Agent(
    name="detective-agent",
    seed="detective-secure-seed-67890",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"]
)

fund_agent_if_low(detective_agent.wallet.address())

@detective_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"🕵️ Detective Agent READY")
    ctx.logger.info(f"📍 Address: {ctx.agent.address}")
    ctx.logger.info(f"🌐 Listening on: http://127.0.0.1:8001")

# Receive evidence and generate report
@detective_agent.on_message(model=EvidenceMetadata)
async def analyze(ctx: Context, sender: str, msg: EvidenceMetadata):
    ctx.logger.info(f"📥 Evidence received from {sender}")
    ctx.logger.info(f"📄 Data: {msg.evidence}")

    pois = set()
    evidence_used = []

    for eid, data in msg.evidence.items():
        if "shows_person" in data:
            pois.add(data["shows_person"])
            evidence_used.append(eid)
        if "claims" in data and "suspect" in data["claims"]:
            pois.add(data["claims"]["suspect"])
            evidence_used.append(eid)

    report = InvestigationReport(
        case_id=f"case-{len(evidence_used)}-{ctx.agent.address[:6]}",
        hypotheses=[{
            "summary": "Detective analysis complete",
            "persons_of_interest": list(pois),
            "evidence_used": evidence_used,
            "confidence": 0.9
        }]
    )

    ctx.logger.info(f"📊 Generated Report: {report}")
    # Optionally: send back to collector or client
    await ctx.send(sender, report)
    ctx.logger.info("✅ Report sent back to Evidence Collector")

if __name__ == "__main__":
    detective_agent.run()

