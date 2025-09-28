# test_story_case.py
import asyncio
import sys
from uagents import Agent, Context
from models import InformantTip, InvestigationReport

dispatch_agent = Agent(name="Dispatch", seed="precinct-41-dispatch-seed-final", port=8889, mailbox=True)
COLLECTOR_ADDRESS = "agent1qdznt02at3xqpc9g6hlytt3ustd6edwh0ujtvrhtkshjv7eyckdskwpy6rh"

reports_received = 0
total_tips = 4

@dispatch_agent.on_event("startup")
async def run_case(ctx: Context):
    case_id = "DE-01-MARTINAISIE-HANGING"
    ctx.logger.info(f"DISPATCH: Initiating case {case_id}.")

    tips = [
        "Initial report: A man's body is hanging from a tree behind the Whirling-in-Rags hostel.",
        "Forensic analysis: The cause of death was a gunshot. The hanging was staged. This is a murder, not a suicide.",
        "Witness testimony: A guest named Klaasje Amandou reports hearing a 'terrible scream' and a gunshot two nights ago.",
        "Motive theory: The victim was a corporate mercenary from Krenel. Union Leader Evrart Claire suggests the murder was an act of 'wild justice' by the local dockworkers faction."
    ]
    
    for i, tip_text in enumerate(tips):
        tip = InformantTip(case_id=case_id, text=tip_text, reply_to=ctx.agent.address)
        await ctx.send(COLLECTOR_ADDRESS, tip)
        ctx.logger.info(f"DISPATCH: Transmitting Tip #{i+1}...")
        await asyncio.sleep(25)

@dispatch_agent.on_message(model=InvestigationReport)
async def handle_report(ctx: Context, sender: str, msg: InvestigationReport):
    global reports_received
    reports_received += 1
    ctx.logger.info(f"DISPATCH: Received interim report #{reports_received}...")
    
    if reports_received == total_tips:
        print("\n" + "═"*80)
        print(f"DISPATCH: FINAL COMPREHENSIVE REPORT RECEIVED FOR CASE '{msg.case_id}'")
        print("─"*80)
        print(f"CASE SUMMARY: {msg.case_summary}\n")
        
        print("■ METTA ANALYSIS (LOGICAL FACTS):")
        for finding in msg.metta_analysis:
            print(f"  - [{finding.get('type')}]: {finding.get('content')}")
            
        print("\n■ AI SYNTHESIS (DETECTIVE'S THOUGHTS):")
        print(msg.ai_synthesis)
        
        print("\n" + "═"*80)
        print("\nDISPATCH: Test complete.")
        sys.exit(0)

if __name__ == "__main__":
    dispatch_agent.run()
