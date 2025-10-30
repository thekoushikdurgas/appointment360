"""
Tests for job scraper service (mocked Playwright)
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from services.job_scraper import JobScraper, PopupHandler, InfiniteScrollHandler


class TestJobScraperService:
    """Test JobScraper service"""
    
    def test_job_scraper_initialization(self):
        """Test job scraper can be initialized"""
        scraper = JobScraper()
        assert scraper is not None
    
    def test_popup_handler_initialization(self):
        """Test popup handler initialization"""
        config = {
            'selectors': {'popup': '.modal', 'close_button': 'button.close'},
            'timeouts': {'popup_detection': 5},
            'retries': {'popup_dismissal': 3}
        }
        handler = PopupHandler(config)
        assert handler.popup_selector == '.modal'
        assert handler.close_button_selector == 'button.close'
    
    @pytest.mark.asyncio
    async def test_popup_detection_mocked(self):
        """Test popup detection with mocked page"""
        config = {
            'selectors': {'popup': '.modal'},
            'timeouts': {'popup_detection': 5}
        }
        handler = PopupHandler(config)
        
        mock_page = AsyncMock()
        mock_page.query_selector = AsyncMock(return_value=Mock())
        mock_page.is_visible = AsyncMock(return_value=True)
        
        result = await handler.detect_popup(mock_page)
        assert isinstance(result, bool)
    
    def test_infinite_scroll_handler_initialization(self):
        """Test infinite scroll handler initialization"""
        config = {
            'selectors': {'more_button': 'button.more'},
            'timeouts': {'scroll_wait': 2},
            'retries': {'scroll_iteration': 50},
            'delays': {'after_scroll': 1}
        }
        handler = InfiniteScrollHandler(config)
        assert handler.more_button_selector == 'button.more'

