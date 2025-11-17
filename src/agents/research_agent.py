"""
Research Agent - Deep, Expert-Level Research
"""

from typing import Dict
from google import genai
from google.genai import types
import json


class ResearchAgent:
    """Agent responsible for deep, expert-level research"""
    
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model
        
        self.system_instruction = """You are an EXPERT RESEARCHER and industry analyst.

Your research must be:
- DEEP: Go beyond surface-level facts
- CURRENT: Focus on latest developments, data, incidents
- SPECIFIC: Find exact statistics, case studies, real examples
- CRITICAL: Identify what is overhyped vs what matters
- ACTIONABLE: Gather insights that lead to practical advice

Research focus:
1. Recent incidents and real-world examples
2. Specific statistics with sources
3. Expert opinions and analysis
4. Contrarian perspectives
5. What is changing and why
6. What most people get wrong
7. Actionable data and frameworks

Prioritize SPECIFIC, ACTIONABLE information over generic facts."""
    
    async def research(self, topic: str, session_id: str) -> Dict:
        """Conduct deep research"""
        
        prompt = f"""Conduct EXPERT-LEVEL research on: {topic}

Search for:
1. Recent incidents, breaches, case studies (last 6-12 months)
2. Specific statistics with sources
3. Expert analysis from credible sources
4. Contrarian perspectives
5. Real company examples
6. Actionable frameworks
7. What is actually changing

Focus on concrete data, recent events, and practitioner insights.

Provide structured research in JSON format:
{{
  "brief": "Comprehensive research with specific details",
  "key_insights": ["Insight with data"],
  "statistics": ["Stat with source"],
  "real_examples": ["Example with details"],
  "sources": [{{"title": "...", "url": "...", "relevance": "..."}}]
}}"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    system_instruction=self.system_instruction,
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )
            
            result_text = response.text
            
            try:
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0].strip()
                
                research_data = json.loads(result_text)
            except json.JSONDecodeError:
                research_data = {
                    "brief": result_text,
                    "key_insights": [],
                    "statistics": [],
                    "real_examples": [],
                    "sources": []
                }
            
            return research_data
            
        except Exception as e:
            raise Exception(f"Research agent error: {str(e)}")