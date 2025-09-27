# Updated test.py
import asyncio
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from models import EvidenceMetadata, InvestigationReport

# Use Kim's real address from your logs
KIM_ADDRESS = "agent1qdznt02at3xqpc9g6hlytt3ustd6edwh0ujtvrhtkshjv7eyckdskwpy6rh"

# Create a temporary agent WITH mailbox
tester = Agent(
    name="Tester",
    seed="hackathon-tester-2025",
    port=8002,
    mailbox=True
)

fund_agent_if_low(tester.wallet.address())

@tester.on_event("startup")
async def send_evidence(ctx: Context):
    ctx.logger.info("🚀 Tester starting up...")
    # Wait a bit to ensure connection
    await asyncio.sleep(3)
    
    # Create proper EvidenceMetadata message
    msg = EvidenceMetadata(evidence={
        "evidence_001": {
            "shows_person": "John Doe",
            "location": "123 Main St",
            "claims": {"suspect": True}
        },
        "evidence_002": {
            "shows_person": "Jane Smith",
            "location": "456 Oak Ave", 
            "claims": {"witness": True}
        }
    })
    
    ctx.logger.info("📤 Sending evidence to Kim...")
    try:
        await ctx.send(KIM_ADDRESS, msg)
        ctx.logger.info("✅ Message sent successfully!")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to send message: {e}")
    
    # Keep running for a bit to receive potential responses
    ctx.logger.info("⏳ Waiting for responses...")
    await asyncio.sleep(15)

@tester.on_message(model=InvestigationReport)
async def handle_report(ctx: Context, sender: str, msg: InvestigationReport):
    ctx.logger.info(f"🎉 SUCCESS! Received investigation report from {sender}")
    ctx.logger.info(f"📋 Case: {msg.case_id}")
    ctx.logger.info(f"🔍 Hypotheses: {len(msg.hypotheses)}")
    for i, hypothesis in enumerate(msg.hypotheses):
        ctx.logger.info(f"   Hypothesis {i+1}: {hypothesis}")

if __name__ == "__main__":
    tester.run()
