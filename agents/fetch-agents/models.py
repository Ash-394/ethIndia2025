# models.py
from typing import Dict, List, Optional, Any
from uagents import Model

class InformantTip(Model):
    case_id: str
    text: str
    reply_to: Optional[str] = None

class CaseFileUpdate(Model):
    case_id: str
    full_evidence_log: List[Dict[str, Any]]
    reply_to: Optional[str] = None

class InvestigationReport(Model):
    case_id: str
    case_summary: str
    key_entities: Dict[str, List[str]]
    evidence_log: List[Dict[str, Any]]
    ai_synthesis: str
