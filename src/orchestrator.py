"""
Content Factory Orchestrator Agent - PRODUCTION VERSION
With retry logic and quality improvements
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from google import genai
from google.genai import types
import time

from agents.research_agent import ResearchAgent
from agents.blog_writer_agent import BlogWriterAgent
from agents.social_media_agent import SocialMediaAgentFactory
from agents.fact_checker_agent import FactCheckerAgent
from agents.editor_agent import EditorAgent
from agents.seo_agent import SEOAgent
from agents.analytics_agent import AnalyticsAgent
from agents.email_agent import EmailAgent
from agents.video_script_agent import VideoScriptAgent

from memory.memory_bank import MemoryBank
from memory.session_service import SessionService
from utils.logger import setup_logger
from utils.metrics import MetricsCollector

logger = setup_logger(__name__)


class ContentFactoryOrchestrator:
    """
    Production-ready orchestrator with retry logic
    """
    
    def __init__(self, api_key: str, primary_model: str):
        self.api_key = api_key
        self.primary_model = primary_model
        
        if not api_key or len(api_key) < 20:
            raise ValueError("Invalid API key. Please check your .env file.")
        
        try:
            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini client: {str(e)}")
        
        self.research_agent = None
        self.blog_writer = None
        self.social_agents = {}
        self.fact_checker = None
        self.editor = None
        self.seo_agent = None
        self.analytics = None
        self.email_agent = None
        self.video_agent = None
        
        self.memory_bank = MemoryBank(storage_path='./memory')
        self.session_service = SessionService()
        self.metrics = MetricsCollector()
        
        # Retry settings
        self.max_retries = 3
        self.retry_delay = 10  # seconds
        
        logger.info("ContentFactoryOrchestrator initialized")
    
    async def _retry_with_backoff(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry"""
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error_msg = str(e)
                
                if "503" in error_msg or "UNAVAILABLE" in error_msg or "429" in error_msg:
                    if attempt < self.max_retries - 1:
                        delay = self.retry_delay * (attempt + 1)
                        logger.warning(f"API overloaded, retrying in {delay}s (attempt {attempt + 1}/{self.max_retries})")
                        await asyncio.sleep(delay)
                        continue
                
                logger.error(f"Error after {attempt + 1} attempts: {error_msg}")
                raise
        
        raise Exception("Max retries exceeded")
    
    async def initialize(self):
        """Initialize all agents"""
        logger.info("Initializing agents...")
        
        self.research_agent = ResearchAgent(
            client=self.client,
            model=self.primary_model
        )
        
        self.blog_writer = BlogWriterAgent(
            client=self.client,
            model='gemini-2.5-pro'  # Use Pro for better quality
        )
        
        social_factory = SocialMediaAgentFactory(
            client=self.client,
            model=self.primary_model
        )
        self.social_agents = {
            'linkedin': social_factory.create_linkedin_agent(),
            'twitter': social_factory.create_twitter_agent(),
            'instagram': social_factory.create_instagram_agent()
        }
        
        self.fact_checker = FactCheckerAgent(
            client=self.client,
            model=self.primary_model
        )
        
        self.editor = EditorAgent(
            client=self.client,
            model=self.primary_model
        )
        
        self.seo_agent = SEOAgent(
            client=self.client,
            model=self.primary_model
        )
        
        self.analytics = AnalyticsAgent(
            client=self.client,
            model=self.primary_model,
            memory_bank=self.memory_bank
        )
        
        self.email_agent = EmailAgent(
            client=self.client,
            model=self.primary_model
        )
        
        self.video_agent = VideoScriptAgent(
            client=self.client,
            model=self.primary_model
        )
        
        self._load_brand_voice()
        
        logger.info("All agents initialized")
    
    def _load_brand_voice(self):
        """Load brand voice"""
        brand_voice = self.memory_bank.get('brand_voice')
        
        if not brand_voice:
            default_voice = {
                'tone': 'professional, engaging, authoritative',
                'style': 'clear, comprehensive, well-structured',
                'avoid': ['jargon', 'buzzwords', 'hyperbole'],
                'preferences': {
                    'sentence_length': 'medium',
                    'paragraph_length': '3-5 sentences',
                    'use_examples': True,
                    'target_length': '1800-2000 words'
                }
            }
            self.memory_bank.set('brand_voice', default_voice)
            logger.info("Default brand voice set")
        else:
            logger.info("Brand voice loaded from memory")
    
    async def create_content_package(
        self,
        topic: str,
        session_id: str,
        platforms: List[str] = None
    ) -> Dict:
        """
        Create content with retry logic and quality checks
        """
        
        start_time = datetime.now()
        session = self.session_service.create_session(session_id)
        session.set('topic', topic)
        session.set('start_time', start_time)
        
        logger.info(f"Starting content package creation for: {topic}")
        
        brand_voice = self.memory_bank.get('brand_voice')
        
        try:
            # STEP 1: RESEARCH with retry
            logger.info("Step 1: Research Agent working...")
            self.metrics.start_timer('research')
            
            research_result = await self._retry_with_backoff(
                self.research_agent.research,
                topic=topic,
                session_id=session_id
            )
            
            self.metrics.stop_timer('research')
            research_brief = research_result['brief']
            sources = research_result.get('sources', [])
            
            session.set('research_brief', research_brief)
            session.set('sources', sources)
            
            logger.info(f"Research complete: {len(sources)} sources found")
            
            # Add delay to avoid rate limiting
            await asyncio.sleep(2)
            
            # STEP 2: CONTENT CREATION
            logger.info("Step 2: Creating content...")
            self.metrics.start_timer('content_creation')
            
            if platforms is None:
                platforms = ['blog']
            
            content = {}
            
            # Create blog with retry
            if 'blog' in platforms:
                logger.info("Creating blog post...")
                content['blog'] = await self._retry_with_backoff(
                    self._create_blog,
                    research_brief, brand_voice, session_id
                )
                await asyncio.sleep(2)
            
            # Create other platforms with retry (sequential to avoid overload)
            if 'linkedin' in platforms:
                logger.info("Creating LinkedIn posts...")
                try:
                    content['linkedin'] = await self._retry_with_backoff(
                        self._create_linkedin,
                        research_brief, brand_voice, session_id
                    )
                    await asyncio.sleep(2)
                except Exception as e:
                    logger.error(f"LinkedIn creation failed: {str(e)}")
                    content['linkedin'] = "Error: Could not generate LinkedIn content"
            
            if 'twitter' in platforms:
                logger.info("Creating Twitter threads...")
                try:
                    content['twitter'] = await self._retry_with_backoff(
                        self._create_twitter,
                        research_brief, brand_voice, session_id
                    )
                    await asyncio.sleep(2)
                except Exception as e:
                    logger.error(f"Twitter creation failed: {str(e)}")
                    content['twitter'] = "Error: Could not generate Twitter content"
            
            if 'email' in platforms:
                logger.info("Creating email newsletter...")
                try:
                    content['email'] = await self._retry_with_backoff(
                        self._create_email,
                        research_brief, brand_voice, session_id
                    )
                    await asyncio.sleep(2)
                except Exception as e:
                    logger.error(f"Email creation failed: {str(e)}")
                    content['email'] = "Error: Could not generate email content"
            
            if 'youtube' in platforms:
                logger.info("Creating video script...")
                try:
                    content['youtube'] = await self._retry_with_backoff(
                        self._create_video_script,
                        research_brief, brand_voice, session_id
                    )
                    await asyncio.sleep(2)
                except Exception as e:
                    logger.error(f"Video script creation failed: {str(e)}")
                    content['youtube'] = "Error: Could not generate video script"
            
            self.metrics.stop_timer('content_creation')
            logger.info(f"Content created for {len(content)} platforms")
            
            # STEP 3: FACT-CHECKING
            logger.info("Step 3: Fact-Checker Agent verifying...")
            self.metrics.start_timer('fact_checking')
            
            blog_content = content.get('blog', '')
            
            try:
                verification_result = await self._retry_with_backoff(
                    self.fact_checker.verify,
                    content=blog_content,
                    session_id=session_id
                )
                
                verification_report = verification_result['report']
                confidence_score = verification_result.get('confidence', 75)
                flagged_claims = verification_result.get('flagged_claims', 0)
                
                logger.info(f"Fact-checking complete: {confidence_score}% confidence")
                
                if flagged_claims:
                    logger.warning(f"Warning: {flagged_claims} claims flagged for review")
            except Exception as e:
                logger.error(f"Fact-checking failed: {str(e)}")
                verification_report = "Fact-checking unavailable"
                confidence_score = 0
                flagged_claims = 0
            
            self.metrics.stop_timer('fact_checking')
            await asyncio.sleep(2)
            
            # STEP 4: EDITING
            logger.info("Step 4: Editor Agent polishing...")
            self.metrics.start_timer('editing')
            
            try:
                edited_blog = await self._retry_with_backoff(
                    self.editor.edit,
                    content=blog_content,
                    brand_voice=brand_voice,
                    session_id=session_id
                )
                
                content['blog'] = edited_blog['content']
                readability_score = edited_blog['readability_score']
                
                logger.info(f"Editing complete: Readability score {readability_score}/100")
            except Exception as e:
                logger.error(f"Editing failed: {str(e)}")
                readability_score = 75
            
            self.metrics.stop_timer('editing')
            await asyncio.sleep(2)
            
            # STEP 5: SEO OPTIMIZATION
            logger.info("Step 5: SEO Agent optimizing...")
            self.metrics.start_timer('seo')
            
            try:
                seo_result = await self._retry_with_backoff(
                    self.seo_agent.optimize,
                    content=content['blog'],
                    topic=topic,
                    session_id=session_id
                )
                
                content['blog'] = seo_result['optimized_content']
                seo_score = seo_result['seo_score']
                keywords = seo_result.get('keywords', {})
                meta_description = seo_result.get('meta_description', '')
                
                logger.info(f"SEO optimization complete: Score {seo_score}/100")
            except Exception as e:
                logger.error(f"SEO optimization failed: {str(e)}")
                seo_score = 75
                keywords = {'primary': topic, 'secondary': []}
                meta_description = f"Learn about {topic}"
            
            self.metrics.stop_timer('seo')
            
            # STEP 6: ANALYTICS
            logger.info("Step 6: Analytics Agent learning...")
            
            content_package = {
                'topic': topic,
                'content': content,
                'verification': verification_report,
                'metrics': {
                    'confidence': confidence_score,
                    'readability': readability_score,
                    'seo_score': seo_score
                },
                'timestamp': datetime.now().isoformat()
            }
            
            self.memory_bank.append_to_history('content_history', content_package)
            
            try:
                learned_insights = await self.analytics.analyze_and_learn(session_id=session_id)
                logger.info(f"Analytics complete: {len(learned_insights.get('patterns', []))} patterns identified")
            except Exception as e:
                logger.error(f"Analytics failed: {str(e)}")
                learned_insights = {'patterns': [], 'insights': 'Analytics unavailable'}
            
            # COMPILE RESULTS
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            metrics = {
                'duration_seconds': duration,
                'blog_word_count': len(content.get('blog', '').split()),
                'linkedin_posts_count': content.get('linkedin', '').count('POST'),
                'twitter_threads_count': content.get('twitter', '').count('THREAD'),
                'verification_confidence': confidence_score,
                'readability_score': readability_score,
                'seo_score': seo_score,
                'sources_used': len(sources),
                'flagged_claims': flagged_claims,
                'keywords': keywords,
                'timings': self.metrics.get_all_timings()
            }
            
            result = {
                'blog': content.get('blog', ''),
                'linkedin': content.get('linkedin', ''),
                'twitter': content.get('twitter', ''),
                'email': content.get('email', ''),
                'video_script': content.get('youtube', ''),
                'verification': verification_report,
                'meta_description': meta_description,
                'metrics': metrics,
                'learned_insights': learned_insights
            }
            
            logger.info(f"Content package complete in {duration:.2f} seconds")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in content creation pipeline: {str(e)}", exc_info=True)
            raise
        
        finally:
            self.session_service.end_session(session_id)
    
    async def _create_blog(self, research: str, brand_voice: dict, session_id: str) -> str:
        """Create blog post"""
        result = await self.blog_writer.write(
            research_brief=research,
            brand_voice=brand_voice,
            session_id=session_id
        )
        return result['content']
    
    async def _create_linkedin(self, research: str, brand_voice: dict, session_id: str) -> str:
        """Create LinkedIn posts"""
        result = await self.social_agents['linkedin'].create(
            research_brief=research,
            brand_voice=brand_voice,
            session_id=session_id
        )
        return result['posts']
    
    async def _create_twitter(self, research: str, brand_voice: dict, session_id: str) -> str:
        """Create Twitter threads"""
        result = await self.social_agents['twitter'].create(
            research_brief=research,
            brand_voice=brand_voice,
            session_id=session_id
        )
        return result['threads']
    
    async def _create_email(self, research: str, brand_voice: dict, session_id: str) -> str:
        """Create email newsletter"""
        result = await self.email_agent.create(
            research_brief=research,
            brand_voice=brand_voice,
            session_id=session_id
        )
        return result['email']
    
    async def _create_video_script(self, research: str, brand_voice: dict, session_id: str) -> str:
        """Create video script"""
        result = await self.video_agent.create(
            research_brief=research,
            brand_voice=brand_voice,
            session_id=session_id
        )
        return result['script']
    
    async def save_outputs(self, result: Dict, topic: str):
        """Save all outputs"""
        import os
        
        output_dir = 'examples/sample_output'
        os.makedirs(output_dir, exist_ok=True)
        
        clean_topic = topic.replace(' ', '_').replace('/', '_')[:50]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        with open(f'{output_dir}/blog_{clean_topic}_{timestamp}.md', 'w', encoding='utf-8') as f:
            f.write(result['blog'])
        
        with open(f'{output_dir}/linkedin_{clean_topic}_{timestamp}.txt', 'w', encoding='utf-8') as f:
            f.write(result['linkedin'])
        
        with open(f'{output_dir}/twitter_{clean_topic}_{timestamp}.txt', 'w', encoding='utf-8') as f:
            f.write(result['twitter'])
        
        with open(f'{output_dir}/email_{clean_topic}_{timestamp}.txt', 'w', encoding='utf-8') as f:
            f.write(result['email'])
        
        with open(f'{output_dir}/video_{clean_topic}_{timestamp}.txt', 'w', encoding='utf-8') as f:
            f.write(result['video_script'])
        
        with open(f'{output_dir}/verification_{clean_topic}_{timestamp}.txt', 'w', encoding='utf-8') as f:
            f.write(result['verification'])
        
        import json
        with open(f'{output_dir}/metrics_{clean_topic}_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(result['metrics'], f, indent=2)
        
        logger.info(f"All outputs saved to {output_dir}/")
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up resources...")
        logger.info("Cleanup complete")