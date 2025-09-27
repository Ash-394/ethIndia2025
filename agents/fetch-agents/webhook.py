# webhook_server.py
from fastapi import FastAPI, Request
import asyncio
import threading
from evidence_collector import kim, EvidenceMetadata

app = FastAPI()

@app.post("/submit-evidence")
async def submit_evidence(request: Request):
    data = await request.json()
    evidence_data = data.get("evidence", {})
    
    # Send message to Kim (must run in Kim's event loop)
    async def send_to_kim():
        msg = EvidenceMetadata(evidence=evidence_data)
        await kim._ctx.send(kim.address, msg)  # Not ideal, but works for testing

    # Schedule in Kim's loop (hacky but functional for local test)
    asyncio.run_coroutine_threadsafe(send_to_kim(), kim._loop)
    
    return {"status": "Evidence queued for Kim"}
