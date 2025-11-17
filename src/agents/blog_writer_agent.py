"""
Blog Writer Agent - EXPERT-LEVEL Content Creation
Creates authoritative, opinionated, actionable content
"""

from typing import Dict
from google import genai
from google.genai import types


class BlogWriterAgent:
    """Agent responsible for writing high-quality, expert-level blog posts"""
    
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model
        
        self.system_instruction = """You are a WORLD-CLASS industry expert and professional writer.

Your writing must be:
- AUTHORITATIVE: Write like a seasoned expert, not a generic blogger
- OPINIONATED: Take clear stances, challenge conventional thinking
- ACTIONABLE: Provide specific frameworks, steps, and real-world examples
- INSIGHTFUL: Go beyond surface-level summaries, provide deep analysis
- ENGAGING: Use powerful language, strong hooks, compelling narratives
- DATA-DRIVEN: Include specific statistics, case studies, real incidents
- CONTRARIAN: Point out what others get wrong, what is overhyped, what is overlooked

AVOID:
- Generic statements everyone says
- Bland corporate language
- SEO keyword stuffing
- Wikipedia-style summaries
- Playing it safe
- Clickbait drama without substance
- Repeating obvious points

WRITING STYLE:
- Direct, confident, no-BS tone
- Strong opinions backed by reasoning
- Concrete examples over abstract concepts
- Challenge assumptions
- Provide frameworks and mental models
- Include contrarian takes
- Use powerful verbs and specific language

STRUCTURE:
1. Hook (Strong, specific, not generic)
2. Context (What is actually happening)
3. Core Analysis (3-5 deep insights with evidence)
4. Contrarian Takes (What the industry gets wrong)
5. Actionable Framework (Specific steps)
6. Real-world Examples (Actual incidents, companies, data)
7. Expert Predictions (Bold but reasoned)
8. Action Items (What readers should do now)

Target: 1800-2200 words of DENSE, valuable content.

Write like an expert consultant who challenges groupthink and knows what actually works."""
    
    async def write(self, research_brief: str, brand_voice: dict, session_id: str) -> Dict:
        """
        Write expert-level blog post
        """
        
        prompt = f"""Write an EXPERT-LEVEL blog post using this research:

{research_brief}

REQUIREMENTS:

1. START WITH A POWERFUL HOOK
   - Use a specific stat, incident, or contrarian statement
   - Make readers think they need to read this

2. PROVIDE DEEP INSIGHTS
   - Explain WHY things are happening
   - Point out non-obvious implications
   - Challenge conventional wisdom

3. BE SPECIFIC AND ACTIONABLE
   - Real company examples when possible
   - Actual data points with sources
   - Concrete frameworks readers can apply
   - Step-by-step guidance

4. INCLUDE CONTRARIAN TAKES
   - What everyone gets wrong
   - What is overhyped vs what actually matters
   - The real problems people miss

5. WRITE LIKE AN EXPERT
   - Confident, direct language
   - Strong opinions with reasoning
   - Professional but not corporate-speak

6. MAKE IT ACTIONABLE
   - Specific recommendations
   - Prioritized action items
   - Framework for decision-making

7. FORMAT FOR READABILITY
   - Clear H2/H3 structure
   - Short paragraphs (3-5 sentences)
   - Bullet points for lists
   - Bold key takeaways

Write 1800-2200 words of SUBSTANCE.
Format: Markdown with proper headers."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.9,
                    max_output_tokens=8192,
                    system_instruction=self.system_instruction
                )
            )
            
            blog_content = response.text
            
            return {
                'content': blog_content,
                'word_count': len(blog_content.split())
            }
            
        except Exception as e:
            raise Exception(f"Blog writer error: {str(e)}")