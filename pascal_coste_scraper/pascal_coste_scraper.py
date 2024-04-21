import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import constants


class PascalCosteScraper:
    """A scraper class for Pascal Coste website."""

    def __init__(self, logger):
        """Initialize the scraper."""
        self.logger = logger
        self.retry_threshold = 1

    def get_header(self):
        """Generate headers for the request."""
        headers = Headers(headers=False)
        return headers.generate()

    def get_all_page_links(self, soup):
        """
        Extract all pagination links from the page.

        Args:
            soup (BeautifulSoup): Parsed HTML page.

        Returns:
            list: List of URLs of all pagination links.

        """
        try:
            next_page_links_outer_tags = soup.find(class_="items pages-items")
            next_page_links = next_page_links_outer_tags.find_all("a")

            all_urls = [next_page_link["href"] for next_page_link in next_page_links]
            all_urls.append(constants.MAIN_URL)

            return all_urls
        except Exception as exe:
            self.logger.error("Error in get_all_page_links.")
            self.logger.error(f"Error: {exe}")
            return None

    def request_and_get_response(self, url):
        """
        Make a request to the given URL and return the response.

        Args:
            url (str): The URL to request.
            params (dict, optional): Query parameters for the request. Defaults to None.

        Returns:
            BeautifulSoup: Parsed HTML content if successful, None otherwise.

        """
        try:

            response = requests.get(
                url,
                headers=self.get_header()
            )

            if response.status_code != 200:
                if self.retry_threshold <= 3:
                    self.logger.warning(f"Status Code is: {response.status_code}")
                    self.retry_threshold += 1
                    # Retry the request
                    return self.request_and_get_response(url)
                else:
                    self.logger.error(f"Response Status Repeatedly Gives {response.status_code}")
                    return None
            else:
                self.logger.info("Successful response received.")
                soup = BeautifulSoup(response.content, "html.parser")
                return soup

        except requests.exceptions.RequestException as req_exc:
            self.logger.error(f"Error occurred: {req_exc}")
            return None

    def get_pagination_links(self):
        """
        Get all pagination links from the main page.

        Returns:
            list: List of pagination URLs if successful, None otherwise.

        """

        main_page_content = self.request_and_get_response(url=constants.MAIN_URL)

        if main_page_content is not None:
            all_urls = self.get_all_page_links(main_page_content)

            if all_urls is not None:
                self.logger.info("Successfully Get URLS.")
                return all_urls
            else:
                self.logger.error("Empty URL. No URLs to scrape.")
                return None
        else:
            self.logger.error("Error while fetching main page content.")
            return None
