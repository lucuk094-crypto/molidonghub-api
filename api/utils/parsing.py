from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv
import cloudscraper
import logging
from typing import Optional, Dict, Any

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class Parsing:
    def __init__(self) -> None:
        # Use cloudscraper instead of requests.Session to bypass Cloudflare
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        self.url: str = "https://anichin.moe"
        self.history_url: Optional[str] = None
        logger.info(f"Initialized Parsing session with CloudScraper for URL: {self.url}")

    def get_parsed_html(self, url: str, **kwargs: Any) -> Optional[BeautifulSoup]:
        """Get parsed HTML content using BeautifulSoup."""
        try:
            # Build full URL
            if url.startswith("/"):
                full_url = f"{self.url}{url}"
            else:
                full_url = f"{self.url}/{url}"

            headers: Dict[str, str] = {
                "User-Agent": getenv(
                    "USER_AGENT",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }

            if kwargs.get("headers"):
                headers.update(kwargs["headers"])
            kwargs["headers"] = headers

            logger.debug(f"Making request to: {full_url}")
            
            # Use cloudscraper to get response
            response = self.scraper.get(full_url, **kwargs)
            response.raise_for_status()
            
            self.history_url = full_url
            
            # response.text already handles decoding properly
            html_content = response.text
            
            if html_content:
                parsed = BeautifulSoup(html_content, "html.parser")
                logger.debug(f"Successfully parsed HTML content for: {url} ({len(html_content)} bytes)")
                return parsed
            else:
                logger.warning(f"No HTML content to parse for: {url}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to parse HTML for {url}: {e}")
            return None

    def parsing(self, data: str) -> Optional[BeautifulSoup]:
        """Parse HTML data using BeautifulSoup."""
        try:
            if not data:
                logger.warning("Empty data provided for parsing")
                return None

            parsed = BeautifulSoup(data, "html.parser")
            logger.debug("Successfully parsed provided HTML data")
            return parsed
        except Exception as e:
            logger.error(f"Failed to parse provided data: {e}")
            return None
