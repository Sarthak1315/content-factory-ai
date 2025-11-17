"""
Test cases for agent functionality
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from google import genai

from src.agents.research_agent import ResearchAgent
from src.agents.blog_writer_agent import BlogWriterAgent
from src.agents.fact_checker_agent import FactCheckerAgent
from src.agents.editor_agent import EditorAgent
from src.agents.seo_agent import SEOAgent


@pytest.fixture
def mock_client():
    """Mock Gemini client"""
    client = Mock(spec=genai.Client)
    return client


@pytest.fixture
def mock_response():
    """Mock API response"""
    response = Mock()
    response.text = "Test response content"
    return response


class TestResearchAgent:
    """Test ResearchAgent functionality"""
    
    @pytest.mark.asyncio
    async def test_research_returns_data(self, mock_client, mock_response):
        """Test research agent returns structured data"""
        mock_client.models.generate_content = AsyncMock(return_value=mock_response)
        mock_response.text = '{"brief": "Test brief", "sources": []}'
        
        agent = ResearchAgent(mock_client, "gemini-2.0-flash-exp")
        result = await agent.research("AI trends", "session_001")
        
        assert 'brief' in result
        assert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_research_handles_errors(self, mock_client):
        """Test research agent error handling"""
        mock_client.models.generate_content = AsyncMock(side_effect=Exception("API Error"))
        
        agent = ResearchAgent(mock_client, "gemini-2.0-flash-exp")
        
        with pytest.raises(Exception):
            await agent.research("AI trends", "session_001")


class TestBlogWriterAgent:
    """Test BlogWriterAgent functionality"""
    
    @pytest.mark.asyncio
    async def test_blog_writer_creates_content(self, mock_client, mock_response):
        """Test blog writer creates content"""
        mock_client.models.generate_content = AsyncMock(return_value=mock_response)
        mock_response.text = "# Test Blog Post\n\nThis is content."
        
        agent = BlogWriterAgent(mock_client, "gemini-1.5-pro")
        result = await agent.write("Research brief", {"tone": "professional"}, "session_001")
        
        assert 'content' in result
        assert 'word_count' in result
        assert isinstance(result['word_count'], int)
    
    @pytest.mark.asyncio
    async def test_blog_writer_word_count(self, mock_client, mock_response):
        """Test blog writer calculates word count correctly"""
        mock_client.models.generate_content = AsyncMock(return_value=mock_response)
        mock_response.text = "word " * 100
        
        agent = BlogWriterAgent(mock_client, "gemini-1.5-pro")
        result = await agent.write("Brief", {"tone": "professional"}, "session_001")
        
        assert result['word_count'] == 100


class TestFactCheckerAgent:
    """Test FactCheckerAgent functionality"""
    
    @pytest.mark.asyncio
    async def test_fact_checker_returns_verification(self, mock_client, mock_response):
        """Test fact checker returns verification data"""
        mock_client.models.generate_content = AsyncMock(return_value=mock_response)
        mock_response.text = '{"report": "Verified", "confidence": 95, "total_claims": 5}'
        
        agent = FactCheckerAgent(mock_client, "gemini-2.0-flash-exp")
        result = await agent.verify("Content to verify", "session_001")
        
        assert 'report' in result
        assert 'confidence' in result
    
    @pytest.mark.asyncio
    async def test_fact_checker_handles_invalid_json(self, mock_client, mock_response):
        """Test fact checker handles invalid JSON response"""
        mock_client.models.generate_content = AsyncMock(return_value=mock_response)
        mock_response.text = "Not valid JSON"
        
        agent = FactCheckerAgent(mock_client, "gemini-2.0-flash-exp")
        result = await agent.verify("Content", "session_001")
        
        assert 'report' in result
        assert result['confidence'] >= 0


class TestEditorAgent:
    """Test EditorAgent functionality"""
    
    @pytest.mark.asyncio
    async def test_editor_improves_content(self, mock_client, mock_response):
        """Test editor agent improves content"""
        mock_client.models.generate_content = AsyncMock(return_value=mock_response)
        mock_response.text = "Edited content here"
        
        agent = EditorAgent(mock_client, "gemini-2.0-flash-exp")
        result = await agent.edit("Original content", {"tone": "friendly"}, "session_001")
        
        assert 'content' in result
        assert 'readability_score' in result
    
    @pytest.mark.asyncio
    async def test_editor_calculates_readability(self, mock_client, mock_response):
        """Test editor calculates readability score"""
        mock_client.models.generate_content = AsyncMock(return_value=mock_response)
        mock_response.text = "Simple content. Easy to read. Very clear."
        
        agent = EditorAgent(mock_client, "gemini-2.0-flash-exp")
        result = await agent.edit("Content", {"tone": "friendly"}, "session_001")
        
        assert 0 <= result['readability_score'] <= 100


class TestSEOAgent:
    """Test SEOAgent functionality"""
    
    @pytest.mark.asyncio
    async def test_seo_agent_optimizes_content(self, mock_client, mock_response):
        """Test SEO agent optimizes content"""
        mock_client.models.generate_content = AsyncMock(return_value=mock_response)
        mock_response.text = '{"optimized_content": "SEO content", "seo_score": 85, "keywords": {}}'
        
        agent = SEOAgent(mock_client, "gemini-2.0-flash-exp")
        result = await agent.optimize("Content", "AI trends", "session_001")
        
        assert 'optimized_content' in result
        assert 'seo_score' in result
    
    @pytest.mark.asyncio
    async def test_seo_agent_handles_json_parsing(self, mock_client, mock_response):
        """Test SEO agent handles JSON parsing errors"""
        mock_client.models.generate_content = AsyncMock(return_value=mock_response)
        mock_response.text = "Invalid JSON response"
        
        agent = SEOAgent(mock_client, "gemini-2.0-flash-exp")
        result = await agent.optimize("Content", "keyword", "session_001")
        
        assert 'seo_score' in result
        assert result['seo_score'] > 0


@pytest.mark.asyncio
async def test_agent_workflow_integration(mock_client, mock_response):
    """Test agents work together in workflow"""
    mock_client.models.generate_content = AsyncMock(return_value=mock_response)
    
    research_agent = ResearchAgent(mock_client, "gemini-2.0-flash-exp")
    blog_writer = BlogWriterAgent(mock_client, "gemini-1.5-pro")
    
    mock_response.text = '{"brief": "Research data", "sources": []}'
    research = await research_agent.research("Topic", "session_001")
    
    mock_response.text = "# Blog Post\n\nContent here."
    blog = await blog_writer.write(research['brief'], {"tone": "professional"}, "session_001")
    
    assert blog['content']
    assert blog['word_count'] > 0