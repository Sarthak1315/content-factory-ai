"""
Editor Agent - Improves content quality
Grammar, readability, brand voice consistency
"""

from typing import Dict
from google import genai
from google.genai import types
import textstat


class EditorAgent:
    """Agent responsible for editing and improving content"""
    
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model
        
        self.system_instruction = """You are a professional Content Editor and Copy Editor.

Your responsibilities:
1. Fix grammar, spelling, and punctuation errors
2. Improve readability and flow
3. Ensure brand voice consistency
4. Enhance clarity and conciseness
5. Maintain the original message and key points

Editing Guidelines:
- Target readability: Grade 8-10 (Flesch-Kincaid)
- Use active voice
- Short, clear sentences
- Smooth transitions
- Remove redundancy
- Keep paragraphs focused (3-4 sentences)

Output: The edited content (maintain original format/structure)

Only make necessary improvements. Don't rewrite entirely."""
    
    async def edit(self, content: str, brand_voice: dict, session_id: str) -> Dict:
        """
        Edit and improve content
        
        Args:
            content: Content to edit
            brand_voice: Brand voice guidelines
            session_id: Session identifier
            
        Returns:
            Dictionary with edited content and scores
        """
        
        voice_str = f"Tone: {brand_voice.get('tone', 'professional')}, Style: {brand_voice.get('style', 'clear')}"
        
        prompt = f"""Edit and improve the following content:

{content}

Brand Voice: {voice_str}

Tasks:
1. Fix all grammar and spelling errors
2. Improve readability (target: Grade 8-10)
3. Ensure brand voice consistency
4. Enhance clarity and flow
5. Keep the core message intact

Provide the edited version."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,
                    system_instruction=self.system_instruction
                )
            )
            
            edited_content = response.text
            
            # Calculate readability score
            try:
                readability_score = textstat.flesch_reading_ease(edited_content)
                readability_score = min(100, max(0, readability_score))
            except:
                readability_score = 85
            
            return {
                'content': edited_content,
                'readability_score': readability_score,
                'word_count': len(edited_content.split())
            }
            
        except Exception as e:
            raise Exception(f"Editor error: {str(e)}")