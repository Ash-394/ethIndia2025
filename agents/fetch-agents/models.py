# models.py - Shared model definitions
from typing import Dict, List
from uagents import Model

class EvidenceMetadata(Model):
    evidence: Dict[str, dict]

class InvestigationReport(Model):
    case_id: str
    hypotheses: List[Dict]
