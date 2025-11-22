import json
from app import FactCheckingPipeline


def print_result(result):
    print("\n" + "="*80)
    print("FACT-CHECK RESULT")
    print("="*80)
    print(f"\nOriginal Statement: {result['original_statement']}")
    print(f"Total Claims: {result['total_claims']}")
    print(f"Overall Verdict: {result['overall_verdict']}")
    
    for i, claim_result in enumerate(result['results'], 1):
        print(f"\n{'-'*80}")
        print(f"Claim {i}: {claim_result['claim']}")
        print(f"  Verdict: {claim_result['verdict']}")
        print(f"  Confidence: {claim_result['confidence']:.1%}")
        print(f"  Reasoning: {claim_result['reasoning']}")
        
        evidence = claim_result.get('evidence', [])
        if evidence:
            print(f"\n  Evidence Retrieved:")
            for j, fact in enumerate(evidence, 1):
                print(f"    {j}. {fact[:100]}...")
    
    print("\n" + "="*80)


def main():
    print("[SEARCH] LLM-Powered Fact Checker - Sample Usage")
    print("="*80)
    
    pipeline = FactCheckingPipeline()
    
    print("\n[INIT] Initializing database...")
    pipeline.initialize_database()
    print("[OK] Database initialized")
    
    test_statements = [
        "The Indian government has announced free electricity to all farmers starting July 2025.",
        "PM-KISAN provides Rs. 6000 per year to all landholding farmers.",
        "MNREGA guarantees 365 days of employment per year.",
        "The Ayushman Bharat scheme provides health insurance up to Rs. 5 lakhs per family per year.",
    ]
    
    for statement in test_statements:
        print(f"\n[SEARCH] Checking: {statement}")
        result = pipeline.check_statement(statement)
        print_result(result)
        
        save_filename = f"result_{test_statements.index(statement)}.json"
        with open(save_filename, "w") as f:
            json.dump(result, f, indent=2)
        print(f"[OK] Result saved to {save_filename}")


if __name__ == "__main__":
    main()
