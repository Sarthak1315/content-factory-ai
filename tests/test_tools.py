"""
Test cases for tool functionality
"""

import pytest
from src.tools.readability_scorer import ReadabilityScorer
from src.tools.brand_voice_matcher import BrandVoiceMatcher
from src.tools.seo_analyzer import SEOAnalyzer
from src.tools.web_search import WebSearchTool


class TestReadabilityScorer:
    """Test ReadabilityScorer functionality"""
    
    def test_calculate_scores(self):
        """Test readability score calculation"""
        text = "This is a simple sentence. It is easy to read. Very clear and concise."
        scores = ReadabilityScorer.calculate_scores(text)
        
        assert 'flesch_reading_ease' in scores
        assert 'overall_score' in scores
        assert isinstance(scores['overall_score'], float)
    
    def test_get_reading_level(self):
        """Test reading level description"""
        level_easy = ReadabilityScorer.get_reading_level(85)
        level_hard = ReadabilityScorer.get_reading_level(30)
        
        assert "Easy" in level_easy
        assert "Difficult" in level_hard
    
    def test_calculate_statistics(self):
        """Test text statistics calculation"""
        text = "Short sentence. Another one. Third sentence here."
        stats = ReadabilityScorer.calculate_statistics(text)
        
        assert 'word_count' in stats
        assert 'sentence_count' in stats
        assert stats['sentence_count'] == 3
    
    def test_handles_empty_text(self):
        """Test handles empty text gracefully"""
        scores = ReadabilityScorer.calculate_scores("")
        
        assert 'overall_score' in scores
        assert scores['overall_score'] >= 0


class TestBrandVoiceMatcher:
    """Test BrandVoiceMatcher functionality"""
    
    def test_analyze_tone_professional(self):
        """Test professional tone analysis"""
        text = "Therefore, we must consider the implications. Furthermore, research shows positive results."
        result = BrandVoiceMatcher.analyze_tone(text, "professional")
        
        assert 'match_score' in result
        assert result['match_score'] > 0
    
    def test_analyze_tone_casual(self):
        """Test casual tone analysis"""
        text = "Hey there! This is awesome stuff. Basically, it's really cool."
        result = BrandVoiceMatcher.analyze_tone(text, "casual")
        
        assert result['matches_found'] > 0
    
    def test_check_avoided_words(self):
        """Test avoided words detection"""
        text = "We need to leverage synergy for paradigm shift."
        avoid_list = ["leverage", "synergy", "paradigm"]
        
        result = BrandVoiceMatcher.check_avoided_words(text, avoid_list)
        
        assert result['avoided_words_used'] == 3
        assert not result['clean']
    
    def test_check_avoided_words_clean(self):
        """Test clean text with no avoided words"""
        text = "We need to use collaboration for improvement."
        avoid_list = ["leverage", "synergy"]
        
        result = BrandVoiceMatcher.check_avoided_words(text, avoid_list)
        
        assert result['avoided_words_used'] == 0
        assert result['clean']
    
    def test_analyze_sentence_structure(self):
        """Test sentence structure analysis"""
        text = "This is a medium sentence with several words. Another one here. Third sentence added."
        preferences = {'sentence_length': 'medium'}
        
        result = BrandVoiceMatcher.analyze_sentence_structure(text, preferences)
        
        assert 'avg_sentence_length' in result
        assert result['total_sentences'] == 3
    
    def test_calculate_overall_match(self):
        """Test overall brand voice matching"""
        text = "Therefore, we present clear findings. Research demonstrates positive outcomes."
        brand_voice = {
            'tone': 'professional',
            'avoid': [],
            'preferences': {'sentence_length': 'medium'}
        }
        
        result = BrandVoiceMatcher.calculate_overall_match(text, brand_voice)
        
        assert 'overall_score' in result
        assert 0 <= result['overall_score'] <= 100
        assert 'recommendation' in result


class TestSEOAnalyzer:
    """Test SEOAnalyzer functionality"""
    
    def test_analyze_keyword_density(self):
        """Test keyword density calculation"""
        text = "AI is important. AI technology advances. The AI field grows. AI AI AI."
        result = SEOAnalyzer.analyze_keyword_density(text, "AI")
        
        assert 'density_percentage' in result
        assert result['occurrences'] > 0
    
    def test_analyze_keyword_density_optimal(self):
        """Test optimal keyword density detection"""
        text = " ".join(["word"] * 98 + ["keyword"] * 2)
        result = SEOAnalyzer.analyze_keyword_density(text, "keyword")
        
        assert result['density_percentage'] == 2.0
        assert result['is_optimal']
    
    def test_analyze_title(self):
        """Test title SEO analysis"""
        title = "Complete Guide to AI Trends in 2025"
        result = SEOAnalyzer.analyze_title(title, "AI Trends")
        
        assert result['has_keyword']
        assert 'score' in result
    
    def test_analyze_title_no_keyword(self):
        """Test title without keyword"""
        title = "Complete Guide to Technology"
        result = SEOAnalyzer.analyze_title(title, "AI Trends")
        
        assert not result['has_keyword']
        assert result['score'] < 100
    
    def test_analyze_meta_description(self):
        """Test meta description analysis"""
        meta = "Learn about AI trends and how artificial intelligence is shaping the future of technology in 2025."
        result = SEOAnalyzer.analyze_meta_description(meta, "AI trends")
        
        assert result['has_keyword']
        assert 'length' in result
    
    def test_analyze_headers(self):
        """Test header structure analysis"""
        text = """# Main Title with Keyword
        
## Section About Keyword
Some content here.

## Another Section
More content.

### Subsection
Details here."""
        
        result = SEOAnalyzer.analyze_headers(text, "Keyword")
        
        assert result['h1_count'] == 1
        assert result['h2_count'] == 2
        assert result['h1_has_keyword']
    
    def test_calculate_overall_seo_score(self):
        """Test comprehensive SEO score calculation"""
        text = """# AI Trends in 2025
        
## Understanding AI
AI technology is advancing rapidly. The AI field continues to grow.

## Future of AI
More content about AI here."""
        
        title = "AI Trends in 2025: Complete Guide"
        meta = "Discover the latest AI trends and how artificial intelligence is transforming technology in 2025."
        
        result = SEOAnalyzer.calculate_overall_seo_score(text, title, meta, "AI trends")
        
        assert 'overall_score' in result
        assert 0 <= result['overall_score'] <= 100
        assert 'grade' in result
        assert 'recommendations' in result
    
    def test_seo_grade_assignment(self):
        """Test SEO grade assignment"""
        assert SEOAnalyzer._get_seo_grade(95) == "A"
        assert SEOAnalyzer._get_seo_grade(85) == "B"
        assert SEOAnalyzer._get_seo_grade(75) == "C"
        assert SEOAnalyzer._get_seo_grade(65) == "D"
        assert SEOAnalyzer._get_seo_grade(50) == "F"


class TestWebSearchTool:
    """Test WebSearchTool functionality"""
    
    def test_create_search_tool(self):
        """Test search tool creation"""
        tool = WebSearchTool.create_search_tool()
        assert tool is not None
    
    def test_format_query_simple(self):
        """Test simple query formatting"""
        query = WebSearchTool.format_query("AI trends")
        assert query == "AI trends"
    
    def test_format_query_with_context(self):
        """Test query formatting with context"""
        query = WebSearchTool.format_query("AI trends", "2025")
        assert "AI trends" in query
        assert "2025" in query