"""
Brand Voice Matcher - Analyzes and matches brand voice consistency
"""

from typing import Dict, List
import re


class BrandVoiceMatcher:
    """Tool for analyzing brand voice consistency"""
    
    @staticmethod
    def analyze_tone(text: str, target_tone: str) -> Dict:
        """Analyze if text matches target tone"""
        text_lower = text.lower()
        
        tone_indicators = {
            'professional': ['therefore', 'however', 'furthermore', 'additionally', 'consequently'],
            'casual': ['hey', 'awesome', 'cool', 'basically', 'stuff', 'things'],
            'friendly': ['you', 'your', 'we', 'our', 'together'],
            'authoritative': ['research shows', 'studies indicate', 'evidence suggests', 'proven', 'demonstrated'],
            'conversational': ['you know', "let's", "we'll", "you're", "it's"]
        }
        
        target_indicators = tone_indicators.get(target_tone.lower(), [])
        matches = sum(1 for indicator in target_indicators if indicator in text_lower)
        
        score = min(100, (matches / len(target_indicators) * 100)) if target_indicators else 50
        
        return {
            'tone': target_tone,
            'match_score': round(score, 2),
            'matches_found': matches,
            'indicators_checked': len(target_indicators)
        }
    
    @staticmethod
    def check_avoided_words(text: str, avoid_list: List[str]) -> Dict:
        """Check for words that should be avoided"""
        text_lower = text.lower()
        found_words = []
        
        for word in avoid_list:
            if word.lower() in text_lower:
                count = text_lower.count(word.lower())
                found_words.append({
                    'word': word,
                    'count': count
                })
        
        return {
            'avoided_words_used': len(found_words),
            'details': found_words,
            'clean': len(found_words) == 0
        }
    
    @staticmethod
    def analyze_sentence_structure(text: str, preferences: Dict) -> Dict:
        """Analyze sentence structure against preferences"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        word_counts = [len(s.split()) for s in sentences]
        avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
        
        target_length = preferences.get('sentence_length', 'medium')
        length_ranges = {
            'short': (5, 12),
            'medium': (12, 20),
            'long': (20, 30)
        }
        
        target_range = length_ranges.get(target_length, (12, 20))
        in_range = sum(1 for wc in word_counts if target_range[0] <= wc <= target_range[1])
        
        match_percentage = (in_range / len(word_counts) * 100) if word_counts else 0
        
        return {
            'avg_sentence_length': round(avg_words, 2),
            'target_range': target_range,
            'match_percentage': round(match_percentage, 2),
            'total_sentences': len(sentences)
        }
    
    @staticmethod
    def calculate_overall_match(text: str, brand_voice: Dict) -> Dict:
        """Calculate overall brand voice match score"""
        tone_match = BrandVoiceMatcher.analyze_tone(
            text, 
            brand_voice.get('tone', 'professional')
        )
        
        avoided = BrandVoiceMatcher.check_avoided_words(
            text,
            brand_voice.get('avoid', [])
        )
        
        structure = BrandVoiceMatcher.analyze_sentence_structure(
            text,
            brand_voice.get('preferences', {})
        )
        
        tone_score = tone_match['match_score']
        avoid_score = 100 if avoided['clean'] else max(0, 100 - (avoided['avoided_words_used'] * 10))
        structure_score = structure['match_percentage']
        
        overall_score = (tone_score * 0.4 + avoid_score * 0.3 + structure_score * 0.3)
        
        return {
            'overall_score': round(overall_score, 2),
            'tone_analysis': tone_match,
            'avoided_words_analysis': avoided,
            'structure_analysis': structure,
            'recommendation': 'Good match' if overall_score >= 80 else 'Needs adjustment'
        }