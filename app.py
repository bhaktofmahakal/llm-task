from embedding_retrieval import FactRetriever
from llm_fact_checker import FactChecker
from config import TOP_K_FACTS
from typing import Dict, List


class FactCheckingPipeline:
    def __init__(self):
        self.retriever = FactRetriever()
        self.checker = FactChecker()

    def check_statement(self, statement: str) -> Dict:
        try:
            claims = self.checker.extract_key_claims(statement)
            
            if not claims:
                claims = [statement]

            results = []
            
            for claim in claims:
                retrieved_facts, distances, metadatas = self.retriever.retrieve_relevant_facts(
                    claim,
                    top_k=TOP_K_FACTS
                )
                
                verification_result = self.checker.verify_claim(claim, retrieved_facts)
                
                results.append({
                    "claim": claim,
                    "verdict": verification_result.get("verdict", "Unverifiable"),
                    "confidence": verification_result.get("confidence", 0.0),
                    "reasoning": verification_result.get("reasoning", ""),
                    "evidence": verification_result.get("evidence", []),
                    "supporting_facts": verification_result.get("supporting_facts", []),
                    "conflicting_facts": verification_result.get("conflicting_facts", []),
                    "metadata": metadatas
                })

            return {
                "original_statement": statement,
                "total_claims": len(claims),
                "results": results,
                "overall_verdict": self._aggregate_verdict(results)
            }

        except Exception as e:
            print(f"Error in fact-checking pipeline: {e}")
            return {
                "original_statement": statement,
                "error": str(e),
                "total_claims": 0,
                "results": [],
                "overall_verdict": "Error"
            }

    def _aggregate_verdict(self, results: List[Dict]) -> str:
        if not results:
            return "Unverifiable"

        verdicts = [r.get("verdict", "Unverifiable") for r in results]
        
        if any(v == "False" for v in verdicts):
            return "False"
        elif all(v == "True" for v in verdicts):
            return "True"
        else:
            return "Unverifiable"

    def initialize_database(self):
        self.retriever.populate_database()

    def reset_database(self):
        self.retriever.clear_database()
