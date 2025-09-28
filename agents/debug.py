# debug_evidence_agent.py
from uagents import Agent, Context, Model
from uagents.communication import DeliveryStatus
from typing import List, Dict
import asyncio

class EvidenceMetadata(Model):
    evidence: Dict[str, dict]

class InvestigationReport(Model):
    case_id: str
    hypotheses: List[Dict]

class DebugMessage(Model):
    message: str

evidence_agent = Agent(
    name="evidence-analyst",
    seed="your-secure-seed-12345",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"]
)

@evidence_agent.on_event("startup")
async def startup_event(ctx: Context):
    ctx.logger.info(f"🚀 Evidence agent started")
    ctx.logger.info(f"📍 Address: {ctx.agent.address}")
    ctx.logger.info(f"🌐 Endpoints: {ctx.agent.endpoints}")
    ctx.logger.info(f"💼 Wallet: {ctx.agent.wallet.address()}")

# Catch ALL messages - any type
@evidence_agent.on_message(model=Model)
async def catch_everything(ctx: Context, sender: str, msg: Model):
    ctx.logger.info(f"🔥 GOT MESSAGE!")
    ctx.logger.info(f"   Type: {type(msg).__name__}")
    ctx.logger.info(f"   From: {sender}")
    ctx.logger.info(f"   Content: {msg}")
    
    # If it's evidence, process it
    if isinstance(msg, EvidenceMetadata):
        ctx.logger.info("✅ This is evidence data!")
        
        pois = set()
        evidence_used = []
        
        for evid_id, data in msg.evidence.items():
            if "shows_person" in data:
                pois.add(data["shows_person"])
                evidence_used.append(evid_id)
            if "claims" in data and "suspect" in data["claims"]:
                pois.add(data["claims"]["suspect"])
                evidence_used.append(evid_id)
        
        report = InvestigationReport(
            case_id=f"case-{len(evidence_used)}",
            hypotheses=[{
                "summary": "Debug analysis complete",
                "persons_of_interest": list(pois),
                "evidence_used": evidence_used,
                "confidence": 0.9
            }]
        )
        
        ctx.logger.info(f"📤 SENDING REPORT: {report}")
        try:
            await ctx.send(sender, report)
            ctx.logger.info("✅ Report sent successfully")
        except Exception as e:
            ctx.logger.error(f"❌ Failed to send report: {e}")

if __name__ == "__main__":
    evidence_agent.run()


# =====================================
# debug_demo_client.py  
from uagents import Agent, Context, Model
from uagents.communication import DeliveryStatus
import asyncio

class EvidenceMetadata(Model):
    evidence: Dict[str, dict]

class InvestigationReport(Model):
    case_id: str
    hypotheses: List[Dict]

demo_client = Agent(
    name="demo-client",
    seed="client-secure-seed-67890", 
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"]
)

# HARDCODE THE EXACT ADDRESS FROM YOUR LOGS
EVIDENCE_AGENT_ADDRESS = "agent1qv7ffp2kxteduqxyl897ru6gd948ygqjp6k0vphc0x0xykpz927cz82nv0d"

@demo_client.on_event("startup")
async def startup_event(ctx: Context):
    ctx.logger.info(f"📱 Demo client started")
    ctx.logger.info(f"📍 Address: {ctx.agent.address}")
    ctx.logger.info(f"🎯 Target: {EVIDENCE_AGENT_ADDRESS}")
    ctx.logger.info(f"🌐 Endpoints: {ctx.agent.endpoints}")

# Send evidence immediately on startup, then every 20 seconds
@demo_client.on_event("startup")
async def send_initial_evidence(ctx: Context):
    await asyncio.sleep(5)  # Wait 5 seconds
    await send_evidence_now(ctx)

@demo_client.on_interval(period=20.0)
async def send_evidence_interval(ctx: Context):
    await send_evidence_now(ctx)

async def send_evidence_now(ctx: Context):
    evidence = EvidenceMetadata(
        evidence={
            "ev_001": {"shows_person": "DebugPerson1", "type": "video"},
            "ev_002": {"claims": {"suspect": "DebugSuspect1", "crime": "debug_crime"}}
        }
    )
    
    ctx.logger.info("🔥 ATTEMPTING TO SEND EVIDENCE...")
    ctx.logger.info(f"   To: {EVIDENCE_AGENT_ADDRESS}")
    ctx.logger.info(f"   Data: {evidence}")
    
    try:
        # Try different send approaches
        ctx.logger.info("📤 Method 1: Normal send...")
        await ctx.send(EVIDENCE_AGENT_ADDRESS, evidence)
        ctx.logger.info("✅ Method 1: Send completed (no exception)")
        
    except Exception as e:
        ctx.logger.error(f"❌ Method 1 failed: {e}")
        ctx.logger.error(f"❌ Exception type: {type(e)}")
        
    # Also try sending a simple debug message
    try:
        ctx.logger.info("📤 Method 2: Sending debug message...")
        debug_msg = {"message": "Hello from client"}
        await ctx.send(EVIDENCE_AGENT_ADDRESS, debug_msg)
        ctx.logger.info("✅ Method 2: Debug message sent")
    except Exception as e:
        ctx.logger.error(f"❌ Method 2 failed: {e}")

# Catch ALL incoming messages
@demo_client.on_message(model=Model) 
async def catch_everything(ctx: Context, sender: str, msg: Model):
    ctx.logger.info(f"🎉 GOT RESPONSE!")
    ctx.logger.info(f"   Type: {type(msg).__name__}")
    ctx.logger.info(f"   From: {sender}")
    ctx.logger.info(f"   Content: {msg}")

if __name__ == "__main__":
    demo_client.run()
