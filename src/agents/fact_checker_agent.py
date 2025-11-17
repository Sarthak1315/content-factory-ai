"""
Fact-Checker Agent - Verifies claims in content (SECRET WEAPON #1)
Uses web search to verify factual claims and assign confidence scores
"""

from typing import Dict, List
from google import genai
from google.genai import types
import json


class FactCheckerAgent:
    """Agent responsible for fact-checking content claims"""
    
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model
        
        self.system_instruction = """You are a professional Fact-Checker and Research Analyst.

Your responsibilities:
1. Extract all factual claims from content
2. Verify each claim using web search
3. Assign confidence scores (0-100%)
4. Provide source citations for verified claims
5. Flag unverified or questionable claims

Confidence Score Guidelines:
- 90-100%: Multiple credible sources confirm
- 70-89%: Single credible source confirms
- 50-69%: Partially confirmed or outdated
- Below 50%: Cannot verify or contradicting sources

Output Format (JSON):
{
  "report": "Summary of fact-checking results",
  "confidence": 85,
  "total_claims": 12,
  "verified_claims": 10,
  "flagged_claims": 2,
  "claims": [
    {
      "claim": "The claim text",
      "verification": "verified/unverified/partial",
      "confidence": 95,
      "sources": ["URL1", "URL2"],
      "notes": "Additional context"
    }
  ]
}

Be thorough and conservative with confidence scores."""
    
    async def verify(self, content: str, session_id: str) -> Dict:
        """
        Verify factual claims in content
        
        Args:
            content: Content to fact-check
            session_id: Session identifier
            
        Returns:
            Dictionary with verification report and scores
        """
        
        prompt = f"""Fact-check the following content:

{content}

Tasks:
1. Extract all factual claims (statistics, dates, names, events, etc.)
2. Verify each claim using web search
3. Assign confidence scores
4. Provide sources for verified claims
5. Flag any unverified or questionable claims

Provide detailed verification report in JSON format."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,  # Lower temperature for accuracy
                    system_instruction=self.system_instruction,
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )
            
            result_text = response.text
            
            # Parse JSON response
            try:
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0].strip()
                
                verification_data = json.loads(result_text)
            except json.JSONDecodeError:
                # Fallback structure
                verification_data = {
                    "report": result_text,
                    "confidence": 75,
                    "total_claims": 0,
                    "verified_claims": 0,
                    "flagged_claims": 0,
                    "claims": []
                }
            
            return verification_data
            
        except Exception as e:
            raise Exception(f"Fact-checker error: {str(e)}")