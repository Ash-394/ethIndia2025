# simple_client.py - Minimal version to test communication
from uagents import Agent, Context, Model
from typing import Dict
import asyncio

class EvidenceMetadata(Model):
    evidence: Dict[str, dict]

# Create simple client
client = Agent(
    name="simple-client",
    seed="simple-seed-123",
    port=8001
)

# The EXACT address from your evidence agent logs
TARGET = "agent1qv7ffp2kxteduqxyl897ru6gd948ygqjp6k0vphc0x0xykpz927cz82nv0d"

@client.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"🚀 Simple client started: {ctx.agent.address}")
    ctx.logger.info(f"🎯 Will target: {TARGET}")
    
    # Send evidence after 5 seconds
    await asyncio.sleep(5)
    await send_test(ctx)

async def send_test(ctx: Context):
    evidence = EvidenceMetadata(evidence={
        "test_001": {"shows_person": "TestPerson"}
    })
    
    ctx.logger.info("📤 SENDING TEST EVIDENCE...")
    try:
        await ctx.send(TARGET, evidence)
        ctx.logger.info("✅ SENT!")
    except Exception as e:
        ctx.logger.error(f"❌ FAILED: {e}")

@client.on_message(model=Model)
async def got_message(ctx: Context, sender: str, msg: Model):
    ctx.logger.info(f"🎉 GOT REPLY: {type(msg)} from {sender}")
    ctx.logger.info(f"�� Content: {msg}")

if __name__ == "__main__":
    client.run()
