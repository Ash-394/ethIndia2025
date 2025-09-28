# evidence_collector_kim.py
import os
import re
import json
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, Any, List
from uagents import Agent, Context
from models import InformantTip, MeTTaScriptUpdate
from fastapi import FastAPI, Request
import uvicorn

load_dotenv()
ASI_KEY = os.getenv("ASI_API_KEY")
client = OpenAI(api_key=ASI_KEY, base_url="https://api.asi1.ai/v1")

collector_agent = Agent(name="EvidenceCollector", seed="kim-secure-seed-12345", port=8000, mailbox=True)

case_scripts: Dict[str, str] = {}
DETECTIVE_ADDRESS = "agent1qf84uk2kup2lfttgv8av3l2aeytu2vn6psufyncp76gsg68nr2k5z6q9cdj"

async def generate_metta_from_tip(ctx: Context, tip_text: str) -> str:
    """Uses a sophisticated AI prompt to translate narrative into a MeTTa script."""
    prompt = f"""
    You are an AI that translates field reports into a MeTTa script.
    Analyze the text and convert it into a series of MeTTa assertions.
    Use predicates: Person, Location, Item, Suspect, Witness, Faction, cause_of_death, seen_at, testimony, motive_theory, staged_scene, contradiction.
    Each assertion must be on a new line and start with `! `. Entities should be in double quotes.

    Example: 'Witness Sylvie saw the suspect, a Krenel merc, at the Whirling-in-Rags hostel. He had a gun.'
    ! (Witness "Sylvie")
    ! (Faction "Krenel")
    ! (Suspect "Krenel Mercenary")
    ! (Person "Sylvie")
    ! (Person "Krenel Mercenary")
    ! (Location "Whirling-in-Rags")
    ! (Item "Gun")
    ! (Weapon "Gun")
    ! (seen_at "Krenel Mercenary" "Whirling-in-Rags")
    ! (has_item "Krenel Mercenary" "Gun")
    ! (testimony "Sylvie" "Saw the suspect at the hostel with a gun.")

    TEXT TO TRANSLATE: "{tip_text}"
    """
    try:
        r = client.chat.completions.create(
            model="asi1-mini", messages=[{"role": "user", "content": prompt}], max_tokens=1024
        )
        return r.choices[0].message.content.strip()
    except Exception as e:
        ctx.logger.error(f"COLLECTOR: MeTTa script generation failed: {e}")
        return ""

@collector_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("COLLECTOR AGENT (MeTTa Scripter): Online.")
    app = create_webhook_app(ctx)
    config = uvicorn.Config(app, host="0.0.0.0", port=8003, log_level="info")
    server = uvicorn.Server(config)
    asyncio.create_task(server.serve())
    ctx.logger.info(f"🚀 Webhook is live! Send tips to http://127.0.0.1:8003/submit_tip")

@collector_agent.on_message(model=InformantTip)
async def handle_tip(ctx: Context, sender: str, msg: InformantTip):
    ctx.logger.info(f"COLLECTOR: Received tip for case '{msg.case_id}'. Translating to MeTTa...")
    if msg.case_id not in case_scripts: case_scripts[msg.case_id] = ""
    new_script_chunk = await generate_metta_from_tip(ctx, msg.text)
    if new_script_chunk:
        case_scripts[msg.case_id] += "\n" + new_script_chunk
    update = MeTTaScriptUpdate(
        case_id=msg.case_id,
        cumulative_script=case_scripts[msg.case_id],
        reply_to=msg.reply_to
    )
    await ctx.send(DETECTIVE_ADDRESS, update)
    ctx.logger.info(f"COLLECTOR: Full MeTTa script for '{msg.case_id}' sent to Detective.")

def create_webhook_app(agent_ctx: Context):
    app = FastAPI()
    @app.post("/submit_tip")
    async def submit_tip_endpoint(request: Request):
        data = await request.json()
        tip_msg = InformantTip(case_id=data.get("case_id"), text=data.get("text"), reply_to=data.get("reply_to"))
        await agent_ctx.send(agent_ctx.agent.address, tip_msg)
        return {"status": "success", "message": "Tip received and is being processed."}
    return app

if __name__ == "__main__":
    collector_agent.run()
