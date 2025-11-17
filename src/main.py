"""
Content Factory AI - Rate Limited Version
"""

import asyncio
import os
import time
from dotenv import load_dotenv
from orchestrator import ContentFactoryOrchestrator
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger(__name__)


async def main():
    """Main execution with rate limiting"""
    
    logger.info("Starting Content Factory AI (Rate Limited)")
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        logger.error("GOOGLE_API_KEY not found")
        return
    
    logger.info("API key validated")
    logger.info("Waiting 60 seconds to avoid rate limits...")
    time.sleep(60)  # Wait 1 minute to reset rate limits
    
    orchestrator = ContentFactoryOrchestrator(
        api_key=api_key,
        primary_model='gemini-2.0-flash-exp'  # Use original model
    )
    
    await orchestrator.initialize()
    logger.info("All agents initialized")
    
    topic = "Future of AI Agents in 2025"
    logger.info(f"Creating content for: {topic}")
    
    try:
        # Create content with just blog first (less API calls)
        result = await orchestrator.create_content_package(
            topic=topic,
            session_id="demo_001",
            platforms=['blog']  # Start with just blog
        )
        
        print("\n" + "="*60)
        print("CONTENT CREATED SUCCESSFULLY!")
        print("="*60)
        print("\nBLOG POST:")
        print(result['blog'][:500])
        print("\n... (truncated)")
        
        print(f"\nMETRICS:")
        print(f"  - Word count: {result['metrics']['blog_word_count']}")
        print(f"  - Duration: {result['metrics']['duration_seconds']:.2f}s")
        print(f"  - SEO Score: {result['metrics']['seo_score']}/100")
        print(f"  - Readability: {result['metrics']['readability_score']}/100")
        
        await orchestrator.save_outputs(result, topic)
        print(f"\nSaved to: examples/sample_output/")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    
    finally:
        await orchestrator.cleanup()


if __name__ == "__main__":
    asyncio.run(main())