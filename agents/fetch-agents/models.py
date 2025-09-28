# models.py
from typing import Dict, List, Optional, Any
from uagents import Model

class InformantTip(Model):
    case_id: str
    text: str
    reply_to: Optional[str] = None

class MeTTaScriptUpdate(Model):
    case_id: str
    cumulative_script: str
    reply_to: Optional[str] = None

class InvestigationReport(Model):
    case_id: str
    insights: List[str]
