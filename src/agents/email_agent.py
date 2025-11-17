"""
Email Agent - Creates email newsletters
Conversion-focused email content
"""

from typing import Dict
from google import genai
from google.genai import types


class EmailAgent:
    """Agent responsible for creating email newsletters"""
    
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model
        
        self.system_instruction = """You are an Email Marketing Specialist.

Create effective email newsletters that:
- Compelling subject lines (5 variations)
- Engaging preview text
- Clear, scannable body (300-500 words)
- Strong call-to-action
- Personal, conversational tone
- Value-focused (not salesy)

Email Structure:
1. Subject Line Options (5 variations)
2. Preview Text
3. Email Body:
   - Hook/opener
   - Main value proposition
   - Key points or insights
   - CTA (clear next step)
   - P.S. section (optional but effective)

Best Practices:
- Keep paragraphs short
- Use "you" language
- Create urgency without pressure
- One clear CTA
- Mobile-friendly formatting"""
    
    async def create(self, research_brief: str, brand_voice: dict, session_id: str) -> Dict:
        """
        Create email newsletter
        
        Args:
            research_brief: Research information
            brand_voice: Brand voice guidelines
            session_id: Session identifier
            
        Returns:
            Dictionary with email content
        """
        
        prompt = f"""Create an email newsletter based on this research:

{research_brief}

Brand Voice: {brand_voice.get('tone', 'professional')}

Include:
- 5 subject line options
- Preview text
- Complete email body (300-500 words)
- Clear CTA
- P.S. section

Make it conversion-focused and engaging."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    system_instruction=self.system_instruction
                )
            )
            
            return {'email': response.text}
            
        except Exception as e:
            raise Exception(f"Email agent error: {str(e)}")