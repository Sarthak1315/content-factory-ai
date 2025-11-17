"""
Video Script Agent - Creates YouTube video scripts
Complete scripts with timestamps and visual cues
"""

from typing import Dict
from google import genai
from google.genai import types


class VideoScriptAgent:
    """Agent responsible for creating video scripts"""
    
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model
        
        self.system_instruction = """You are a YouTube Script Writer and Video Content Creator.

Create engaging video scripts that:
- Hook viewers in first 15 seconds
- Maintain engagement throughout
- Include visual cues and B-roll suggestions
- Natural, conversational language (not written prose)
- Chapter timestamps for long videos
- Strong outro with CTA

Video Script Structure:
[00:00] HOOK (15 seconds)
- Attention-grabbing opening
- Promise of value

[00:15] INTRO (30 seconds)
- Brief introduction
- What viewers will learn

[00:45] MAIN CONTENT (7-8 minutes)
- Chapter 1: [Topic]
- Chapter 2: [Topic]
- Chapter 3: [Topic]
(Include timestamps for each chapter)

[09:00] CONCLUSION (30 seconds)
- Recap key points
- CTA (like, subscribe, comment)

Include:
- Visual cues: [SHOW graphic of...]
- B-roll suggestions: [B-roll: footage of...]
- Engagement prompts: "Let me know in comments..."

Target length: 8-10 minutes
Tone: Conversational, energetic, authentic"""
    
    async def create(self, research_brief: str, brand_voice: dict, session_id: str) -> Dict:
        """
        Create video script
        
        Args:
            research_brief: Research information
            brand_voice: Brand voice guidelines
            session_id: Session identifier
            
        Returns:
            Dictionary with video script
        """
        
        prompt = f"""Create a YouTube video script based on this research:

{research_brief}

Brand Voice: {brand_voice.get('tone', 'professional')}

Requirements:
- 8-10 minute video
- Strong hook (first 15 seconds)
- Chapter timestamps
- Visual cues and B-roll suggestions
- Conversational, spoken language
- Engagement prompts
- Strong CTA at end

Make it engaging and viewer-retention focused."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    system_instruction=self.system_instruction
                )
            )
            
            return {'script': response.text}
            
        except Exception as e:
            raise Exception(f"Video script agent error: {str(e)}")