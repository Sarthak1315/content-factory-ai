"""
Web Search Tool - Wrapper for Google Search functionality
"""

from typing import Dict, List, Optional
from google.genai import types


class WebSearchTool:
    """Tool for performing web searches"""
    
    @staticmethod
    def create_search_tool() -> types.Tool:
        """Create Google Search tool for agents"""
        return types.Tool(google_search=types.GoogleSearch())
    
    @staticmethod
    def parse_search_results(response) -> List[Dict]:
        """Parse search results from response"""
        results = []
        
        if hasattr(response, 'candidates'):
            for candidate in response.candidates:
                if hasattr(candidate, 'grounding_metadata'):
                    metadata = candidate.grounding_metadata
                    if hasattr(metadata, 'search_entry_point'):
                        results.append({
                            'source': 'web_search',
                            'data': str(metadata)
                        })
        
        return results
    
    @staticmethod
    def format_query(topic: str, context: Optional[str] = None) -> str:
        """Format search query for better results"""
        if context:
            return f"{topic} {context}"
        return topic