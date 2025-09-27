# enhanced_metta_agent.py - Real MeTTa Integration
import os
from dotenv import load_dotenv
from typing import Dict, List, Any
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from openai import OpenAI

# MeTTa Integration
try:
    from hyperon import MeTTa, E, ValueAtom
    METTA_AVAILABLE = True
except ImportError:
    print("Installing hyperon-experimental...")
    import subprocess
    subprocess.check_call(["pip", "install", "hyperon-experimental"])
    from hyperon import MeTTa, E, ValueAtom
    METTA_AVAILABLE = True

from models import EvidenceMetadata, InvestigationReport

load_dotenv()

ASI_KEY = os.getenv("ASI_API_KEY")
client = OpenAI(api_key=ASI_KEY, base_url="https://api.asi1.ai/v1")

class MeTTaReasoningEngine:
    def __init__(self):
        self.metta = MeTTa()
        self.setup_base_knowledge()
    
    def setup_base_knowledge(self):
        """Initialize MeTTa with base reasoning rules for evidence analysis"""
        # Define evidence analysis rules in MeTTa
        base_rules = """
        ; Evidence relationship rules
        (= (related-evidence $x $y) 
           (if (and (person-in-evidence $x $p) (person-in-evidence $y $p)) True False))
        
        ; Suspect identification rules  
        (= (potential-suspect $person)
           (if (suspect-claim $person) True
               (if (> (evidence-count $person) 2) True False)))
        
        ; Location clustering rules
        (= (same-area $loc1 $loc2)
           (if (< (location-distance $loc1 $loc2) 1000) True False))
        
        ; Timeline analysis rules
        (= (suspicious-timeline $person)
           (if (> (timeline-gaps $person) 1) True False))
        
        ; Evidence strength assessment
        (= (strong-evidence $evidence)
           (if (> (confidence-score $evidence) 0.8) True False))
        """
        
        # Load rules into MeTTa space
        for line in base_rules.strip().split('\n'):
            if line.strip() and not line.strip().startswith(';'):
                try:
                    self.metta.run(line)
                except Exception as e:
                    print(f"MeTTa rule error: {e}")
    
    def add_evidence_to_metta(self, evidence_id: str, evidence_data: Dict):
        """Convert evidence to MeTTa facts"""
        try:
            # Add person facts
            if 'shows_person' in evidence_data:
                person = evidence_data['shows_person']
                self.metta.run(f"(person-in-evidence {evidence_id} {person})")
                
                # Add claims
                if 'claims' in evidence_data:
                    for claim, value in evidence_data['claims'].items():
                        if value:
                            self.metta.run(f"({claim} {person})")
            
            # Add location facts
            if 'location' in evidence_data:
                location = evidence_data['location'].replace(' ', '_')
                self.metta.run(f"(evidence-location {evidence_id} {location})")
            
            # Add timestamp if available
            if 'timestamp' in evidence_data:
                timestamp = evidence_data['timestamp']
                self.metta.run(f"(evidence-time {evidence_id} {timestamp})")
                
            print(f"✅ Added evidence {evidence_id} to MeTTa space")
            
        except Exception as e:
            print(f"❌ MeTTa evidence addition error: {e}")
    
    def reason_about_case(self, case_id: str) -> List[Dict]:
        """Use MeTTa reasoning to generate hypotheses"""
        try:
            # Query for suspects
            suspects_query = "(potential-suspect $x)"
            suspects = self.metta.run(suspects_query)
            
            # Query for related evidence
            relations_query = "(related-evidence $x $y)"
            relations = self.metta.run(relations_query)
            
            # Query for strong evidence
            strong_evidence_query = "(strong-evidence $x)"
            strong_evidence = self.metta.run(strong_evidence_query)
            
            # Build reasoning-based hypotheses
            hypotheses = []
            
            if suspects:
                hypotheses.append({
                    "type": "suspect_identification",
                    "reasoning": "MeTTa logical inference identified potential suspects",
                    "suspects": [str(s) for s in suspects],
                    "confidence": 0.85,
                    "metta_derived": True
                })
            
            if relations:
                hypotheses.append({
                    "type": "evidence_correlation", 
                    "reasoning": "MeTTa found correlations between evidence items",
                    "correlations": [{"evidence_a": str(r[0]), "evidence_b": str(r[1])} for r in relations],
                    "confidence": 0.75,
                    "metta_derived": True
                })
            
            return hypotheses if hypotheses else [{
                "type": "initial_analysis",
                "reasoning": "MeTTa base analysis - insufficient data for complex inference",
                "confidence": 0.5,
                "metta_derived": True
            }]
            
        except Exception as e:
            print(f"❌ MeTTa reasoning error: {e}")
            return [{
                "type": "error_fallback",
                "reasoning": f"MeTTa reasoning failed: {e}",
                "confidence": 0.3,
                "metta_derived": False
            }]

# Enhanced Detective Agent with MeTTa
class EnhancedDetectiveAgent:
    def __init__(self):
        self.metta_engine = MeTTaReasoningEngine()
        self.case_data = {}
        
        self.agent = Agent(
            name="EnhancedHarry",
            seed="enhanced-harry-metta-seed",
            port=8001,
            mailbox=True,
        )
        
        fund_agent_if_low(self.agent.wallet.address())
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.agent.on_event("startup")
        async def startup(ctx: Context):
            ctx.logger.info("🧠 Enhanced Detective with MeTTa READY")
            ctx.logger.info(f"📍 Address: {ctx.agent.address}")
            ctx.logger.info(f"🔮 MeTTa Engine: {'✅ Active' if METTA_AVAILABLE else '❌ Failed'}")
        
        @self.agent.on_message(model=EvidenceMetadata)
        async def analyze_with_metta(ctx: Context, sender: str, msg: EvidenceMetadata):
            ctx.logger.info(f"🧠 Enhanced analysis starting for evidence from {sender}")
            
            case_id = "case_001"
            if case_id not in self.case_data:
                self.case_data[case_id] = {"evidence_items": [], "metta_facts": []}
            
            # Store evidence
            self.case_data[case_id]["evidence_items"].append(msg.evidence)
            
            # Add each evidence item to MeTTa
            for evidence_id, evidence_data in msg.evidence.items():
                self.metta_engine.add_evidence_to_metta(evidence_id, evidence_data)
                ctx.logger.info(f"📊 Added {evidence_id} to MeTTa reasoning space")
            
            # Get AI-enhanced analysis
            ai_analysis = await self.get_ai_insights(msg.evidence)
            
            # Get MeTTa reasoning
            metta_hypotheses = self.metta_engine.reason_about_case(case_id)
            
            # Combine AI and MeTTa insights
            combined_hypotheses = metta_hypotheses + [{
                "type": "ai_analysis",
                "reasoning": ai_analysis.get("analysis", "AI analysis completed"),
                "insights": ai_analysis.get("insights", []),
                "confidence": ai_analysis.get("confidence", 0.7),
                "metta_derived": False
            }]
            
            report = InvestigationReport(
                case_id=case_id,
                hypotheses=combined_hypotheses
            )
            
            ctx.logger.info(f"🎯 Enhanced report with {len(combined_hypotheses)} hypotheses ready")
            await ctx.send(sender, report)
    
    async def get_ai_insights(self, evidence: Dict) -> Dict:
        """Get AI insights to complement MeTTa reasoning"""
        try:
            prompt = f"""
            As a detective AI, analyze this evidence and provide insights that complement logical reasoning:
            
            Evidence: {evidence}
            
            Return JSON with:
            - analysis: Brief summary
            - insights: List of key insights
            - confidence: Float 0-1
            """
            
            response = client.chat.completions.create(
                model="asi1-mini",
                messages=[
                    {"role": "system", "content": "You are a detective AI providing insights to complement logical reasoning engines."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {
                "analysis": f"AI analysis error: {e}",
                "insights": ["Error in AI processing"],
                "confidence": 0.3
            }
    
    def run(self):
        self.agent.run()

# Usage
if __name__ == "__main__":
    detective = EnhancedDetectiveAgent()
    detective.run()
