# test_interactive_case.py
import asyncio
import sys
import requests
from uagents import Agent, Context, Bureau
from models import InformantTip, InvestigationReport, PoliceChatMessage, PoliceChatResponse

# This test now acts as the "Police Department" user
police_dept = Agent(name="PoliceDept", seed="police-dept-test-seed", port=8889, mailbox=True)

COLLECTOR_ADDRESS = "agent1qdznt02at3xqpc9g6hlytt3ustd6edwh0ujtvrhtkshjv7eyckdskwpy6rh"
DETECTIVE_WEBHOOK = "http://127.0.0.1:8002/ask_detective"

@police_dept.on_event("startup")
async def run_interactive_test(ctx: Context):
    case_id = "DE-01-MARTINAISIE-HANGING"
    ctx.logger.info(f"POLICE DEPT: Opening new case file: {case_id}")
    
    # 1. Submit the initial tip to the collector
    tip = InformantTip(
        case_id=case_id,
        text="Initial patrol report: A male victim has been discovered hanging from a tree behind the Whirling-in-Rags hostel.",
        reply_to=ctx.agent.address
    )
    await ctx.send(COLLECTOR_ADDRESS, tip)
    ctx.logger.info("POLICE DEPT: Initial tip sent to collector. Awaiting detective's synthesis...")

# This handler receives the main report after evidence is processed
@police_dept.on_message(model=InvestigationReport)
async def handle_main_report(ctx: Context, sender: str, msg: InvestigationReport):
    ctx.logger.info("POLICE DEPT: Detective's initial report received. Reviewing...")
    print("\n" + "═"*80)
    print(f"INITIAL REPORT FROM DETECTIVE {sender}")
    print(f"CASE: {msg.case_id}\nSUMMARY: {msg.case_summary}")
    print("═"*80)
    
    # 2. Now, ask a follow-up question via the detective's webhook
    ctx.logger.info("POLICE DEPT: Report looks good. Asking a follow-up question...")
    
    question_payload = {
        "case_id": msg.case_id,
        "question": "What is the primary location of interest in this case?"
    }
    
    # The webhook is not an agent, so we use a standard HTTP library like requests
    # We send the question and then wait for the reply on our agent's mailbox
    try:
        response = requests.post(DETECTIVE_WEBHOOK, json=question_payload, timeout=10)
        if response.status_code != 200:
             ctx.logger.error(f"Failed to send question to webhook: {response.text}")
    except Exception as e:
        ctx.logger.error(f"Error calling webhook: {e}")

# This handler receives the answer to the specific question
@police_dept.on_message(model=PoliceChatResponse)
async def handle_chat_response(ctx: Context, sender: str, msg: PoliceChatResponse):
    ctx.logger.info("POLICE DEPT: Received response to our question.")
    print("\n" + "═"*80)
    print(f"DETECTIVE'S RESPONSE to our question:")
    print(f">> {msg.response_text}")
    print("═"*80)
    ctx.logger.info("POLICE DEPT: Test complete. All systems nominal.")
    sys.exit(0)

if __name__ == "__main__":
    police_dept.run()
