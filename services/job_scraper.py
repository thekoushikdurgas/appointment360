"""
Job Scraper Service
Learn, understand, and implement job scraping with popup handling,
infinite scrolling, and dynamic button clicking.
"""
import asyncio
import logging
from typing import Dict, List, Optional
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

from .scraping_exceptions import (
    PopupNotFoundError,
    PopupDismissalError,
    ScrollTimeoutError,
    ButtonNotFoundError,
    ExtractionError,
    NetworkError,
    ScrapingError
)

logger = logging.getLogger(__name__)


class PopupHandler:
    """
    Handles popup detection and dismissal.
    Learning: Understand modal structures and DOM manipulation.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.popup_selector = config.get('selectors', {}).get('popup', '.top-level-modal-container')
        self.close_button_selector = config.get('selectors', {}).get('close_button', 'button.close, button[aria-label="Close"]')
        self.timeout = config.get('timeouts', {}).get('popup_detection', 5)
        self.max_retries = config.get('retries', {}).get('popup_dismissal', 3)
        
    async def detect_popup(self, page: Page) -> bool:
        """
        Detect if popup exists on the page.
        Learn: Understand CSS selectors and element visibility.
        """
        try:
            logger.info(f"Looking for popup with selector: {self.popup_selector}")
            popup = await page.query_selector(self.popup_selector)
            if popup:
                is_visible = await page.is_visible(self.popup_selector)
                logger.info(f"Popup detected and visible: {is_visible}")
                return is_visible
            return False
        except Exception as e:
            logger.error(f"Error detecting popup: {e}")
            return False
    
    async def dismiss_popup(self, page: Page) -> bool:
        """
        Dismiss the popup by clicking close button or pressing ESC.
        Learn: Understand button interactions and keyboard events.
        """
        try:
            # Method 1: Try to find and click close button
            logger.info("Attempting to find close button")
            close_button = await page.query_selector(self.close_button_selector)
            
            if close_button:
                is_visible = await close_button.is_visible()
                if is_visible:
                    logger.info("Close button found and visible, clicking...")
                    await close_button.click(timeout=2000)
                    
                    # Wait a bit for popup to close
                    await asyncio.sleep(0.5)
                    
                    # Verify popup is gone
                    if not await self.detect_popup(page):
                        logger.info("Popup successfully dismissed")
                        return True
            
            # Method 2: Try pressing ESC key
            logger.info("Trying ESC key to dismiss popup")
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.5)
            
            if not await self.detect_popup(page):
                logger.info("Popup dismissed with ESC key")
                return True
                
            # Method 3: Click outside popup (backdrop)
            logger.info("Trying backdrop click")
            popup = await page.query_selector(self.popup_selector)
            if popup:
                box = await popup.bounding_box()
                if box:
                    # Click slightly outside the popup
                    await page.mouse.click(box['x'] - 10, box['y'] - 10)
                    await asyncio.sleep(0.5)
                    
                    if not await self.detect_popup(page):
                        logger.info("Popup dismissed with backdrop click")
                        return True
            
            logger.warning("Could not dismiss popup")
            raise PopupDismissalError("Failed to dismiss popup after all methods")
            
        except Exception as e:
            logger.error(f"Error dismissing popup: {e}")
            raise PopupDismissalError(f"Error dismissing popup: {str(e)}")
    
    async def wait_for_no_popup(self, page: Page, timeout: int = None) -> bool:
        """
        Wait until popup is no longer visible.
        Learn: Understand async waiting patterns.
        """
        timeout = timeout or self.timeout
        try:
            await page.wait_for_selector(self.popup_selector, state='hidden', timeout=timeout * 1000)
            logger.info("Popup is no longer visible")
            return True
        except PlaywrightTimeoutError:
            logger.warning(f"Popup still visible after {timeout}s timeout")
            return False
    
    async def handle_popup(self, page: Page) -> bool:
        """
        Main popup handling workflow.
        """
        for attempt in range(1, self.max_retries + 1):
            logger.info(f"Popup handling attempt {attempt}/{self.max_retries}")
            
            if await self.detect_popup(page):
                logger.info("Popup detected, attempting to dismiss...")
                if await self.dismiss_popup(page):
                    if await self.wait_for_no_popup(page):
                        return True
            else:
                logger.info("No popup detected")
                return True
        
        logger.warning("Failed to handle popup after all attempts")
        return False


class InfiniteScrollHandler:
    """
    Handles infinite scrolling to load all content.
    Learning: Understand scroll events and content loading patterns.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.scroll_wait = config.get('delays', {}).get('after_scroll', 1)
        self.content_load_timeout = config.get('timeouts', {}).get('content_load', 5)
        self.max_scroll_iterations = config.get('retries', {}).get('scroll_iteration', 50)
        
    async def get_scroll_height(self, page: Page) -> int:
        """Get current scroll height of the page."""
        return await page.evaluate('document.documentElement.scrollHeight')
    
    async def get_scroll_position(self, page: Page) -> int:
        """Get current scroll position."""
        return await page.evaluate('window.pageYOffset + window.innerHeight')
    
    async def scroll_to_bottom(self, page: Page) -> None:
        """
        Scroll page to bottom.
        Learn: Understand JavaScript scroll API.
        """
        last_height = await self.get_scroll_height(page)
        
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        
        # Wait for potential new content
        await asyncio.sleep(self.scroll_wait)
        
        # Wait for network idle (new content might be loading)
        try:
            await page.wait_for_load_state('networkidle', timeout=self.content_load_timeout * 1000)
        except PlaywrightTimeoutError:
            logger.warning("Network did not become idle")
    
    async def is_scroll_complete(self, page: Page) -> bool:
        """
        Check if scrolling is complete (no new content loading).
        Learn: Understand scroll completion detection.
        """
        current_position = await self.get_scroll_position(page)
        document_height = await self.get_scroll_height(page)
        
        # Add a small tolerance for floating point errors
        return current_position >= document_height - 10
    
    async def scroll_until_complete(self, page: Page) -> None:
        """
        Keep scrolling until all content is loaded.
        Learn: Understand iterative scrolling patterns.
        """
        logger.info("Starting infinite scroll handling")
        iterations = 0
        
        while iterations < self.max_scroll_iterations:
            # Get initial state
            initial_height = await self.get_scroll_height(page)
            
            # Scroll to bottom
            await self.scroll_to_bottom(page)
            
            # Wait for content to load
            await asyncio.sleep(self.scroll_wait)
            
            # Check if new content appeared
            new_height = await self.get_scroll_height(page)
            
            if new_height == initial_height:
                logger.info("No new content loaded, scrolling complete")
                break
            else:
                logger.info(f"New content loaded: {initial_height} -> {new_height}")
            
            iterations += 1
            
            if iterations >= self.max_scroll_iterations:
                logger.warning("Reached max scroll iterations")
                raise ScrollTimeoutError(f"Reached maximum scroll iterations: {self.max_scroll_iterations}")
        
        logger.info("Infinite scroll complete")


class ButtonDetector:
    """
    Detects and clicks "See more jobs" button.
    Learning: Understand button states and dynamic content loading.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.button_selector = config.get('selectors', {}).get('more_button', 
                                                               'button:has-text("See more jobs"), button:has-text("See More"), button:has-text("Load More")')
        self.click_wait = config.get('delays', {}).get('after_click', 2)
        self.max_clicks = config.get('retries', {}).get('button_click', 10)
        
    async def find_button(self, page: Page) -> Optional[object]:
        """
        Find the "See more jobs" button.
        Learn: Understand multiple selector strategies.
        """
        # Try different button text variations
        button_texts = [
            "See more jobs",
            "See More Jobs",
            "Load more jobs",
            "Show more jobs",
            "View more jobs"
        ]
        
        for text in button_texts:
            selector = f'button:has-text("{text}")'
            logger.info(f"Looking for button with text: {text}")
            
            button = await page.query_selector(selector)
            if button:
                is_visible = await button.is_visible()
                if is_visible:
                    logger.info(f"Found button: {text}")
                    return button
        
        # Try generic "more" button with various class patterns
        generic_selectors = [
            'button[class*="more"]',
            'button[class*="load"]',
            'button:has-text("more")',
            'a:has-text("See more"), a:has-text("Load more")'
        ]
        
        for selector in generic_selectors:
            button = await page.query_selector(selector)
            if button:
                is_visible = await button.is_visible()
                if is_visible:
                    button_text = await button.inner_text()
                    logger.info(f"Found generic 'more' button: {button_text}")
                    return button
        
        return None
    
    async def is_button_visible(self, page: Page) -> bool:
        """Check if any 'more' button is visible."""
        button = await self.find_button(page)
        return button is not None
    
    async def click_button(self, page: Page, button) -> bool:
        """
        Click the button and wait for content to load.
        Learn: Understand button interactions and content loading.
        """
        try:
            # Scroll button into view
            await button.scroll_into_view_if_needed()
            await asyncio.sleep(0.2)
            
            # Click the button
            logger.info("Clicking button...")
            await button.click()
            
            # Wait for new content to load
            await asyncio.sleep(self.click_wait)
            
            # Wait for network to be idle
            try:
                await page.wait_for_load_state('networkidle', timeout=5000)
            except PlaywrightTimeoutError:
                logger.warning("Network did not become idle after button click")
            
            return True
            
        except Exception as e:
            logger.error(f"Error clicking button: {e}")
            return False
    
    async def click_all_buttons(self, page: Page) -> int:
        """
        Click all "See more jobs" buttons until none remain.
        Learn: Understand iterative button clicking patterns.
        """
        logger.info("Starting button detection and clicking")
        clicks = 0
        
        while clicks < self.max_clicks:
            button = await self.find_button(page)
            
            if not button:
                logger.info("No more buttons found")
                break
            
            if await self.click_button(page, button):
                clicks += 1
                logger.info(f"Clicked button {clicks}/{self.max_clicks}")
            else:
                logger.warning("Failed to click button")
                break
            
            # Wait a bit before checking for next button
            await asyncio.sleep(0.5)
        
        if clicks >= self.max_clicks:
            logger.warning("Reached max button clicks")
        
        if clicks == 0:
            logger.info("No buttons found to click")
        
        logger.info(f"Completed {clicks} button clicks")
        return clicks


class JobExtractor:
    """
    Extracts job data from the page.
    Learning: Understand HTML structure and data extraction patterns.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.job_card_selector = config.get('selectors', {}).get('job_card', 
                                                                 '.job-card, .job-item, .job-listing, [class*="job"]')
        
    async def find_job_elements(self, page: Page) -> List:
        """
        Find all job elements on the page.
        Learn: Understand CSS selectors for job listings.
        """
        # Try multiple selectors
        selectors = [
            self.job_card_selector,
            '.job-card',
            '.job-item',
            '.job-listing',
            'article.job',
            '[data-job-id]',
            '[class*="job-card"]',
            '[class*="job-item"]'
        ]
        
        for selector in selectors:
            logger.info(f"Looking for jobs with selector: {selector}")
            jobs = await page.query_selector_all(selector)
            if jobs:
                logger.info(f"Found {len(jobs)} jobs with selector: {selector}")
                return jobs
        
        logger.warning("No job elements found")
        return []
    
    async def extract_job_data(self, job_element) -> Dict:
        """
        Extract data from a single job element.
        Learn: Understand data extraction from HTML elements.
        """
        job_data = {}
        
        try:
            # Extract title
            title_elem = await job_element.query_selector('h2, h3, .job-title, [class*="title"]')
            if title_elem:
                job_data['title'] = await title_elem.inner_text()
            
            # Extract company
            company_elem = await job_element.query_selector('.company, [class*="company"]')
            if company_elem:
                job_data['company'] = await company_elem.inner_text()
            
            # Extract location
            location_elem = await job_element.query_selector('.location, [class*="location"]')
            if location_elem:
                job_data['location'] = await location_elem.inner_text()
            
            # Extract description
            desc_elem = await job_element.query_selector('.description, [class*="description"], p')
            if desc_elem:
                job_data['description'] = await desc_elem.inner_text()
            
            # Extract URL/link
            link_elem = await job_element.query_selector('a')
            if link_elem:
                href = await link_elem.get_attribute('href')
                if href:
                    job_data['url'] = href
                    # Make absolute URL if relative
                    if href.startswith('/'):
                        job_data['url'] = 'https://example.com' + href
            
            # Extract additional metadata
            job_data['raw_html'] = await job_element.inner_html()
            
        except Exception as e:
            logger.error(f"Error extracting job data: {e}")
            raise ExtractionError(f"Failed to extract job data: {str(e)}")
        
        return job_data
    
    async def extract_all_jobs(self, page: Page) -> List[Dict]:
        """
        Extract all jobs from the page.
        Learn: Understand batch data extraction.
        """
        logger.info("Starting job extraction")
        job_elements = await self.find_job_elements(page)
        
        jobs = []
        for i, element in enumerate(job_elements):
            logger.info(f"Extracting job {i+1}/{len(job_elements)}")
            job_data = await self.extract_job_data(element)
            if job_data:
                jobs.append(job_data)
        
        logger.info(f"Extracted {len(jobs)} jobs")
        return jobs


class JobScraper:
    """
    Main orchestrator for job scraping.
    Combines all components to create complete workflow.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        
        self.popup_handler = PopupHandler(self.config)
        self.scroll_handler = InfiniteScrollHandler(self.config)
        self.button_detector = ButtonDetector(self.config)
        self.job_extractor = JobExtractor(self.config)
        
    def _default_config(self) -> Dict:
        """Default configuration."""
        return {
            'timeouts': {
                'page_load': 30,
                'popup_detection': 5,
                'scroll_wait': 2,
                'content_load': 10,
            },
            'retries': {
                'popup_dismissal': 3,
                'button_click': 3,
                'scroll_iteration': 50,
            },
            'selectors': {
                'popup': '.top-level-modal-container',
                'close_button': 'button.close, button[aria-label="Close"]',
                'job_card': '.job-card, .job-item',
                'more_button': 'button:has-text("See more jobs")',
            },
            'delays': {
                'after_popup': 1,
                'after_scroll': 1,
                'after_click': 2,
            }
        }
    
    async def scrape_jobs(self, url: str) -> List[Dict]:
        """
        Main scraping workflow.
        Learn: Understand complete workflow orchestration.
        """
        from playwright.async_api import async_playwright
        
        logger.info(f"Starting job scraping for URL: {url}")
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Step 1: Load page
                logger.info("Step 1: Loading page")
                try:
                    await page.goto(url, wait_until='networkidle', timeout=60000)
                    await asyncio.sleep(1)
                except Exception as e:
                    raise NetworkError(f"Failed to load page: {str(e)}", url=url)
                
                # Step 2: Handle popup
                logger.info("Step 2: Handling popup")
                await self.popup_handler.handle_popup(page)
                await asyncio.sleep(self.config['delays']['after_popup'])
                
                # Step 3: Infinite scroll
                logger.info("Step 3: Handling infinite scroll")
                await self.scroll_handler.scroll_until_complete(page)
                
                # Step 4: Click "See more jobs" buttons
                logger.info("Step 4: Clicking 'See more jobs' buttons")
                await self.button_detector.click_all_buttons(page)
                
                # Step 5: Extract jobs
                logger.info("Step 5: Extracting jobs")
                jobs = await self.job_extractor.extract_all_jobs(page)
                
                logger.info(f"Scraping complete! Found {len(jobs)} jobs")
                return jobs
                
            except ScrapingError:
                # Re-raise scraping errors
                raise
            except Exception as e:
                # Wrap unexpected errors
                raise ScrapingError(f"Unexpected error during scraping: {str(e)}", url=url)
            finally:
                await browser.close()


# Example usage
if __name__ == '__main__':
    import asyncio
    
    logging.basicConfig(level=logging.INFO)
    
    scraper = JobScraper()
    
    # Run scraper
    url = "https://example.com/jobs"  # Replace with actual URL
    jobs = asyncio.run(scraper.scrape_jobs(url))
    
    print(f"Found {len(jobs)} jobs:")
    for job in jobs:
        print(job)

