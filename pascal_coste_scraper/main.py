from pascal_coste_scraper import PascalCosteScraper
from extraction_file import ExtractFields
from logger_config import logger
from concurrent.futures import ThreadPoolExecutor

def get_all_products(url:str):
    """
    Function to scrape products from a given URL
    """
    page_content = scraper.request_and_get_response(url)
    extractor.scrape_all_products(page_content)

if __name__ == "__main__":

    scraper = PascalCosteScraper(logger)
    extractor = ExtractFields()

    # Get all pagination links from the Pascal Coste website
    all_pages_link = scraper.get_pagination_links()

    # Extract products from all URLs concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(get_all_products, all_pages_link)

    # Create JSON file containing extracted data
    extractor.create_json_file()
