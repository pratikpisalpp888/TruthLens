"""
TruthLens — LangGraph Agent State Definition.
"""

import time
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages


class TruthLensState(TypedDict):
    case_id: str
    documents: list

    # Agent outputs
    classification_results: dict
    forensic_results: dict
    cross_reference_results: dict
    itr_results: dict
    fraud_dna_results: dict
    compliance_results: dict

    # Final outputs
    risk_scores: dict
    final_decision: dict
    report: str

    # Meta
    agent_logs: list
    errors: list
    current_agent: str
    start_time: float
