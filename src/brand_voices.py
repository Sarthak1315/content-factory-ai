"""
Brand Voice Management System - With Custom Voice Support
"""

from typing import Dict, List
import json
import os


class BrandVoiceManager:
    """Manages predefined and custom brand voices"""
    
    PREDEFINED_VOICES = {
        'aggressive_consultant': {
            'name': 'Aggressive Consultant',
            'description': 'Bold, contrarian, no-BS consultant who challenges everything',
            'tone': 'aggressive, direct, confrontational',
            'style': 'punchy, bold, unapologetic',
            'perspective': 'first-person expert who has seen everything',
            'sentence_length': 'short to medium',
            'opinion_level': 'very high - strong takes on everything',
            'vocabulary': 'professional but edgy, uses strong verbs',
            'avoid': ['softening language', 'hedging', 'corporate speak', 'maybe', 'perhaps'],
            'use_often': ['here is what actually works', 'stop doing X', 'the truth is', 'most companies fail at'],
            'examples': [
                'Your security strategy is broken. Not outdated - broken.',
                'Stop buying tools you do not need. Start fixing processes you ignored.',
                'Zero Trust is useless if your IAM is garbage.'
            ],
            'writing_rules': [
                'Challenge conventional wisdom aggressively',
                'Call out bad practices by name',
                'Use strong, definitive language',
                'Start sentences with action verbs',
                'Question reader assumptions directly',
                'Provide harsh truths with solutions',
                'Be memorable and quotable'
            ],
            'is_custom': False
        },
        
        'friendly_expert': {
            'name': 'Friendly Expert',
            'description': 'Approachable expert who simplifies complex topics',
            'tone': 'friendly, warm, encouraging',
            'style': 'conversational, clear, accessible',
            'perspective': 'experienced guide helping you succeed',
            'sentence_length': 'medium',
            'opinion_level': 'moderate - balanced with empathy',
            'vocabulary': 'clear professional language, minimal jargon',
            'avoid': ['intimidating terms', 'blame', 'condescension', 'fear mongering'],
            'use_often': ['let me show you', 'here is the good news', 'you can', 'I will help you'],
            'examples': [
                'Let me walk you through this step by step.',
                'Here is the good news: you do not need to do everything at once.',
                'I have helped dozens of companies with this exact problem.'
            ],
            'writing_rules': [
                'Use we/you language frequently',
                'Break complex concepts into simple steps',
                'Acknowledge reader concerns',
                'Provide encouragement along with advice',
                'Use analogies and relatable examples',
                'Build confidence while teaching',
                'Make expertise feel accessible'
            ],
            'is_custom': False
        },
        
        'data_analyst': {
            'name': 'Data-Driven Analyst',
            'description': 'Analytical expert focused on data, ROI, and measurable outcomes',
            'tone': 'analytical, objective, precise',
            'style': 'data-focused, structured, evidence-based',
            'perspective': 'researcher presenting findings',
            'sentence_length': 'medium to long',
            'opinion_level': 'low - data speaks for itself',
            'vocabulary': 'technical and precise, includes metrics',
            'avoid': ['emotional language', 'hyperbole', 'unsubstantiated claims', 'gut feelings'],
            'use_often': ['according to data', 'ROI calculation', 'statistically', 'evidence shows'],
            'examples': [
                'Analysis of 2,847 breach incidents reveals three critical patterns.',
                'ROI calculation: $50K investment reduces breach probability by 73%.',
                'Data from 12-month longitudinal study shows...'
            ],
            'writing_rules': [
                'Lead with data and statistics',
                'Provide specific numbers always',
                'Include methodology when relevant',
                'Show calculations and frameworks',
                'Use charts and data visualization concepts',
                'Focus on measurable outcomes',
                'Cite sources extensively'
            ],
            'is_custom': False
        },
        
        'investigative_journalist': {
            'name': 'Investigative Journalist',
            'description': 'Story-driven expert who uncovers what others miss',
            'tone': 'investigative, revealing, narrative',
            'style': 'story-driven, detailed, exposing',
            'perspective': 'insider revealing the truth',
            'sentence_length': 'varied for narrative flow',
            'opinion_level': 'moderate - focused on uncovering facts',
            'vocabulary': 'vivid, specific, scene-setting',
            'avoid': ['vague generalizations', 'corporate PR language', 'surface coverage'],
            'use_often': ['here is what really happened', 'behind the scenes', 'the untold story', 'what they did not tell you'],
            'examples': [
                'Here is what the breach report did not tell you.',
                'I talked to three CISOs who were there. Here is what actually happened.',
                'The ransomware gang operated for six months before anyone noticed.'
            ],
            'writing_rules': [
                'Use narrative structure',
                'Include specific scenes and moments',
                'Quote real people and sources',
                'Reveal hidden information',
                'Build tension and resolution',
                'Use timeline storytelling',
                'Connect dots others missed'
            ],
            'is_custom': False
        },
        
        'pragmatic_practitioner': {
            'name': 'Pragmatic Practitioner',
            'description': 'Hands-on expert focused on what actually works in practice',
            'tone': 'practical, realistic, experienced',
            'style': 'straightforward, actionable, no-fluff',
            'perspective': 'practitioner who has implemented solutions',
            'sentence_length': 'short to medium',
            'opinion_level': 'high - based on real experience',
            'vocabulary': 'plain language, operational terms',
            'avoid': ['theory without practice', 'vendor marketing', 'buzzwords', 'unrealistic solutions'],
            'use_often': ['in practice', 'what actually works', 'here is how to do it', 'from experience'],
            'examples': [
                'Theory says X. In practice, Y works better.',
                'I have deployed this 47 times. Here is what breaks.',
                'Skip the advanced features. Master the basics first.'
            ],
            'writing_rules': [
                'Prioritize actionable over interesting',
                'Include implementation gotchas',
                'Provide time estimates',
                'Mention common pitfalls',
                'Focus on 80/20 solutions',
                'Share battle-tested approaches',
                'Warn about what fails'
            ],
            'is_custom': False
        }
    }
    
    def __init__(self, storage_path: str = './brand_voices'):
        self.storage_path = storage_path
        self.custom_voices_file = os.path.join(storage_path, 'custom_voices.json')
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage directory if needed"""
        os.makedirs(self.storage_path, exist_ok=True)
        if not os.path.exists(self.custom_voices_file):
            with open(self.custom_voices_file, 'w') as f:
                json.dump({}, f)
    
    def get_all_voices(self) -> Dict[str, Dict]:
        """Get all voices (predefined + custom)"""
        all_voices = self.PREDEFINED_VOICES.copy()
        custom_voices = self.load_custom_voices()
        all_voices.update(custom_voices)
        return all_voices
    
    def load_custom_voices(self) -> Dict[str, Dict]:
        """Load custom voices from storage"""
        try:
            with open(self.custom_voices_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def save_custom_voice(self, voice_id: str, voice_data: Dict) -> bool:
        """Save a custom voice"""
        try:
            custom_voices = self.load_custom_voices()
            voice_data['is_custom'] = True
            custom_voices[voice_id] = voice_data
            
            with open(self.custom_voices_file, 'w', encoding='utf-8') as f:
                json.dump(custom_voices, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving voice: {e}")
            return False
    
    def delete_custom_voice(self, voice_id: str) -> bool:
        """Delete a custom voice"""
        try:
            custom_voices = self.load_custom_voices()
            if voice_id in custom_voices:
                del custom_voices[voice_id]
                
                with open(self.custom_voices_file, 'w', encoding='utf-8') as f:
                    json.dump(custom_voices, f, indent=2, ensure_ascii=False)
                
                return True
            return False
        except Exception:
            return False
    
    def get_voice(self, voice_id: str) -> Dict:
        """Get specific voice by ID"""
        all_voices = self.get_all_voices()
        return all_voices.get(voice_id, self.PREDEFINED_VOICES['pragmatic_practitioner'])
    
    def parse_voice_from_text(self, text: str) -> Dict:
        """Parse brand voice from free-form text description"""
        # This creates a voice profile from natural language description
        voice = {
            'name': 'Custom Voice',
            'description': text[:200],
            'tone': self._extract_tone(text),
            'style': text[:500],
            'perspective': 'expert voice',
            'sentence_length': 'medium',
            'opinion_level': 'moderate',
            'vocabulary': 'professional',
            'avoid': [],
            'use_often': [],
            'examples': [],
            'writing_rules': [
                'Follow the voice description provided',
                'Maintain consistency throughout',
                'Match the tone and style described'
            ],
            'full_description': text,
            'is_custom': True
        }
        return voice
    
    def _extract_tone(self, text: str) -> str:
        """Extract tone keywords from text"""
        tone_keywords = {
            'aggressive': ['aggressive', 'bold', 'direct', 'confrontational', 'harsh', 'blunt'],
            'friendly': ['friendly', 'warm', 'approachable', 'welcoming', 'kind'],
            'professional': ['professional', 'formal', 'business', 'corporate'],
            'casual': ['casual', 'informal', 'relaxed', 'conversational'],
            'analytical': ['analytical', 'data-driven', 'logical', 'systematic']
        }
        
        text_lower = text.lower()
        detected_tones = []
        
        for tone, keywords in tone_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_tones.append(tone)
        
        return ', '.join(detected_tones) if detected_tones else 'professional, clear'


# Global instance
brand_voice_manager = BrandVoiceManager()