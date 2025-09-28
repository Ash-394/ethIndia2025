# asi_chat_integration.py - ASI:One Chat Protocol
import os
import json
from typing import Dict, Any, List
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from openai import OpenAI
import asyncio

# Chat Protocol Models
class ChatMessage(Model):
    user_id: str
    message: str
    context: Dict[str, Any]

class ChatResponse(Model):
    response: str
    evidence_analysis: Dict[str, Any] = None
    investigation_status: str
    confidence: float
    next_actions: List[str] = []

class EvidenceSubmission(Model):
    user_id: str
    evidence_type: str
    evidence_data: Dict[str, Any]
    description: str

# ASI:One Chat Agent
class ASIChatAgent:
    """Human-facing chat agent that interfaces with ASI:One and coordinates investigation agents"""
    
    def __init__(self):
        self.agent = Agent(
            name="ASI_Chat_Detective",
            seed="asi-chat-detective-seed",
            port=8100,
            mailbox=True
        )
        
        fund_agent_if_low(self.agent.wallet.address())
        
        self.client = OpenAI(
            api_key=os.getenv("ASI_API_KEY"),
            base_url="https://api.asi1.ai/v1"
        )
        
        # Active conversations and case tracking
        self.active_cases = {}
        self.user_sessions = {}
        
        # Agent network addresses (update with real addresses)
        self.detective_agents = {
            "enhanced_detective": "ENHANCED_DETECTIVE_ADDRESS",
            "collaboration_coordinator": "COLLABORATION_COORDINATOR_ADDRESS",
            "evidence_collector": "EVIDENCE_COLLECTOR_ADDRESS"
        }
        
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.agent.on_event("startup")
        async def startup(ctx: Context):
            ctx.logger.info("💬 ASI:One Chat Detective Agent READY")
            ctx.logger.info(f"🌐 Available for human-agent interaction")
            ctx.logger.info(f"📍 Address: {ctx.agent.address}")
        
        @self.agent.on_message(model=ChatMessage)
        async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
            """Handle conversational input from humans via ASI:One"""
            ctx.logger.info(f"💬 Chat message from user {msg.user_id}")
            
            # Initialize user session if new
            if msg.user_id not in self.user_sessions:
                self.user_sessions[msg.user_id] = {
                    "cases": [],
                    "conversation_history": [],
                    "preferences": {}
                }
            
            # Add to conversation history
            self.user_sessions[msg.user_id]["conversation_history"].append({
                "role": "user",
                "content": msg.message,
                "context": msg.context
            })
            
            # Process the message
            response = await self.process_chat_message(msg)
            
            # Add response to history
            self.user_sessions[msg.user_id]["conversation_history"].append({
                "role": "assistant", 
                "content": response.response
            })
            
            await ctx.send(sender, response)
            ctx.logger.info(f"📤 Response sent to user {msg.user_id}")
        
        @self.agent.on_message(model=EvidenceSubmission)
        async def handle_evidence_submission(ctx: Context, sender: str, msg: EvidenceSubmission):
            """Handle evidence submitted through chat interface"""
            ctx.logger.info(f"📄 Evidence submitted by user {msg.user_id}")
            
            # Create or update case
            case_id = await self.create_or_update_case(msg.user_id, msg)
            
            # Forward evidence to investigation network
            await self.forward_to_investigators(ctx, case_id, msg.evidence_data)
            
            # Send acknowledgment
            response = ChatResponse(
                response=f"Evidence received and case {case_id} initiated. Investigation agents are analyzing...",
                investigation_status="processing",
                confidence=1.0,
                next_actions=["Wait for analysis", "Submit additional evidence", "Ask for status update"]
            )
            
            await ctx.send(sender, response)
    
    async def process_chat_message(self, msg: ChatMessage) -> ChatResponse:
        """Process conversational message using ASI:One intelligence"""
        
        # Determine intent using ASI:One
        intent = await self.classify_intent(msg.message, msg.context)
        
        if intent == "evidence_submission":
            return await self.handle_evidence_discussion(msg)
        elif intent == "case_inquiry":
            return await self.handle_case_inquiry(msg)
        elif intent == "investigation_status":
            return await self.handle_status_request(msg)
        elif intent == "general_question":
            return await self.handle_general_question(msg)
        else:
            return await self.handle_unknown_intent(msg)
    
    async def classify_intent(self, message: str, context: Dict) -> str:
        """Use ASI:One to classify user intent"""
        try:
            response = self.client.chat.completions.create(
                model="asi1-mini",
                messages=[
