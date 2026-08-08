from .parsing import Parsing
from urllib.parse import urlparse
import re
import logging
from typing import Dict, List, Optional, Any, Union
from bs4 import BeautifulSoup, Tag

# Configure logging
logger = logging.getLogger(__name__)


class Home(Parsing):
    def __init__(self, page: int = 1) -> None:
        super().__init__()
        self.__page: int = page
        logger.info(f"Initialized Home scraper for page: {page}")

    def __get_card(self, item: Tag) -> Optional[Dict[str, Union[str, int, None]]]:
        """Extract card information from a home page item (new structure)."""
        try:
            # Find bsx container
            bsx = item.find("div", {"class": "bsx"})
            if not bsx:
                logger.warning("bsx container not found in home item")
                return None

            # Extract link and slug
            link = bsx.find("a", href=True)
            if not link or not link.get("href"):
                logger.warning("Link not found in home item")
                return None

            url = link.get("href")
            slug_path = urlparse(url).path
            slug = (
                slug_path.split("/")[-2]
                if slug_path.endswith("/")
                else slug_path.split("/")[-1]
            )

            # Extract title from h2 inside div.tt
            title_div = bsx.find("div", {"class": "tt"})
            title = "Unknown Title"
            headline = "Unknown"
            
            if title_div:
                h2 = title_div.find("h2")
                if h2:
                    # Get full text and split to get both title and headline
                    full_text = h2.text.strip()
                    # Usually format is: "Title Episode X Subtitle Indonesia"
                    # Extract just the title part (before "Episode" or similar keywords)
                    if " Episode " in full_text:
                        title = full_text.split(" Episode ")[0].strip()
                        headline = full_text
                    elif " Sub " in full_text:
                        title = full_text.split(" Sub ")[0].strip()
                        headline = full_text
                    else:
                        title = full_text
                        headline = full_text

            # Extract type
            type_div = bsx.find("div", {"class": "typez"})
            anime_type = type_div.text.strip() if type_div else "Unknown"

            # Extract episode/status from div.bt
            bt_div = bsx.find("div", {"class": "bt"})
            eps = None
            status = "Unknown"
            
            if bt_div:
                status_text = bt_div.text.strip()
                status = status_text
                # Try to extract episode number
                eps_match = re.search(r'(?:Ep|Episode)\s*(\d+)', status_text)
                if eps_match:
                    eps = int(eps_match.group(1))

            # Extract thumbnail from img
            img = bsx.find("img")
            thumbnail = ""
            if img:
                # Try multiple attributes
                thumbnail = (
                    img.get("data-src") or 
                    img.get("src") or 
                    img.get("data-lazy-src") or
                    ""
                )

            card_data = {
                "title": title,
                "type": anime_type,
                "headline": headline,
                "eps": eps,
                "status": status,
                "thumbnail": thumbnail,
                "slug": slug,
            }

            logger.debug(f"Successfully extracted card data for: {title}")
            return card_data

        except Exception as e:
            logger.error(f"Error extracting card data: {e}")
            return None

    def __get_home(
        self, data: BeautifulSoup
    ) -> Dict[str, Union[List[Dict[str, Any]], int, str]]:
        """Extract home page content from the data (new structure)."""
        cards = []
        try:
            # Find all bixbox sections
            content_sections = data.find_all("div", {"class": "bixbox"})
            logger.info(f"Found {len(content_sections)} bixbox sections in home page")

            for section in content_sections:
                try:
                    # Extract section name from h3 or first header
                    section_name = "unknown"
                    header = section.find(["h1", "h2", "h3"])
                    if header:
                        section_name = header.text.lower().strip().replace(" ", "_")

                    # Find articles with class 'bs'
                    articles = section.find_all("article", {"class": "bs"})
                    section_items = []

                    for article in articles:
                        try:
                            card = self.__get_card(article)
                            if card:
                                section_items.append(card)
                        except Exception as card_error:
                            logger.error(
                                f"Error processing article in section {section_name}: {card_error}"
                            )
                            continue

                    if section_items:
                        cards.append({"section": section_name, "cards": section_items})
                        logger.debug(
                            f"Added section '{section_name}' with {len(section_items)} items"
                        )

                except Exception as section_error:
                    logger.error(f"Error processing section: {section_error}")
                    continue

            result = {
                "results": cards,
                "page": self.__page,
                "total": len(cards),
                "source": self.history_url,
            }

            logger.info(
                f"Successfully processed {len(cards)} sections for page {self.__page}"
            )
            return result

        except Exception as e:
            logger.error(f"Error extracting home page content: {e}")
            return {
                "results": [],
                "page": self.__page,
                "total": 0,
                "source": self.history_url,
                "error": str(e),
            }

    def get_details(self) -> Dict[str, Union[List[Dict[str, Any]], int, str]]:
        """Get home page details."""
        try:
            logger.info(f"Starting to fetch home page for page: {self.__page}")

            url = ""
            if self.__page > 1:
                url = f"/page/{self.__page}/"

            data = self.get_parsed_html(url)
            if not data:
                logger.error("Failed to get home page data")
                return {
                    "results": [],
                    "page": self.__page,
                    "total": 0,
                    "source": self.history_url,
                    "error": "Failed to fetch home page",
                }

            return self.__get_home(data)

        except Exception as e:
            logger.error(f"Error in get_details for page {self.__page}: {e}")
            return {
                "results": [],
                "page": self.__page,
                "total": 0,
                "source": self.history_url,
                "error": str(e),
            }


if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    home = Home(1)
    print(home.get_details())
