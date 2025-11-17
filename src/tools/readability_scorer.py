"""
Readability Scorer - Analyzes content readability
"""

import textstat
from typing import Dict


class ReadabilityScorer:
    """Tool for calculating readability scores"""
    
    @staticmethod
    def calculate_scores(text: str) -> Dict:
        """Calculate various readability scores"""
        try:
            flesch_reading_ease = textstat.flesch_reading_ease(text)
            flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
            gunning_fog = textstat.gunning_fog(text)
            smog_index = textstat.smog_index(text)
            automated_readability = textstat.automated_readability_index(text)
            
            scores = {
                'flesch_reading_ease': round(flesch_reading_ease, 2),
                'flesch_kincaid_grade': round(flesch_kincaid_grade, 2),
                'gunning_fog': round(gunning_fog, 2),
                'smog_index': round(smog_index, 2),
                'automated_readability': round(automated_readability, 2),
                'overall_score': round(flesch_reading_ease, 2)
            }
            
            return scores
            
        except Exception as e:
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'gunning_fog': 0,
                'smog_index': 0,
                'automated_readability': 0,
                'overall_score': 0,
                'error': str(e)
            }
    
    @staticmethod
    def get_reading_level(score: float) -> str:
        """Get reading level description from Flesch score"""
        if score >= 90:
            return "Very Easy (5th grade)"
        elif score >= 80:
            return "Easy (6th grade)"
        elif score >= 70:
            return "Fairly Easy (7th grade)"
        elif score >= 60:
            return "Standard (8th-9th grade)"
        elif score >= 50:
            return "Fairly Difficult (10th-12th grade)"
        elif score >= 30:
            return "Difficult (College)"
        else:
            return "Very Difficult (College graduate)"
    
    @staticmethod
    def calculate_statistics(text: str) -> Dict:
        """Calculate text statistics"""
        try:
            word_count = textstat.lexicon_count(text, removepunct=True)
            sentence_count = textstat.sentence_count(text)
            syllable_count = textstat.syllable_count(text)
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            
            return {
                'word_count': word_count,
                'sentence_count': sentence_count,
                'syllable_count': syllable_count,
                'avg_sentence_length': round(avg_sentence_length, 2),
                'difficult_words': textstat.difficult_words(text)
            }
            
        except Exception as e:
            return {
                'word_count': 0,
                'sentence_count': 0,
                'syllable_count': 0,
                'avg_sentence_length': 0,
                'difficult_words': 0,
                'error': str(e)
            }