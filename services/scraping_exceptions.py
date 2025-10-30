"""
Custom exceptions for job scraping.
"""
from typing import Optional


class ScrapingError(Exception):
    """Base exception for all scraping errors."""
    def __init__(self, message: str, url: Optional[str] = None):
        self.message = message
        self.url = url
        super().__init__(self.message)


class PopupNotFoundError(ScrapingError):
    """Popup could not be detected when expected."""
    pass


class PopupDismissalError(ScrapingError):
    """Failed to dismiss popup."""
    pass


class ScrollTimeoutError(ScrapingError):
    """Scroll completion timeout exceeded."""
    pass


class ButtonNotFoundError(ScrapingError):
    """Expected button not found."""
    pass


class ButtonClickError(ScrapingError):
    """Failed to click button."""
    pass


class ExtractionError(ScrapingError):
    """Job extraction failed."""
    pass


class NetworkError(ScrapingError):
    """Network request failed."""
    pass


class RateLimitError(ScrapingError):
    """Rate limit exceeded."""
    pass


class AccessDeniedError(ScrapingError):
    """Access denied by website."""
    pass


class ConfigurationError(ScrapingError):
    """Configuration error."""
    pass

