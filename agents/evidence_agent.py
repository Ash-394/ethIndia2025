from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from typing import Dict, List

# Model for evidence
class EvidenceMetadata(Model):
    evidence: Dict[str, dict]

# Knowledge Graph placeholder (Metta)
METTA_GRAPH = {}

# Agent setup
collector_agent = Agent(
    name="evidence-collector",
    seed="collector-secure-seed-12345",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"]
)

# Fund the wallet
fund_agent_if_low(collector_agent.wallet.address())

# Startup logging
@collector_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"🚀 Evidence Collector READY")
    ctx.logger.info(f"📍 Address: {ctx.agent.address}")
    ctx.logger.info(f"🌐 Listening on: http://127.0.0.1:8000")

# Receive new evidence
@collector_agent.on_message(model=EvidenceMetadata)
async def handle_evidence(ctx: Context, sender: str, msg: EvidenceMetadata):
    ctx.logger.info(f"🔥 New evidence received from {sender}")
    ctx.logger.info(f"📄 Data: {msg.evidence}")

    # Update Metta graph per case
    for eid, data in msg.evidence.items():
        METTA_GRAPH[eid] = data

    ctx.logger.info(f"🧠 METTA Graph updated: {METTA_GRAPH}")

    # Notify Detective Agent
    DETECTIVE_AGENT_ADDRESS = "PASTE_DETECTIVE_ADDRESS_HERE"
    await ctx.send(DETECTIVE_AGENT_ADDRESS, msg)
    ctx.logger.info(f"📤 Notified Detective Agent: {DETECTIVE_AGENT_ADDRESS}")

if __name__ == "__main__":
    collector_agent.run()

