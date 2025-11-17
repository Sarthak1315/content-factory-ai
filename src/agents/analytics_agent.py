"""
Analytics Agent - Learns from content performance (SECRET WEAPON #3)
Tracks patterns and improves future content based on data
"""

from typing import Dict, List
from google import genai
from google.genai import types
import json


class AnalyticsAgent:
    """Agent responsible for analytics and learning"""
    
    def __init__(self, client: genai.Client, model: str, memory_bank):
        self.client = client
        self.model = model
        self.memory_bank = memory_bank
        
        self.system_instruction = """You are a Data Analyst and Content Performance Specialist.

Your responsibilities:
1. Analyze content performance patterns
2. Identify what works best (topics, formats, styles)
3. Learn from successful content
4. Provide actionable insights for improvement
5. Track trends over time

Analysis Areas:
- Topic performance (which topics get most engagement)
- Content length optimization
- Headline effectiveness
- Best posting times
- Format preferences (lists, how-tos, etc.)

Output Format (JSON):
{
  "patterns": [
    {
      "pattern": "Description of pattern found",
      "confidence": 85,
      "recommendation": "What to do based on this"
    }
  ],
  "best_topics": ["topic1", "topic2"],
  "optimal_length": "1500-1800 words",
  "best_headlines": ["format1", "format2"],
  "insights": "Overall insights and recommendations"
}"""
    
    async def analyze_and_learn(self, session_id: str) -> Dict:
        """
        Analyze content history and learn patterns
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary with learned patterns and insights
        """
        
        content_history = self.memory_bank.get('content_history', [])
        
        if len(content_history) < 5:
            return {
                "patterns": [],
                "insights": "Not enough data yet (minimum 5 content pieces needed)",
                "data_points": len(content_history)
            }
        
        history_summary = []
        for item in content_history[-20:]:
            history_summary.append({
                'topic': item.get('topic', ''),
                'metrics': item.get('metrics', {}),
                'timestamp': item.get('timestamp', '')
            })
        
        prompt = f"""Analyze this content performance data and identify patterns:

Content History:
{json.dumps(history_summary, indent=2)}

Tasks:
1. Identify patterns in successful content
2. Determine optimal content characteristics
3. Find trends over time
4. Provide actionable recommendations

Return analysis in JSON format."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    system_instruction=self.system_instruction
                )
            )
            
            result_text = response.text
            
            try:
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0].strip()
                
                analysis_data = json.loads(result_text)
            except json.JSONDecodeError:
                analysis_data = {
                    "patterns": [],
                    "insights": result_text,
                    "data_points": len(content_history)
                }
            
            self.memory_bank.set('learned_patterns', analysis_data)
            
            return analysis_data
            
        except Exception as e:
            raise Exception(f"Analytics agent error: {str(e)}")