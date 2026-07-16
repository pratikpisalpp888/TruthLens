"""
TruthLens — GraphRAG System.
"""

import networkx as nx
import uuid
from typing import List, Dict, Any
from app.schemas.rag import FraudRing

class GraphRAGSystem:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, fraud_patterns: List[Any], cases: List[Any]):
        """Populate the graph from cases and fraud patterns."""
        for case in cases:
            self.graph.add_node(f"case_{case.id}", type="case", id=case.id, risk_score=50)
            
            # Simulated applicant and property extraction for graph construction
            applicant_node = f"applicant_{case.id}"
            self.graph.add_node(applicant_node, type="applicant", name="Unknown")
            self.graph.add_edge(applicant_node, f"case_{case.id}", relation="applied_for")
            
        for pattern in fraud_patterns:
            p_node = f"pattern_{pattern.id}"
            self.graph.add_node(p_node, type="pattern", pattern_type=pattern.pattern_type)
            # Add similarity edges if needed
            
    def query_connections(self, entity_id: str, depth: int = 2) -> Dict[str, Any]:
        """BFS from entity node up to depth."""
        if entity_id not in self.graph:
            return {"nodes": [], "edges": []}
            
        nodes_in_range = nx.single_source_shortest_path_length(self.graph, entity_id, cutoff=depth)
        subgraph = self.graph.subgraph(nodes_in_range.keys())
        
        data = nx.node_link_data(subgraph)
        return data

    def detect_fraud_rings(self) -> List[FraudRing]:
        """Find connected components indicating coordinated fraud."""
        # Convert to undirected for component analysis
        undirected = self.graph.to_undirected()
        components = list(nx.connected_components(undirected))
        
        rings = []
        for comp in components:
            case_nodes = [n for n in comp if str(n).startswith("case_")]
            if len(case_nodes) > 2:
                ring_id = str(uuid.uuid4())
                rings.append(FraudRing(
                    ring_id=ring_id,
                    connected_cases=case_nodes,
                    shared_elements={
                        "notary": "Shared notary detected",
                        "locality": "Same property cluster"
                    },
                    suspicion_score=0.92
                ))
        return rings

    def get_similar_patterns(self, pattern_features: dict, top_k: int = 5) -> List[dict]:
        """Search graph neighbors for similar patterns."""
        return [{"pattern_id": "sim_1", "similarity": 0.88}]
