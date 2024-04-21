import json
from datetime import datetime
import pandas as pd

class ExtractFields:
    """
    A class for extracting and storing information about products from a webpage.
    """

    def __init__(self):
        """
        Initialize the ExtractFields object with an empty dictionary to store product data.
        """
        self.main_data = {
            "name": [],
            "price": [],
            "brand": [],
            "imageUrl": [],
            "productUrl": [],
            "timeStamp": []
        }

    def extract_image_url(self, product):
        """
        Extract the image URL of a product.

        Parameters:
            product (bs4.element.Tag): BeautifulSoup Tag representing a product.

        Returns:
            str: The URL of the product image, or an empty string if not found.
        """
        try:
            return product.find(class_="product-image-photo")["data-amsrc"]
        except (AttributeError, KeyError):
            return ""

    def extract_name(self, product):
        """
        Extract the name of a product.

        Parameters:
            product (bs4.element.Tag): BeautifulSoup Tag representing a product.

        Returns:
            str: The name of the product, or an empty string if not found.
        """
        try:
            return product.find(class_="product-name uk-margin-top").text.encode('latin1').decode('unicode_escape')
        except AttributeError:
            return ""

    def extract_brand(self, product):
        """
        Extract the brand of a product.

        Parameters:
            product (bs4.element.Tag): BeautifulSoup Tag representing a product.

        Returns:
            str: The brand of the product, or an empty string if not found.
        """
        try:
            return product.find(class_="uk-grid uk-grid-small small-label uk-grid-divider uk-flex-center").div.text
        except AttributeError:
            return ""

    def extract_product_url(self, product):
        """
        Extract the URL of a product.

        Parameters:
            product (bs4.element.Tag): BeautifulSoup Tag representing a product.

        Returns:
            str: The URL of the product, or an empty string if not found.
        """
        try:
            return product.find(class_="product-name uk-margin-top").a["href"]
        except AttributeError:
            return ""

    def extract_price(self, product):
        """
        Extract the price of a product.

        Parameters:
            product (bs4.element.Tag): BeautifulSoup Tag representing a product.

        Returns:
            str: The price of the product, or an empty string if not found.
        """
        try:
            return product.find(class_="uk-price").text.replace("\xa0€", "")
        except AttributeError:
            return ""

    def scrape_product_info(self, product):
        """
        Scrape information about a product and add it to the main data dictionary.

        Parameters:
            product (bs4.element.Tag): BeautifulSoup Tag representing a product.
        """
        image_url = self.extract_image_url(product)
        name = self.extract_name(product)
        brand = self.extract_brand(product)
        product_url = self.extract_product_url(product)
        price = self.extract_price(product)

        self.main_data["imageUrl"].append(image_url)
        self.main_data["name"].append(name)
        self.main_data["brand"].append(brand)
        self.main_data["productUrl"].append(product_url)
        self.main_data["price"].append(price)
        self.main_data["timeStamp"].append(str(datetime.now()))

    def scrape_all_products(self, soup):
        """
        Scrape information about all products on a webpage and add them to the main data dictionary.

        Parameters:
            soup (bs4.BeautifulSoup): BeautifulSoup object representing the webpage.
        """
        products = soup.find_all(class_="uk-panel uk-position-relative")

        for product in products:
            self.scrape_product_info(product)

    def create_json_file(self):
        """
        Create a JSON file containing the scraped product data.
        """
        data = pd.DataFrame(self.main_data)

        # Converting it into list of dictionaries starts
        data_for_json_list = data.to_dict('records')
        with open("pascal_coste.json", "w", encoding="utf-8") as final:
            json.dump(data_for_json_list, final, ensure_ascii=False)
        print("JSON file successfully created")
        # Converting it into list of dictionaries ends
