"""
SEO Analyzer - Analyzes and scores SEO elements
"""

from typing import Dict, List
import re


class SEOAnalyzer:
    """Tool for analyzing SEO quality"""
    
    @staticmethod
    def analyze_keyword_density(text: str, keyword: str) -> Dict:
        """Calculate keyword density"""
        text_lower = text.lower()
        keyword_lower = keyword.lower()
        
        total_words = len(text.split())
        keyword_count = text_lower.count(keyword_lower)
        
        density = (keyword_count / total_words * 100) if total_words > 0 else 0
        
        optimal_range = (1, 2.5)
        is_optimal = optimal_range[0] <= density <= optimal_range[1]
        
        return {
            'keyword': keyword,
            'occurrences': keyword_count,
            'density_percentage': round(density, 2),
            'optimal_range': optimal_range,
            'is_optimal': is_optimal,
            'recommendation': 'Good' if is_optimal else ('Increase usage' if density < optimal_range[0] else 'Reduce usage')
        }
    
    @staticmethod
    def analyze_title(title: str, keyword: str) -> Dict:
        """Analyze title SEO"""
        title_length = len(title)
        has_keyword = keyword.lower() in title.lower()
        
        optimal_length = (50, 60)
        length_ok = optimal_length[0] <= title_length <= optimal_length[1]
        
        score = 0
        if length_ok:
            score += 50
        if has_keyword:
            score += 50
        
        return {
            'title': title,
            'length': title_length,
            'optimal_length': optimal_length,
            'length_ok': length_ok,
            'has_keyword': has_keyword,
            'score': score,
            'recommendation': 'Optimize title' if score < 80 else 'Good title'
        }
    
    @staticmethod
    def analyze_meta_description(meta: str, keyword: str) -> Dict:
        """Analyze meta description SEO"""
        meta_length = len(meta)
        has_keyword = keyword.lower() in meta.lower()
        
        optimal_length = (150, 160)
        length_ok = optimal_length[0] <= meta_length <= optimal_length[1]
        
        score = 0
        if length_ok:
            score += 50
        if has_keyword:
            score += 50
        
        return {
            'length': meta_length,
            'optimal_length': optimal_length,
            'length_ok': length_ok,
            'has_keyword': has_keyword,
            'score': score,
            'recommendation': 'Optimize meta' if score < 80 else 'Good meta description'
        }
    
    @staticmethod
    def analyze_headers(text: str, keyword: str) -> Dict:
        """Analyze header structure and keyword usage"""
        h1_pattern = r'^#\s+(.+)$'
        h2_pattern = r'^##\s+(.+)$'
        h3_pattern = r'^###\s+(.+)$'
        
        h1s = re.findall(h1_pattern, text, re.MULTILINE)
        h2s = re.findall(h2_pattern, text, re.MULTILINE)
        h3s = re.findall(h3_pattern, text, re.MULTILINE)
        
        h1_has_keyword = any(keyword.lower() in h.lower() for h in h1s)
        h2_with_keyword = sum(1 for h in h2s if keyword.lower() in h.lower())
        
        score = 0
        if len(h1s) == 1:
            score += 20
        if h1_has_keyword:
            score += 30
        if len(h2s) >= 3:
            score += 25
        if h2_with_keyword >= 1:
            score += 25
        
        return {
            'h1_count': len(h1s),
            'h2_count': len(h2s),
            'h3_count': len(h3s),
            'h1_has_keyword': h1_has_keyword,
            'h2_with_keyword': h2_with_keyword,
            'score': score,
            'recommendation': 'Improve headers' if score < 70 else 'Good header structure'
        }
    
    @staticmethod
    def calculate_overall_seo_score(text: str, title: str, meta: str, keyword: str) -> Dict:
        """Calculate comprehensive SEO score"""
        keyword_analysis = SEOAnalyzer.analyze_keyword_density(text, keyword)
        title_analysis = SEOAnalyzer.analyze_title(title, keyword)
        meta_analysis = SEOAnalyzer.analyze_meta_description(meta, keyword)
        header_analysis = SEOAnalyzer.analyze_headers(text, keyword)
        
        keyword_score = 100 if keyword_analysis['is_optimal'] else 50
        title_score = title_analysis['score']
        meta_score = meta_analysis['score']
        header_score = header_analysis['score']
        
        overall_score = (
            keyword_score * 0.3 +
            title_score * 0.25 +
            meta_score * 0.20 +
            header_score * 0.25
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'keyword_analysis': keyword_analysis,
            'title_analysis': title_analysis,
            'meta_analysis': meta_analysis,
            'header_analysis': header_analysis,
            'grade': SEOAnalyzer._get_seo_grade(overall_score),
            'recommendations': SEOAnalyzer._get_recommendations(
                keyword_analysis, title_analysis, meta_analysis, header_analysis
            )
        }
    
    @staticmethod
    def _get_seo_grade(score: float) -> str:
        """Get letter grade for SEO score"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    @staticmethod
    def _get_recommendations(keyword_analysis: Dict, title_analysis: Dict, 
                            meta_analysis: Dict, header_analysis: Dict) -> List[str]:
        """Generate SEO improvement recommendations"""
        recommendations = []
        
        if not keyword_analysis['is_optimal']:
            recommendations.append(keyword_analysis['recommendation'])
        
        if title_analysis['score'] < 80:
            recommendations.append(f"Title: {title_analysis['recommendation']}")
        
        if meta_analysis['score'] < 80:
            recommendations.append(f"Meta: {meta_analysis['recommendation']}")
        
        if header_analysis['score'] < 70:
            recommendations.append(f"Headers: {header_analysis['recommendation']}")
        
        if not recommendations:
            recommendations.append("SEO is well optimized")
        
        return recommendations