# multi_agent_reasoning.py - Advanced reasoning system
import os
import asyncio
from typing import Dict, List, Any
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from openai import OpenAI
from dataclasses import dataclass
import json

# New specialized message types
class HypothesisRequest(Model):
    case_id: str
    evidence_summary: Dict[str, Any]
    focus_area: str  # "timeline", "relationships", "motives", "evidence_chain"

class HypothesisResponse(Model):
    case_id: str
    focus_area: str
    hypothesis: Dict[str, Any]
    confidence: float
    supporting_evidence: List[str]

class CollaborativeAnalysis(Model):
    case_id: str
    all_hypotheses: List[Dict[str, Any]]
    consensus_rating: float
    final_assessment: Dict[str, Any]

# Specialized Reasoning Agents
class TimelineAnalyst:
    """Agent specialized in temporal reasoning and timeline construction"""
    
    def __init__(self, port: int = 8010):
        self.agent = Agent(
            name="TimelineAnalyst",
            seed="timeline-analyst-seed",
            port=port,
            mailbox=True
        )
        fund_agent_if_low(self.agent.wallet.address())
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.agent.on_message(model=HypothesisRequest)
        async def analyze_timeline(ctx: Context, sender: str, msg: HypothesisRequest):
            if msg.focus_area != "timeline":
                return
                
            ctx.logger.info(f"⏰ Timeline analysis requested for case {msg.case_id}")
            
            # Analyze temporal patterns
            timeline_hypothesis = await self.build_timeline_hypothesis(msg.evidence_summary)
            
            response = HypothesisResponse(
                case_id=msg.case_id,
                focus_area="timeline",
                hypothesis=timeline_hypothesis,
                confidence=timeline_hypothesis.get("confidence", 0.7),
                supporting_evidence=timeline_hypothesis.get("evidence_ids", [])
            )
            
            await ctx.send(sender, response)
            ctx.logger.info("📊 Timeline hypothesis sent")
    
    async def build_timeline_hypothesis(self, evidence: Dict) -> Dict:
        """Build timeline-focused hypothesis using temporal reasoning"""
        events = []
        
        # Extract temporal information
        for evidence_id, data in evidence.items():
            if 'timestamp' in data:
                events.append({
                    'time': data['timestamp'],
                    'event': f"Evidence {evidence_id}: {data.get('shows_person', 'Unknown')} at {data.get('location', 'Unknown location')}",
                    'evidence_id': evidence_id
                })
        
        # Sort by time
        events.sort(key=lambda x: x['time'])
        
        # Analyze patterns
        timeline_gaps = self.find_timeline_gaps(events)
        concurrent_events = self.find_concurrent_events(events)
        
        return {
            "type": "timeline_analysis",
            "events_sequence": events,
            "timeline_gaps": timeline_gaps,
            "concurrent_events": concurrent_events,
            "hypothesis": "Timeline analysis reveals patterns in evidence sequence",
            "confidence": 0.8 if events else 0.3,
            "evidence_ids": [e['evidence_id'] for e in events]
        }
    
    def find_timeline_gaps(self, events: List) -> List:
        """Find suspicious gaps in timeline"""
        # Implementation for gap detection
        return []
    
    def find_concurrent_events(self, events: List) -> List:
        """Find events happening at similar times"""
        # Implementation for concurrent event detection
        return []

class RelationshipAnalyst:
    """Agent specialized in relationship and network analysis"""
    
    def __init__(self, port: int = 8011):
        self.agent = Agent(
            name="RelationshipAnalyst", 
            seed="relationship-analyst-seed",
            port=port,
            mailbox=True
        )
        fund_agent_if_low(self.agent.wallet.address())
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.agent.on_message(model=HypothesisRequest)
        async def analyze_relationships(ctx: Context, sender: str, msg: HypothesisRequest):
            if msg.focus_area != "relationships":
                return
                
            ctx.logger.info(f"👥 Relationship analysis requested for case {msg.case_id}")
            
            relationship_hypothesis = await self.build_relationship_hypothesis(msg.evidence_summary)
            
            response = HypothesisResponse(
                case_id=msg.case_id,
                focus_area="relationships",
                hypothesis=relationship_hypothesis,
                confidence=relationship_hypothesis.get("confidence", 0.7),
                supporting_evidence=relationship_hypothesis.get("evidence_ids", [])
            )
            
            await ctx.send(sender, response)
    
    async def build_relationship_hypothesis(self, evidence: Dict) -> Dict:
        """Analyze relationships between entities"""
        people = set()
        locations = set()
        connections = []
        
        # Extract entities
        for evidence_id, data in evidence.items():
            if 'shows_person' in data:
                people.add(data['shows_person'])
            if 'location' in data:
                locations.add(data['location'])
            
            # Find connections
            if 'shows_person' in data and 'location' in data:
                connections.append({
                    'person': data['shows_person'],
                    'location': data['location'],
                    'evidence': evidence_id,
                    'relationship': 'present_at'
                })
        
        return {
            "type": "relationship_analysis",
            "people_identified": list(people),
            "locations_identified": list(locations),
            "connections": connections,
            "network_density": len(connections) / max(len(people) * len(locations), 1),
            "hypothesis": f"Network analysis identified {len(people)} people connected through {len(locations)} locations",
            "confidence": 0.8 if connections else 0.3,
            "evidence_ids": [c['evidence'] for c in connections]
        }

class MotiveAnalyst:
    """Agent specialized in motive and behavioral analysis using AI"""
    
    def __init__(self, port: int = 8012):
        self.agent = Agent(
            name="MotiveAnalyst",
            seed="motive-analyst-seed", 
            port=port,
            mailbox=True
        )
        fund_agent_if_low(self.agent.wallet.address())
        self.client = OpenAI(api_key=os.getenv("ASI_API_KEY"), base_url="https://api.asi1.ai/v1")
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.agent.on_message(model=HypothesisRequest)
        async def analyze_motives(ctx: Context, sender: str, msg: HypothesisRequest):
            if msg.focus_area != "motives":
                return
                
            ctx.logger.info(f"🎯 Motive analysis requested for case {msg.case_id}")
            
            motive_hypothesis = await self.build_motive_hypothesis(msg.evidence_summary)
            
            response = HypothesisResponse(
                case_id=msg.case_id,
                focus_area="motives",
                hypothesis=motive_hypothesis,
                confidence=motive_hypothesis.get("confidence", 0.6),
                supporting_evidence=motive_hypothesis.get("evidence_ids", [])
            )
            
            await ctx.send(sender, response)
    
    async def build_motive_hypothesis(self, evidence: Dict) -> Dict:
        """Use AI to analyze potential motives and behavioral patterns"""
        try:
            prompt = f"""
            Analyze the following evidence for potential motives and behavioral patterns:
            
            Evidence: {json.dumps(evidence, indent=2)}
            
            Return JSON analysis with:
            - potential_motives: List of possible motives
            - behavioral_patterns: Observable patterns
            - risk_assessment: Risk level and reasoning
            - confidence: Float 0-1
            - evidence_ids: List of supporting evidence IDs
            """
            
            response = self.client.chat.completions.create(
                model="asi1-mini",
                messages=[
                    {"role": "system", "content": "You are a behavioral analyst AI specializing in motive analysis for investigations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800
            )
            
            analysis = json.loads(response.choices[0].message.content)
            analysis["type"] = "motive_analysis"
            analysis["hypothesis"] = "AI-powered behavioral and motive analysis"
            
            return analysis
            
        except Exception as e:
            return {
                "type": "motive_analysis",
                "hypothesis": f"Motive analysis error: {e}",
                "potential_motives": ["Analysis failed"],
                "confidence": 0.1,
                "evidence_ids": list(evidence.keys()) if evidence else []
            }

class CollaborationCoordinator:
    """Master agent that coordinates specialized analysts and synthesizes results"""
    
    def __init__(self, port: int = 8020):
        self.agent = Agent(
            name="CollaborationCoordinator",
            seed="collaboration-coordinator-seed",
            port=port,
            mailbox=True
        )
        fund_agent_if_low(self.agent.wallet.address())
        
        # Analyst addresses (you'll need to update these with real addresses)
        self.analysts = {
            "timeline": "TIMELINE_ANALYST_ADDRESS",
            "relationships": "RELATIONSHIP_ANALYST_ADDRESS", 
            "motives": "MOTIVE_ANALYST_ADDRESS"
        }
        
        self.pending_analyses = {}
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.agent.on_message(model=EvidenceMetadata)
        async def coordinate_analysis(ctx: Context, sender: str, msg: EvidenceMetadata):
            ctx.logger.info(f"🎯 Coordinating multi-agent analysis for evidence from {sender}")
            
            case_id = f"case_{hash(str(msg.evidence))}"
            self.pending_analyses[case_id] = {
                "responses": {},
                "sender": sender,
                "evidence": msg.evidence
            }
            
            # Request specialized analyses
            for focus_area, analyst_address in self.analysts.items():
                request = HypothesisRequest(
                    case_id=case_id,
                    evidence_summary=msg.evidence,
                    focus_area=focus_area
                )
                
                try:
                    await ctx.send(analyst_address, request)
                    ctx.logger.info(f"📤 Requested {focus_area} analysis")
                except Exception as e:
                    ctx.logger.error(f"❌ Failed to contact {focus_area} analyst: {e}")
        
        @self.agent.on_message(model=HypothesisResponse)
        async def collect_hypothesis(ctx: Context, sender: str, msg: HypothesisResponse):
            ctx.logger.info(f"📊 Received {msg.focus_area} hypothesis for case {msg.case_id}")
            
            if msg.case_id not in self.pending_analyses:
                return
            
            # Store response
            self.pending_analyses[msg.case_id]["responses"][msg.focus_area] = msg.hypothesis
            
            # Check if all analyses complete
            expected_analyses = set(self.analysts.keys())
            received_analyses = set(self.pending_analyses[msg.case_id]["responses"].keys())
            
            if expected_analyses <= received_analyses:
                # All analyses received, synthesize results
                await self.synthesize_and_respond(ctx, msg.case_id)
    
    async def synthesize_and_respond(self, ctx: Context, case_id: str):
        """Synthesize all specialist analyses into final assessment"""
        analysis_data = self.pending_analyses[case_id]
        all_hypotheses = list(analysis_data["responses"].values())
        
        # Calculate consensus rating
        confidences = [h.get("confidence", 0.5) for h in all_hypotheses]
        consensus_rating = sum(confidences) / len(confidences)
        
        # Build final assessment
        final_assessment = {
            "case_summary": f"Multi-agent collaborative analysis of {len(analysis_data['evidence'])} evidence items",
            "specialist_findings": analysis_data["responses"],
            "consensus_confidence": consensus_rating,
            "recommendation": "High confidence" if consensus_rating > 0.7 else "Medium confidence" if consensus_rating > 0.5 else "Low confidence"
        }
        
        # Send collaborative analysis back
        response = CollaborativeAnalysis(
            case_id=case_id,
            all_hypotheses=all_hypotheses,
            consensus_rating=consensus_rating,
            final_assessment=final_assessment
        )
        
        original_sender = analysis_data["sender"]
        await ctx.send(original_sender, response)
        ctx.logger.info(f"🎯 Collaborative analysis complete for case {case_id}")
        
        # Cleanup
        del self.pending_analyses[case_id]

# Multi-agent system runner
class MultiAgentReasoningSystem:
    def __init__(self):
        self.timeline_analyst = TimelineAnalyst(8010)
        self.relationship_analyst = RelationshipAnalyst(8011) 
        self.motive_analyst = MotiveAnalyst(8012)
        self.coordinator = CollaborationCoordinator(8020)
    
    async def run_all_agents(self):
        """Run all agents concurrently"""
        tasks = [
            asyncio.create_task(self.run_agent(self.timeline_analyst.agent)),
            asyncio.create_task(self.run_agent(self.relationship_analyst.agent)),
            asyncio.create_task(self.run_agent(self.motive_analyst.agent)),
            asyncio.create_task(self.run_agent(self.coordinator.agent)),
        ]
        
        await asyncio.gather(*tasks)
    
    async def run_agent(self, agent):
        """Helper to run individual agent"""
        agent.run()

if __name__ == "__main__":
    system = MultiAgentReasoningSystem()
    asyncio.run(system.run_all_agents())
