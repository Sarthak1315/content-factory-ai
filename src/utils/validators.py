"""
Content Validator - Validate content quality and requirements
"""

from typing import Dict, List
import re


class ContentValidator:
    """Validate content against quality standards"""
    
    @staticmethod
    def validate_blog_post(content: str, min_words: int = 1500, max_words: int = 2500) -> Dict:
        """Validate blog post meets requirements"""
        word_count = len(content.split())
        has_title = bool(re.search(r'^#\s+.+$', content, re.MULTILINE))
        has_headers = bool(re.search(r'^##\s+.+$', content, re.MULTILINE))
        has_content = len(content.strip()) > 0
        
        issues = []
        if word_count < min_words:
            issues.append(f"Word count too low: {word_count} (minimum {min_words})")
        elif word_count > max_words:
            issues.append(f"Word count too high: {word_count} (maximum {max_words})")
        
        if not has_title:
            issues.append("Missing H1 title")
        
        if not has_headers:
            issues.append("Missing H2 headers")
        
        if not has_content:
            issues.append("Content is empty")
        
        return {
            'valid': len(issues) == 0,
            'word_count': word_count,
            'has_title': has_title,
            'has_headers': has_headers,
            'issues': issues,
            'score': ContentValidator._calculate_blog_score(
                word_count, has_title, has_headers, min_words, max_words
            )
        }
    
    @staticmethod
    def _calculate_blog_score(word_count: int, has_title: bool, has_headers: bool, 
                             min_words: int, max_words: int) -> int:
        """Calculate blog quality score"""
        score = 0
        
        if min_words <= word_count <= max_words:
            score += 40
        elif word_count > min_words * 0.8:
            score += 20
        
        if has_title:
            score += 30
        
        if has_headers:
            score += 30
        
        return score
    
    @staticmethod
    def validate_social_post(content: str, platform: str) -> Dict:
        """Validate social media post for specific platform"""
        limits = {
            'twitter': 280,
            'linkedin': 3000,
            'instagram': 2200
        }
        
        char_count = len(content)
        max_chars = limits.get(platform.lower(), 1000)
        
        within_limit = char_count <= max_chars
        has_content = len(content.strip()) > 0
        has_hashtags = '#' in content
        
        issues = []
        if not has_content:
            issues.append("Content is empty")
        
        if not within_limit:
            issues.append(f"Exceeds {platform} limit: {char_count}/{max_chars} characters")
        
        if platform.lower() in ['twitter', 'linkedin', 'instagram'] and not has_hashtags:
            issues.append(f"Consider adding hashtags for {platform}")
        
        return {
            'valid': len(issues) == 0,
            'platform': platform,
            'char_count': char_count,
            'max_chars': max_chars,
            'within_limit': within_limit,
            'has_hashtags': has_hashtags,
            'issues': issues
        }
    
    @staticmethod
    def validate_email(content: str) -> Dict:
        """Validate email newsletter"""
        has_subject = 'Subject:' in content or 'SUBJECT LINE' in content.upper()
        has_body = len(content) > 100
        has_cta = any(word in content.upper() for word in ['CLICK', 'LEARN MORE', 'READ', 'GET', 'DOWNLOAD'])
        
        word_count = len(content.split())
        optimal_length = 300 <= word_count <= 600
        
        issues = []
        if not has_subject:
            issues.append("Missing subject line")
        
        if not has_body:
            issues.append("Email body too short")
        
        if not has_cta:
            issues.append("Missing clear call-to-action")
        
        if not optimal_length:
            issues.append(f"Word count not optimal: {word_count} (target: 300-600)")
        
        return {
            'valid': len(issues) == 0,
            'has_subject': has_subject,
            'has_body': has_body,
            'has_cta': has_cta,
            'word_count': word_count,
            'optimal_length': optimal_length,
            'issues': issues
        }
    
    @staticmethod
    def validate_video_script(content: str) -> Dict:
        """Validate video script"""
        has_timestamps = bool(re.search(r'\[\d{2}:\d{2}\]', content))
        has_hook = '[00:00]' in content or '[0:00]' in content
        has_sections = content.count('[') >= 3
        
        word_count = len(content.split())
        duration_estimate = word_count / 150
        
        issues = []
        if not has_timestamps:
            issues.append("Missing timestamps")
        
        if not has_hook:
            issues.append("Missing hook section at start")
        
        if not has_sections:
            issues.append("Needs more sections/chapters")
        
        if word_count < 800:
            issues.append(f"Script too short: {word_count} words (minimum 800)")
        
        return {
            'valid': len(issues) == 0,
            'has_timestamps': has_timestamps,
            'has_hook': has_hook,
            'has_sections': has_sections,
            'word_count': word_count,
            'estimated_duration_minutes': round(duration_estimate, 1),
            'issues': issues
        }
    
    @staticmethod
    def validate_all_content(content_package: Dict) -> Dict:
        """Validate entire content package"""
        results = {}
        
        if 'blog' in content_package:
            results['blog'] = ContentValidator.validate_blog_post(content_package['blog'])
        
        if 'linkedin' in content_package:
            results['linkedin'] = ContentValidator.validate_social_post(
                content_package['linkedin'], 'linkedin'
            )
        
        if 'twitter' in content_package:
            results['twitter'] = ContentValidator.validate_social_post(
                content_package['twitter'], 'twitter'
            )
        
        if 'email' in content_package:
            results['email'] = ContentValidator.validate_email(content_package['email'])
        
        if 'video_script' in content_package:
            results['video_script'] = ContentValidator.validate_video_script(
                content_package['video_script']
            )
        
        all_valid = all(result.get('valid', False) for result in results.values())
        total_issues = sum(len(result.get('issues', [])) for result in results.values())
        
        return {
            'all_valid': all_valid,
            'total_issues': total_issues,
            'results': results
        }