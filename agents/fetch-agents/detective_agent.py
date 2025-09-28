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

# Import FastAPI and WebSocket components
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

load_dotenv()
ASI_KEY = os.getenv("ASI_API_KEY")
client = OpenAI(api_key=ASI_KEY, base_url="https://api.asi1.ai/v1")

detective_agent = Agent(name="LeadDetective", seed="enhanced-harry-metta-detective", port=8001, mailbox=True)

# --- WebSocket Connection Manager ---
# This dictionary will store active frontend connections, organized by case_id
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, case_id: str):
        await websocket.accept()
        if case_id not in self.active_connections:
            self.active_connections[case_id] = []
        self.active_connections[case_id].append(websocket)

    def disconnect(self, websocket: WebSocket, case_id: str):
        if case_id in self.active_connections:
            self.active_connections[case_id].remove(websocket)

    async def push_report(self, case_id: str, report: InvestigationReport):
        if case_id in self.active_connections:
            websockets = self.active_connections[case_id]
            for connection in websockets:
                await connection.send_json(report.model_dump())

manager = ConnectionManager()
case_reports: Dict[str, InvestigationReport] = {}

def create_webhook_app(agent_ctx: Context):
    app = FastAPI()

    # WebSocket endpoint for the frontend to listen on
    @app.websocket("/ws/report/{case_id}")
    async def websocket_endpoint(websocket: WebSocket, case_id: str):
        await manager.connect(websocket, case_id)
        try:
            # Keep the connection alive
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            manager.disconnect(websocket, case_id)
            agent_ctx.logger.info(f"Frontend disconnected from case {case_id}")

    return app

# (The synthesize_case_file function remains the same)
async def synthesize_case_file(ctx: Context, evidence_log: List[Dict[str, Any]]) -> Dict[str, Any]:
    evidence_text = json.dumps(evidence_log, indent=2)
    prompt = f"You are a Lead Detective AI. Analyze this case file and return a JSON object with 'case_summary', 'key_entities', and 'ai_synthesis'. CASE FILE: {evidence_text}"
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
    ctx.logger.info(f"LEAD DETECTIVE AGENT: Online. Address: {ctx.agent.address}")
    app = create_webhook_app(ctx)
    config = uvicorn.Config(app, host="0.0.0.0", port=8002, log_level="info")
    server = uvicorn.Server(config)
    asyncio.create_task(server.serve())
    ctx.logger.info(f"🚀 WebSocket Endpoint: ws://127.0.0.1:8002/ws/report/{{case_id}}")

@detective_agent.on_message(model=CaseFileUpdate)
async def analyze_case_file(ctx: Context, sender: str, msg: CaseFileUpdate):
    ctx.logger.info(f"DETECTIVE: Synthesizing case file '{msg.case_id}'...")
    synthesis = await synthesize_case_file(ctx, msg.full_evidence_log)
    final_report = InvestigationReport(
        case_id=msg.case_id,
        evidence_log=msg.full_evidence_log,
        case_summary=synthesis.get("case_summary", "Synthesis failed."),
        key_entities=synthesis.get("key_entities", {}),
        ai_synthesis=str(synthesis.get("ai_synthesis", "Could not generate synthesis."))
    )
    
    case_reports[msg.case_id] = final_report
    ctx.logger.info(f"DETECTIVE: Synthesis for '{msg.case_id}' complete. Pushing report to frontend...")
    
    # PUSH the final report to any connected frontend clients
    await manager.push_report(msg.case_id, final_report)

if __name__ == "__main__":
    detective_agent.run()
