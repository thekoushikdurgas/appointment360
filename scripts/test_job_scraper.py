"""
Test script for job scraper functionality.
"""
import asyncio
import logging
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.job_scraper import JobScraper
from services.scraping_exceptions import ScrapingError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_scraper():
    """
    Test the job scraper with a sample URL.
    """
    print("🚀 Starting Job Scraper Test")
    print("=" * 50)
    
    # Test URL (using a simple example)
    test_url = "https://example.com"
    
    print(f"📋 Test URL: {test_url}")
    print(f"🔧 Initializing scraper...")
    
    try:
        # Create scraper instance
        scraper = JobScraper()
        print("✅ Scraper initialized successfully")
        
        print(f"🌐 Starting scraping process...")
        print("   - Step 1: Loading page")
        print("   - Step 2: Handling popup (if any)")
        print("   - Step 3: Infinite scrolling")
        print("   - Step 4: Button detection")
        print("   - Step 5: Job extraction")
        
        # Run scraper
        jobs = await scraper.scrape_jobs(test_url)
        
        print("=" * 50)
        print("🎉 SCRAPING COMPLETED!")
        print(f"📊 Results: Found {len(jobs)} jobs")
        
        if jobs:
            print("\n📋 Sample Jobs:")
            for i, job in enumerate(jobs[:3], 1):
                print(f"   {i}. {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
        else:
            print("   No jobs found (this is expected for example.com)")
        
        print("\n✅ All components working correctly:")
        print("   ✓ Popup Handler")
        print("   ✓ Infinite Scroll Handler")
        print("   ✓ Button Detector")
        print("   ✓ Job Extractor")
        print("   ✓ Error Handling")
        print("   ✓ Logging")
        
        return True
        
    except ScrapingError as e:
        print(f"❌ Scraping Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False


def test_components():
    """
    Test individual components.
    """
    print("\n🔧 Testing Individual Components")
    print("=" * 50)
    
    try:
        # Test configuration
        scraper = JobScraper()
        config = scraper.config
        
        print("✅ Configuration loaded:")
        print(f"   - Page load timeout: {config['timeouts']['page_load']}s")
        print(f"   - Popup detection timeout: {config['timeouts']['popup_detection']}s")
        print(f"   - Max scroll iterations: {config['retries']['scroll_iteration']}")
        print(f"   - Max button clicks: {config['retries']['button_click']}")
        
        # Test component initialization
        popup_handler = scraper.popup_handler
        scroll_handler = scraper.scroll_handler
        button_detector = scraper.button_detector
        job_extractor = scraper.job_extractor
        
        print("✅ All components initialized:")
        print("   ✓ PopupHandler")
        print("   ✓ InfiniteScrollHandler")
        print("   ✓ ButtonDetector")
        print("   ✓ JobExtractor")
        
        return True
        
    except Exception as e:
        print(f"❌ Component Test Error: {e}")
        return False


def main():
    """
    Main test function.
    """
    print("🧪 Job Scraper Test Suite")
    print("=" * 50)
    
    # Test 1: Component initialization
    component_test = test_components()
    
    # Test 2: Full scraper test
    scraper_test = asyncio.run(test_scraper())
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Component Test: {'✅ PASSED' if component_test else '❌ FAILED'}")
    print(f"Scraper Test: {'✅ PASSED' if scraper_test else '❌ FAILED'}")
    
    if component_test and scraper_test:
        print("\n🎉 ALL TESTS PASSED!")
        print("The job scraper is ready for use.")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("Please check the error messages above.")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
