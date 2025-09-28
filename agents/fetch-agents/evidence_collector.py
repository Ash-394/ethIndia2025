# evidence_collector.py
import os
import json
import re
import asyncio
from dotenv import load_dotenv
from typing import Dict, Any, List
from uagents import Agent, Context
from models import InformantTip, CaseFileUpdate
from openai import OpenAI

from fastapi import FastAPI, Request
import uvicorn

# Load API key from .env
load_dotenv()
ASI_KEY = os.getenv("ASI_API_KEY")
client = OpenAI(api_key=ASI_KEY, base_url="https://api.asi1.ai/v1")

# Agent initialization with the essential mailbox parameter
collector_agent = Agent(
    name="EvidenceCollector",
    seed="kim-secure-seed-12345",
    port=8000,
    mailbox=True  # RE-ADDED: This is critical for receiving replies from other agents
)

case_files: Dict[str, List[Dict[str, Any]]] = {}
DETECTIVE_ADDRESS = "agent1qf84uk2kup2lfttgv8av3l2aeytu2vn6psufyncp76gsg68nr2k5z6q9cdj"

def create_webhook_app(agent_ctx: Context):
    app = FastAPI()

    @app.post("/submit_tip")
    async def submit_tip_endpoint(request: Request):
        try:
            data = await request.json()
            case_id = data.get("case_id")
            text = data.get("text")
            reply_to = data.get("reply_to") # Good addition!

            if not case_id or not text:
                return {"status": "error", "message": "Missing 'case_id' or 'text'"}

            tip_msg = InformantTip(case_id=case_id, text=text, reply_to=reply_to)
            await agent_ctx.send(agent_ctx.address, tip_msg)
            return {"status": "success", "message": "Tip received and is being processed."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    return app

async def categorize_tip(ctx: Context, tip_text: str) -> Dict[str, Any]:
    prompt = f"""
    Analyze the following field report text and convert it into a structured JSON evidence object.
    The JSON object must have three keys:
    1. "type": A professional evidence category (e.g., 'Initial Report', 'Witness Testimony', 'Forensic Detail').
    2. "summary": A concise, one-sentence summary of the information.
    3. "entities": A dictionary of lists, identifying all 'persons', 'locations', or 'items'.
    REPORT TEXT: "{tip_text}"
    """
    try:
        r = client.chat.completions.create(
            model="asi1-mini", messages=[{"role": "user", "content": prompt}], max_tokens=1024
        )
        response_content = r.choices[0].message.content
        match = re.search(r"```(json)?\s*([\s\S]*?)\s*```", response_content)
        clean_content = match.group(2) if match else response_content
        return json.loads(clean_content)
    except Exception as e:
        ctx.logger.error(f"COLLECTOR: AI categorization failed: {e}")
        return {}

@collector_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"COLLECTOR AGENT: Online. Address: {ctx.agent.address}")
    app = create_webhook_app(ctx)
    config = uvicorn.Config(app, host="0.0.0.0", port=8003, log_level="info")
    server = uvicorn.Server(config)
    asyncio.create_task(server.serve())
    ctx.logger.info(f"🚀 Webhook is live! Send tips to http://127.0.0.1:8003/submit_tip")

@collector_agent.on_message(model=InformantTip)
async def handle_tip(ctx: Context, sender: str, msg: InformantTip):
    ctx.logger.info(f"COLLECTOR: Received tip for case '{msg.case_id}'. Processing...")
    if msg.case_id not in case_files:
        case_files[msg.case_id] = []
    categorized_evidence = await categorize_tip(ctx, msg.text)
    if categorized_evidence:
        case_files[msg.case_id].append(categorized_evidence)
        ctx.logger.info(
            f"COLLECTOR: Evidence logged. Total entries for case '{msg.case_id}': {len(case_files[msg.case_id])}"
        )
    update = CaseFileUpdate(
        case_id=msg.case_id,
        full_evidence_log=case_files[msg.case_id],
        reply_to=msg.reply_to,
    )
    await ctx.send(DETECTIVE_ADDRESS, update)
    ctx.logger.info(f"COLLECTOR: Full case file for '{msg.case_id}' sent to Detective unit.")

if __name__ == "__main__":
    collector_agent.run()
