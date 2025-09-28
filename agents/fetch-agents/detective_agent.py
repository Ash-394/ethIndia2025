# detective_agent.py
import os
import re
import json
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, Any, List
from uagents import Agent, Context
from models import InvestigationReport, CaseFileUpdate
from fastapi import FastAPI
import uvicorn

load_dotenv()
ASI_KEY = os.getenv("ASI_API_KEY")
client = OpenAI(api_key=ASI_KEY, base_url="https://api.asi1.ai/v1")

detective_agent = Agent(name="LeadDetective", seed="enhanced-harry-metta-detective", port=8001, mailbox=True)
case_reports: Dict[str, InvestigationReport] = {}

def create_webhook_app(agent_ctx: Context):
    # ... (code is unchanged)
    app = FastAPI()
    @app.get("/get_report/{case_id}")
    async def get_report_endpoint(case_id: str):
        report = case_reports.get(case_id)
        if report:
            return {"status": "complete", "report": report.model_dump()}
        else:
            return {"status": "processing"}
    return app

async def synthesize_case_file(ctx: Context, evidence_log: List[Dict[str, Any]]) -> Dict[str, Any]:
    evidence_text = json.dumps(evidence_log, indent=2)
    
    # --- NEW, UPGRADED PROMPT ---
    prompt = f"""
    You are the Lead Detective assigned to this case. In the evidence files, you are sometimes referred to as 'Harry'.
    When you see 'Harry', that's you. Synthesize the entire case file from your first-person perspective.
    
    Your response MUST be a single JSON object with the following keys:
    1. "case_summary": Write a brief, first-person summary of the case. (e.g., "My investigation currently involves...")
    2. "key_entities": A dictionary of lists, summarizing all unique 'persons', 'locations', and 'items'.
    3. "ai_synthesis": Your internal monologue. What are your thoughts? What are the connections, motives, and contradictions?
    4. "confidence_level": Your confidence in your current synthesis ('Low', 'Medium', 'High').
    5. "recommended_next_steps": A list of 2-3 concrete actions you should take next to move the investigation forward.

    CASE FILE:
    {evidence_text}
    """
    try:
        r = client.chat.completions.create(model="asi1-mini", messages=[{"role": "user", "content": prompt}], max_tokens=2048)
        response_content = r.choices[0].message.content
        match = re.search(r"```(json)?\s*([\s\S]*?)\s*```", response_content)
        clean_content = match.group(2) if match else response_content
        return json.loads(clean_content)
    except Exception as e:
        ctx.logger.error(f"DETECTIVE: AI synthesis failed: {e}")
        return {}

@detective_agent.on_event("startup")
async def startup(ctx: Context):
    # ... (code is unchanged)
    ctx.logger.info(f"LEAD DETECTIVE AGENT: Online. Address: {ctx.agent.address}")
    app = create_webhook_app(ctx)
    config = uvicorn.Config(app, host="0.0.0.0", port=8002, log_level="info")
    server = uvicorn.Server(config)
    asyncio.create_task(server.serve())
    ctx.logger.info(f"🚀 Get Report Endpoint: http://127.0.0.1:8002/get_report/{{case_id}}")

@detective_agent.on_message(model=CaseFileUpdate)
async def analyze_case_file(ctx: Context, sender: str, msg: CaseFileUpdate):
    ctx.logger.info(f"DETECTIVE: Synthesizing case file '{msg.case_id}'...")
    synthesis = await synthesize_case_file(ctx, msg.full_evidence_log)
    
    final_report = InvestigationReport(
        case_id=msg.case_id,
        evidence_log=msg.full_evidence_log,
        case_summary=synthesis.get("case_summary", "Synthesis failed."),
        key_entities=synthesis.get("key_entities", {}),
        ai_synthesis=str(synthesis.get("ai_synthesis", "Could not generate synthesis.")),
        # Populate the new fields
        confidence_level=synthesis.get("confidence_level", "Unknown"),
        recommended_next_steps=synthesis.get("recommended_next_steps", [])
    )
    
    case_reports[msg.case_id] = final_report
    
    if msg.reply_to:
        await ctx.send(msg.reply_to, final_report)
    
    ctx.logger.info(f"DETECTIVE: Synthesis for '{msg.case_id}' complete. Report is now available.")

if __name__ == "__main__":
    detective_agent.run()
