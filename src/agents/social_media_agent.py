"""
Social Media Agents - Create platform-specific content
LinkedIn, Twitter, Instagram agents for multi-platform content
"""

from typing import Dict
from google import genai
from google.genai import types


class LinkedInAgent:
    """Creates LinkedIn posts"""
    
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model
        
        self.system_instruction = """You are a LinkedIn Content Specialist.

Create professional LinkedIn posts that:
- Start with a strong hook (first line matters!)
- Provide value and insights
- Are conversational yet professional
- Include 5-7 relevant hashtags
- Have clear call-to-action
- Length: 150-200 words per post

Format:
POST 1:
[Hook line]

[Main content with line breaks for readability]

[CTA]

#Hashtag1 #Hashtag2 #Hashtag3

---

Create 3-5 variations on the same topic."""
    
    async def create(self, research_brief: str, brand_voice: dict, session_id: str) -> Dict:
        """Create LinkedIn posts"""
        
        prompt = f"""Create 3-5 LinkedIn posts based on this research:

{research_brief}

Brand Voice: {brand_voice.get('tone', 'professional')}

Make each post unique with different angles or hooks."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.9,
                    system_instruction=self.system_instruction
                )
            )
            
            return {'posts': response.text}
            
        except Exception as e:
            raise Exception(f"LinkedIn agent error: {str(e)}")


class TwitterAgent:
    """Creates Twitter threads"""
    
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model
        
        self.system_instruction = """You are a Twitter Thread Creator and viral content specialist.

Create engaging Twitter threads that:
- Start with an attention-grabbing hook
- Each tweet: 240-280 characters (leave room for retweets)
- Use line breaks for readability
- Include relevant emojis (strategic, not excessive)
- Thread structure: Hook → Value → Insights → CTA
- 5-10 tweets per thread

Format:
THREAD 1:
Tweet 1/10: [Hook with emoji]

Tweet 2/10: [Insight or context]

Tweet 3/10: [Key point]
...

Create 5-8 threads with different hooks/angles."""
    
    async def create(self, research_brief: str, brand_voice: dict, session_id: str) -> Dict:
        """Create Twitter threads"""
        
        prompt = f"""Create 5-8 Twitter threads based on this research:

{research_brief}

Brand Voice: {brand_voice.get('tone', 'professional')}

Make each thread viral-worthy with strong hooks."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.9,
                    system_instruction=self.system_instruction
                )
            )
            
            return {'threads': response.text}
            
        except Exception as e:
            raise Exception(f"Twitter agent error: {str(e)}")


class InstagramAgent:
    """Creates Instagram captions"""
    
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model
        
        self.system_instruction = """You are an Instagram Content Creator.

Create engaging Instagram captions that:
- Start with attention-grabbing first line
- Visual-first approach (suggest image/graphic)
- Casual, relatable tone
- Use emojis naturally
- Include 20-30 relevant hashtags
- Length: 200-300 words
- Include CTA for engagement

Format each post clearly with image suggestion."""
    
    async def create(self, research_brief: str, brand_voice: dict, session_id: str) -> Dict:
        """Create Instagram captions"""
        
        prompt = f"""Create 3-5 Instagram posts based on this research:

{research_brief}

Include image/graphic suggestions for each post."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.9,
                    system_instruction=self.system_instruction
                )
            )
            
            return {'captions': response.text}
            
        except Exception as e:
            raise Exception(f"Instagram agent error: {str(e)}")


class SocialMediaAgentFactory:
    """Factory to create social media agents"""
    
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model
    
    def create_linkedin_agent(self) -> LinkedInAgent:
        return LinkedInAgent(self.client, self.model)
    
    def create_twitter_agent(self) -> TwitterAgent:
        return TwitterAgent(self.client, self.model)
    
    def create_instagram_agent(self) -> InstagramAgent:
        return InstagramAgent(self.client, self.model)