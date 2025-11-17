"""
Content Factory AI - Working Version with Correct Models
"""

import asyncio
import os
from dotenv import load_dotenv
from orchestrator import ContentFactoryOrchestrator
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger(__name__)


async def main():
    """Main execution"""
    
    logger.info("Starting Content Factory AI")
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        logger.error("GOOGLE_API_KEY not found")
        return
    
    logger.info("API key validated")
    
    # Use gemini-2.5-flash (latest stable model with good rate limits)
    orchestrator = ContentFactoryOrchestrator(
        api_key=api_key,
        primary_model='gemini-2.5-flash'
    )
    
    await orchestrator.initialize()
    logger.info("All agents initialized")
    
    topic = "Future of AI Agents in 2025"
    logger.info(f"Creating content for: {topic}")
    
    try:
        # Create content with just blog first (fewer API calls)
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
        print(f"  - Verification Confidence: {result['metrics']['verification_confidence']}%")
        
        await orchestrator.save_outputs(result, topic)
        print(f"\nOutput saved to: examples/sample_output/")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        await orchestrator.cleanup()
        logger.info("Done!")


if __name__ == "__main__":
    asyncio.run(main())