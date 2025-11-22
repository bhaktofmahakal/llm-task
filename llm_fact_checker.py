import json
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, CONFIDENCE_THRESHOLD


class FactChecker:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = LLM_MODEL

    def build_verification_prompt(self, claim: str, retrieved_facts: list) -> str:
        facts_text = "\n".join([f"- {fact}" for fact in retrieved_facts])
        
        prompt = f"""You are an expert fact-checker. Your task is to verify if the following claim is true, false, or unverifiable based on the provided facts.

CLAIM TO VERIFY:
"{claim}"

RETRIEVED FACTS FOR REFERENCE:
{facts_text}

Based on the retrieved facts, determine:
1. Whether the claim is TRUE (supported by facts), FALSE (contradicted by facts), or UNVERIFIABLE (insufficient information)
2. Provide clear reasoning
3. Cite which facts support or contradict the claim

Respond in the following JSON format:
{{
  "verdict": "True" or "False" or "Unverifiable",
  "confidence": <0.0 to 1.0>,
  "reasoning": "Your detailed reasoning",
  "supporting_facts": ["fact 1", "fact 2"],
  "conflicting_facts": ["fact 1", "fact 2"]
}}

Only respond with valid JSON, no additional text."""
        
        return prompt

    def verify_claim(self, claim: str, retrieved_facts: list) -> dict:
        if not retrieved_facts:
            return {
                "verdict": "Unverifiable",
                "confidence": 0.0,
                "reasoning": "No relevant facts found in the database to verify this claim.",
                "evidence": [],
                "supporting_facts": [],
                "conflicting_facts": []
            }

        prompt = self.build_verification_prompt(claim, retrieved_facts)
        
        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            response_text = message.choices[0].message.content.strip()
            
            result = json.loads(response_text)
            
            result["evidence"] = retrieved_facts
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return {
                "verdict": "Unverifiable",
                "confidence": 0.0,
                "reasoning": f"Error processing LLM response: {str(e)}",
                "evidence": retrieved_facts,
                "supporting_facts": [],
                "conflicting_facts": []
            }
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return {
                "verdict": "Unverifiable",
                "confidence": 0.0,
                "reasoning": f"Error verifying claim: {str(e)}",
                "evidence": retrieved_facts,
                "supporting_facts": [],
                "conflicting_facts": []
            }

    def extract_key_claims(self, text: str) -> list:
        prompt = f"""Extract the main claims or assertions from the following text. 
Return as a JSON array of strings, each representing one key claim.
Only return the JSON array, no additional text.

Text: "{text}"

Example output:
["claim 1", "claim 2", "claim 3"]"""
        
        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            response_text = message.choices[0].message.content.strip()
            claims = json.loads(response_text)
            
            if isinstance(claims, list):
                return claims
            else:
                return [text]
                
        except Exception as e:
            print(f"Error extracting claims: {e}")
            return [text]
