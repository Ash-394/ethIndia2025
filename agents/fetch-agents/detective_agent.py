# detective_agent.py
import os
import re
import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, Any, List
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from models import InvestigationReport, CaseFileUpdate

load_dotenv()
ASI_KEY = os.getenv("ASI_API_KEY")

client = OpenAI(api_key=ASI_KEY, base_url="https://api.asi1.ai/v1")

# Agent Name: LeadDetective | Seed: enhanced-harry-metta-detective
detective_agent = Agent(name="LeadDetective", seed="enhanced-harry-metta-detective", port=8001, mailbox=True)
fund_agent_if_low(detective_agent.wallet.address())

async def synthesize_case_file(ctx: Context, evidence_log: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Uses AI to synthesize all evidence into a coherent theory."""
    evidence_text = json.dumps(evidence_log, indent=2)
    prompt = f"""
    You are a Lead Detective AI. Your task is to analyze a complete case file and generate a high-level synthesis for a human analyst.
    Analyze the JSON case file below. Return a single JSON object with three keys:
    1. "case_summary": A brief, professional summary of the investigation's current status.
    2. "key_entities": A dictionary of lists, summarizing all unique 'persons', 'locations', and 'items' from the entire file.
    3. "ai_synthesis": This is the core of your task. Generate a detailed analytical synthesis. Identify potential motives, murder weapons, compelling evidence, circumstantial evidence, and any contradictions or unanswered questions. Structure this as a professional intelligence report.

    CASE FILE:
    {evidence_text}
    """
    try:
        r = client.chat.completions.create(
            model="asi1-mini", messages=[{"role": "user", "content": prompt}], max_tokens=2048
        )
        response_content = r.choices[0].message.content
        match = re.search(r"```(json)?\s*([\s\S]*?)\s*```", response_content)
        clean_content = match.group(2) if match else response_content
        return json.loads(clean_content)
    except Exception as e:
        ctx.logger.error(f"DETECTIVE: AI synthesis failed: {e}")
        return {}

@detective_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"LEAD DETECTIVE AGENT: Online. Address: {ctx.agent.address}")

@detective_agent.on_message(model=CaseFileUpdate)
async def analyze_case_file(ctx: Context, sender: str, msg: CaseFileUpdate):
    ctx.logger.info(f"DETECTIVE: Received updated case file '{msg.case_id}' from {sender}. Beginning synthesis...")

    synthesis = await synthesize_case_file(ctx, msg.full_evidence_log)

    # ** THE FIX IS HERE: Convert the 'ai_synthesis' part to a string **
    synthesis_text = str(synthesis.get("ai_synthesis", "Could not generate synthesis."))

    final_report = InvestigationReport(
        case_id=msg.case_id,
        evidence_log=msg.full_evidence_log,
        case_summary=synthesis.get("case_summary", "Synthesis failed."),
        key_entities=synthesis.get("key_entities", {}),
        ai_synthesis=synthesis_text # Use the converted string here
    )

    # Note: The webhook has no mailbox, so this send will not deliver a reply.
    # The success is seeing the log message below without errors.
    if msg.reply_to:
        await ctx.send(msg.reply_to, final_report)
    
    ctx.logger.info(f"DETECTIVE: Synthesis complete. Final report for '{msg.case_id}' created successfully.")

if __name__ == "__main__":
    detective_agent.run()
