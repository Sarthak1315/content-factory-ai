"""
SEO Agent - Optimizes content for search engines
Keyword research, meta descriptions, SEO scoring
"""

from typing import Dict, List
from google import genai
from google.genai import types
import json


class SEOAgent:
    """Agent responsible for SEO optimization"""
    
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model
        
        self.system_instruction = """You are an SEO Specialist and Content Optimizer.

Your responsibilities:
1. Conduct keyword research
2. Optimize title and headers (H1, H2, H3)
3. Create compelling meta description
4. Ensure keyword density (1-2%)
5. Suggest internal linking opportunities
6. Calculate SEO score

SEO Best Practices:
- Title: 50-60 characters, include primary keyword
- Meta description: 150-160 characters, compelling + keyword
- Headers: Use keywords naturally in H2/H3
- Content: Natural keyword integration (avoid stuffing)
- Readability: Clear, scannable structure

Output Format (JSON):
{
  "optimized_content": "Content with SEO improvements",
  "seo_score": 85,
  "keywords": {
    "primary": "main keyword",
    "secondary": ["keyword2", "keyword3"]
  },
  "meta_description": "Compelling meta description",
  "title_suggestion": "SEO-optimized title",
  "improvements": ["List of improvements made"]
}"""
    
    async def optimize(self, content: str, topic: str, session_id: str) -> Dict:
        """
        Optimize content for SEO
        
        Args:
            content: Content to optimize
            topic: Main topic/keyword
            session_id: Session identifier
            
        Returns:
            Dictionary with optimized content and SEO data
        """
        
        prompt = f"""Optimize this content for SEO:

Topic/Primary Keyword: {topic}

Content:
{content}

Tasks:
1. Research related keywords using web search
2. Optimize title, headers, and content
3. Create meta description
4. Calculate SEO score (0-100)
5. Provide list of improvements

Return results in JSON format as specified."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,
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
                
                seo_data = json.loads(result_text)
            except json.JSONDecodeError:
                seo_data = {
                    "optimized_content": content,
                    "seo_score": 75,
                    "keywords": {"primary": topic, "secondary": []},
                    "meta_description": f"Learn about {topic}",
                    "title_suggestion": topic,
                    "improvements": []
                }
            
            return seo_data
            
        except Exception as e:
            raise Exception(f"SEO agent error: {str(e)}")