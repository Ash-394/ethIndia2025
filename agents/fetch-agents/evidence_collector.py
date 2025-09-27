# FIXED evidence_collector.py
import os
import json
import asyncio
import threading
import time
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from models import EvidenceMetadata, InvestigationReport

load_dotenv()

# Keys
ASI_KEY = os.getenv("ASI_API_KEY")
AGENTVERSE_KEY = os.getenv("AGENTVERSE_API_KEY")

client = OpenAI(api_key=ASI_KEY, base_url="https://api.asi1.ai/v1")

# Dynamic Metta graph in memory
METTA_GRAPH = {"cases": {}}

kim = Agent(
    name="Kim",
    seed="kim-secure-seed-12345",
    port=8000,
    mailbox=True,
)

fund_agent_if_low(kim.wallet.address())

@kim.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("🚀 Kim (Evidence Collector) READY")
    ctx.logger.info(f"📍 Address: {ctx.agent.address}")
    ctx.logger.info(f"🔑 Using ASI key: {bool(ASI_KEY)}, Agentverse key: {bool(AGENTVERSE_KEY)}")   

async def enrich_evidence_with_llm(evidence: Dict[str, dict]) -> Dict:
    """Send evidence to ASI One to create nodes and edges dynamically."""
    text = str(evidence)
    try:
        r = client.chat.completions.create(
            model="asi1-mini",
            messages=[
                {"role": "system", "content": "Analyze this evidence and return JSON with 'nodes' and 'edges' for a knowledge graph."},
                {"role": "user", "content": text},
            ],
            max_tokens=1024,
        )
        return json.loads(r.choices[0].message.content)
    except Exception as e:
        print(f"LLM error: {e}")
        return {"nodes": [], "edges": []}

@kim.on_message(model=EvidenceMetadata)
async def collect_evidence(ctx: Context, sender: str, msg: EvidenceMetadata):
    ctx.logger.info(f"🔥 Evidence received from {sender}")
    ctx.logger.info(f"📄 Data: {msg.evidence}")

    case_id = "case_001"
    if case_id not in METTA_GRAPH["cases"]:
        METTA_GRAPH["cases"][case_id] = {"nodes": [], "edges": []}

    # Enrich evidence with LLM analysis
    enriched = await enrich_evidence_with_llm(msg.evidence)
    METTA_GRAPH["cases"][case_id]["nodes"].extend(enriched.get("nodes", []))
    METTA_GRAPH["cases"][case_id]["edges"].extend(enriched.get("edges", []))

    ctx.logger.info(f"📊 Metta graph updated: {len(METTA_GRAPH['cases'][case_id]['nodes'])} nodes")

    # Forward to Harry - use the correct address from your logs
    HARRY_ADDRESS = "agent1qvj30dp74r50tgnkzywq0vp2xj5kkkdk86mvltjmmqgkv8qqhstqqh66lux"
    await ctx.send(HARRY_ADDRESS, msg)
    ctx.logger.info("📤 Evidence forwarded to Harry")

@kim.on_message(model=InvestigationReport)
async def handle_report(ctx: Context, sender: str, msg: InvestigationReport):
    ctx.logger.info(f"📊 Investigation report received from {sender}")
    ctx.logger.info(f"📋 Case: {msg.case_id}, Hypotheses: {len(msg.hypotheses)}")
    for i, hypothesis in enumerate(msg.hypotheses):
        ctx.logger.info(f"   Hypothesis {i+1}: {hypothesis.get('summary', 'No summary')}")

# REMOVED the problematic catch_all handler with model=object

# ----------------------------
# Webhook Server (optional)
# ----------------------------

def create_webhook_app(kim_agent):
    from fastapi import FastAPI, Request
    import uvicorn

    app = FastAPI()

    @app.post("/submit-evidence")
    async def submit_evidence(request: Request):
        try:
            data = await request.json()
            evidence_data = data.get("evidence", {})
            msg = EvidenceMetadata(evidence=evidence_data)

            # Schedule message sending in Kim's event loop
            def send_msg():
                loop = kim_agent._loop
                if loop and loop.is_running():
                    asyncio.run_coroutine_threadsafe(
                        kim_agent._ctx.send(kim_agent.address, msg),
                        loop
                    )

            # Run in a thread to avoid blocking
            threading.Thread(target=send_msg, daemon=True).start()

            return {"status": "Evidence accepted", "evidence": evidence_data}
        except Exception as e:
            return {"error": str(e)}

    return app

if __name__ == "__main__":
    # Option 1: Run just the agent
    kim.run()
    
    # Option 2: Run with webhook (comment out kim.run() above and uncomment below)
    """
    # Start Kim in a background thread
    def run_kim():
        kim.run()

    kim_thread = threading.Thread(target=run_kim, daemon=True)
    kim_thread.start()

    # Wait for Kim to initialize
    time.sleep(3)

    # Start webhook server on port 8003
    import uvicorn
    webhook_app = create_webhook_app(kim)
    print("🌐 Webhook server starting on http://localhost:8003/submit-evidence")
    uvicorn.run(webhook_app, host="0.0.0.0", port=8003)
    """
